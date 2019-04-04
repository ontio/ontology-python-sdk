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

import base58

from typing import List

from ontology.vm.op_code import CHECKSIG
from ontology.crypto.digest import Digest
from ontology.core.program import ProgramBuilder
from ontology.exception.error_code import ErrorCode
from ontology.vm.params_builder import ParamsBuilder
from ontology.exception.exception import SDKException


class Address(object):
    __COIN_VERSION = b'\x17'

    def __init__(self, script_hash: bytes):
        if not isinstance(script_hash, bytes):
            raise SDKException(ErrorCode.other_error('Invalid script hash.'))
        if len(script_hash) != 20:
            raise SDKException(ErrorCode.other_error('Invalid script hash.'))
        self.ZERO = script_hash

    @staticmethod
    def to_script_hash(byte_script) -> bytes:
        return Digest.hash160(msg=byte_script, is_hex=False)

    @staticmethod
    def address_from_bytes_pubkey(public_key: bytes):
        builder = ParamsBuilder()
        builder.emit_push_bytearray(bytearray(public_key))
        builder.emit(CHECKSIG)
        addr = Address(Address.to_script_hash(builder.to_bytes()))
        return addr

    @staticmethod
    def address_from_multi_pub_keys(m: int, pub_keys: List[bytes]):
        return Address(Address.to_script_hash(ProgramBuilder.program_from_multi_pubkey(m, pub_keys)))

    @staticmethod
    def b58_address_from_multi_pub_keys(m: int, pub_keys: List[bytes]):
        return Address(Address.to_script_hash(ProgramBuilder.program_from_multi_pubkey(m, pub_keys))).b58encode()

    @staticmethod
    def address_from_vm_code(code: str):
        """
        generate contract address from avm bytecode.
        :param code: str
        :return: Address
        """
        script_hash = Address.to_script_hash(bytearray.fromhex(code))[::-1]
        return Address(script_hash)

    def b58encode(self):
        script_builder = Address.__COIN_VERSION + self.ZERO
        c256 = Digest.hash256(script_builder)[0:4]
        out_bytes = script_builder + c256
        return base58.b58encode(out_bytes).decode('utf-8')

    def to_bytes(self):
        return self.ZERO

    def to_bytearray(self):
        return bytearray(self.ZERO)

    def to_hex_str(self):
        return bytes.hex(self.ZERO)

    def to_reverse_hex_str(self):
        bytearray_zero = bytearray(self.ZERO)
        bytearray_zero.reverse()
        return bytearray.hex(bytearray_zero)

    @classmethod
    def b58decode(cls, address: str):
        data = base58.b58decode(address)
        if len(data) != 25:
            raise SDKException(ErrorCode.param_error)
        if data[0] != int.from_bytes(Address.__COIN_VERSION, "little"):
            raise SDKException(ErrorCode.param_error)
        checksum = Digest.hash256(data[0:21])
        if data[21:25] != checksum[0:4]:
            raise SDKException(ErrorCode.param_error)
        return cls(data[1:21])
