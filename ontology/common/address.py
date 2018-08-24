#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base58
from binascii import a2b_hex

from ontology.vm.op_code import CHECKSIG
from ontology.crypto.digest import Digest
from ontology.common.error_code import ErrorCode
from ontology.core.program import ProgramBuilder
from ontology.vm.params_builder import ParamsBuilder
from ontology.exception.exception import SDKException


class Address(object):
    __COIN_VERSION = b'\x17'

    def __init__(self, value: bytes):
        self.ZERO = value  # 20 bytes

    @staticmethod
    def to_script_hash(byte_script):
        return a2b_hex(Digest.hash160(msg=byte_script, is_hex=True))

    @staticmethod
    def address_from_bytes_pubkey(public_key: bytes):
        builder = ParamsBuilder()
        builder.emit_push_byte_array(bytearray(public_key))
        builder.emit(CHECKSIG)
        addr = Address(Address.to_script_hash(builder.to_array()))
        return addr

    @staticmethod
    def address_from_multi_pub_keys(m: int, pub_keys: []):
        return Address(Address.to_script_hash(ProgramBuilder.program_from_multi_pubkey(m, pub_keys)))

    # this function is for contract
    @staticmethod
    def address_from_vm_code(code: str):
        return Address(Address.to_script_hash(bytearray.fromhex(code)))

    def b58encode(self):
        sb = Address.__COIN_VERSION + self.ZERO
        c256 = Digest.hash256(sb)[0:4]
        outb = sb + bytearray(c256)
        return base58.b58encode(bytes(outb)).decode('utf-8')

    def to_array(self):
        return self.ZERO

    def to_byte_array(self):
        return bytearray(self.ZERO)

    def to_hex_str(self):
        return bytearray(self.ZERO).hex()

    def to_reverse_hex_str(self):
        temp = bytearray(self.ZERO)
        temp.reverse()
        return temp.hex()

    @staticmethod
    def b58decode(address: str) -> bytes:
        data = base58.b58decode(address)
        if len(data) != 25:
            raise SDKException(ErrorCode.param_error)
        if data[0] != int.from_bytes(Address.__COIN_VERSION, "little"):
            raise SDKException(ErrorCode.param_error)
        checksum = Digest.hash256(data[0:21])
        if data[21:25] != checksum[0:4]:
            raise SDKException(ErrorCode.param_error)
        return data[1:21]

    @staticmethod
    def decode_base58(address: str):
        return Address(Address.b58decode(address))
