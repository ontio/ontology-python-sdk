#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from ontology.utils.utils import bytes_reader
from ontology.core.program import ProgramBuilder
from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Sig(object):
    def __init__(self, public_keys=None, m: int = 0, sig_data=None):
        self.public_keys = public_keys  # a list to save public keys
        self.m = m
        self.sig_data = sig_data

    def __iter__(self):
        data = dict(M=self.m, publicKeys=list(), sigData=list())
        for key in self.public_keys:
            data['publicKeys'].append(binascii.b2a_hex(key).decode('ascii'))
        for s_data in self.sig_data:
            data['sigData'].append(binascii.b2a_hex(s_data).decode('ascii'))
        for key, value in data.items():
            yield (key, value)

    def serialize(self) -> bytes:
        invoke_script = ProgramBuilder.program_from_params(self.sig_data)
        if len(self.public_keys) == 0:
            raise SDKException(ErrorCode.other_error('Public key in sig is empty.'))

        if len(self.public_keys) == 1:
            verification_script = ProgramBuilder.program_from_pubkey(self.public_keys[0])
        else:
            verification_script = ProgramBuilder.program_from_multi_pubkey(self.M, self.public_keys)
        ms = StreamManager.GetStream()
        writer = BinaryWriter(ms)
        writer.write_var_bytes(invoke_script)
        writer.write_var_bytes(verification_script)
        ms.flush()
        res = ms.to_bytes()
        res = bytes_reader(res)
        StreamManager.ReleaseStream(ms)
        return res

    @staticmethod
    def deserialize_from(sig_bytes: bytes):
        ms = StreamManager.GetStream(sig_bytes)
        reader = BinaryReader(ms)
        return Sig.deserialize(reader)

    @staticmethod
    def deserialize(reader: BinaryReader):
        invocation_script = reader.read_var_bytes()
        verification_script = reader.read_var_bytes()
        sig = Sig()
        sig.sig_data = ProgramBuilder.get_param_info(invocation_script)
        info = ProgramBuilder.get_program_info(verification_script)

        sig.public_keys = info.pubkeys
        sig.m = info.m
        return sig
