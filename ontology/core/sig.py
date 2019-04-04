"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

from ontology.utils.utils import bytes_reader
from ontology.core.program import ProgramBuilder
from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Sig(object):
    def __init__(self, public_keys=None, m: int = 0, sig_data: list = None):
        self.public_keys = public_keys  # a list to save public keys
        self.m = m
        if sig_data is None:
            sig_data = list()
        self.__sig_data = sig_data

    def __iter__(self):
        data = dict(M=self.m, publicKeys=list(), sigData=list())
        for key in self.public_keys:
            data['publicKeys'].append(bytes.hex(key))
        for s_data in self.__sig_data:
            data['sigData'].append(bytes.hex(s_data))
        for key, value in data.items():
            yield (key, value)

    @property
    def sig_data(self):
        return self.__sig_data

    @sig_data.setter
    def sig_data(self, sig_data):
        self.__sig_data = sig_data

    def serialize(self) -> bytes:
        invoke_script = ProgramBuilder.program_from_params(self.__sig_data)
        if len(self.public_keys) == 0:
            raise SDKException(ErrorCode.other_error('Public key in sig is empty.'))

        if len(self.public_keys) == 1:
            verification_script = ProgramBuilder.program_from_pubkey(self.public_keys[0])
        else:
            verification_script = ProgramBuilder.program_from_multi_pubkey(self.m, self.public_keys)
        ms = StreamManager.get_stream()
        writer = BinaryWriter(ms)
        writer.write_var_bytes(invoke_script)
        writer.write_var_bytes(verification_script)
        ms.flush()
        res = ms.hexlify()
        res = bytes_reader(res)
        StreamManager.release_stream(ms)
        return res

    @staticmethod
    def deserialize_from(sig_bytes: bytes):
        ms = StreamManager.get_stream(sig_bytes)
        reader = BinaryReader(ms)
        return Sig.deserialize(reader)

    @staticmethod
    def deserialize(reader: BinaryReader):
        invocation_script = reader.read_var_bytes()
        verification_script = reader.read_var_bytes()
        sig = Sig()
        sig.__sig_data = ProgramBuilder.get_param_info(invocation_script)
        info = ProgramBuilder.get_program_info(verification_script)

        sig.public_keys = info.pubkeys
        sig.m = info.m
        return sig
