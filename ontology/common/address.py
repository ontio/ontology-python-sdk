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

from typing import List, Union

from ontology.vm.op_code import CHECKSIG
from ontology.crypto.digest import Digest
from ontology.core.program import ProgramBuilder
from ontology.exception.error_code import ErrorCode
from ontology.vm.params_builder import ParamsBuilder
from ontology.crypto.hd_public_key import HDPublicKey
from ontology.exception.exception import SDKException


class Address(object):
    __COIN_VERSION = b'\x17'

    def __init__(self, script_hash: Union[bytes, bytearray]):
        if not isinstance(script_hash, bytes):
            try:
                script_hash = bytes(script_hash)
            except TypeError:
                raise SDKException(ErrorCode.other_error('Invalid script hash.'))
        if len(script_hash) != 20:
            raise SDKException(ErrorCode.other_error('Invalid script hash.'))
        self.ZERO = script_hash

    @classmethod
    def __from_byte_script(cls, byte_script: bytes, little_endian: bool = True):
        if not little_endian:
            return cls(Digest.hash160(msg=byte_script, is_hex=False)[::-1])
        return cls(Digest.hash160(msg=byte_script, is_hex=False))

    @classmethod
    def from_public_key(cls, public_key: bytes):
        builder = ParamsBuilder()
        builder.emit_push_bytearray(bytearray(public_key))
        builder.emit(CHECKSIG)
        return cls.__from_byte_script(builder.to_bytes())

    @classmethod
    def from_hd_public_key(cls, hd_public_key: HDPublicKey):
        return cls.from_public_key(hd_public_key.to_bytes())

    @classmethod
    def from_multi_pub_keys(cls, m: int, pub_keys: List[bytes]):
        return cls.__from_byte_script(ProgramBuilder.program_from_multi_pubkey(m, pub_keys))

    @classmethod
    def from_avm_code(cls, code: str):
        """
        generate contract address from avm bytecode.
        """
        return cls.__from_byte_script(bytes.fromhex(code), little_endian=False)

    def b58encode(self):
        data = Address.__COIN_VERSION + self.ZERO
        checksum = Digest.hash256(data)[0:4]
        return base58.b58encode(data + checksum).decode('utf-8')

    def to_bytes(self):
        return self.ZERO

    def to_bytearray(self):
        return bytearray(self.ZERO)

    def hex(self, little_endian: bool = True):
        if little_endian:
            return self.ZERO.hex()
        bytearray_zero = bytearray(self.ZERO)
        bytearray_zero.reverse()
        return bytearray_zero.hex()

    @classmethod
    def b58decode(cls, address: str):
        if isinstance(address, Address):
            return address
        if isinstance(address, bytes):
            return cls(address)
        data = base58.b58decode(address)
        if len(data) != 25:
            raise SDKException(ErrorCode.param_error)
        if data[0] != int.from_bytes(Address.__COIN_VERSION, "little"):
            raise SDKException(ErrorCode.param_error)
        checksum = Digest.hash256(data[0:21])
        if data[21:25] != checksum[0:4]:
            raise SDKException(ErrorCode.param_error)
        return cls(data[1:21])
