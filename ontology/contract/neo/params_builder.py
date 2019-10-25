"""
Copyright (C) 2018-2019 The ontology Authors
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
from struct import Struct

from ontology.vm.op_code import (
    PACK,
    NEWMAP,
    TOALTSTACK,
    DUPFROMALTSTACK,
    SETITEM,
    FROMALTSTACK,
    NEWSTRUCT,
    SWAP,
    APPEND,
    PUSH1, PUSH0, PUSHM1, APPCALL)

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.base_params_builder import BaseParamsBuilder
from ontology.common.address import Address
from ontology.account.account import Account


class NeoParamsBuilder(BaseParamsBuilder):
    def __init__(self):
        super().__init__()

    def push_vm_param(self, param):
        if isinstance(param, bytearray) or isinstance(param, bytes):
            self.push_bytearray(param)
        elif isinstance(param, str):
            self.push_bytearray(bytes(param.encode()))
        elif isinstance(param, bool):
            self.push_bool(param)
        elif isinstance(param, int):
            self.push_int(param)
        elif isinstance(param, dict):
            self.push_map(param)
        elif isinstance(param, list):
            self.create_code_params_script_builder(param)
            self.push_int(len(param))
            self.emit(PACK)
        elif isinstance(param, Struct):
            self.push_struct(param)
        elif isinstance(param, Address):
            self.push_bytearray(param.to_bytes())
        elif isinstance(param, Account):
            self.push_bytearray(param.get_address().to_bytes())
        else:
            raise SDKException(ErrorCode.other_error('parameter type is error'))

    def push_map(self, dict_param: dict):
        self.emit(NEWMAP)
        self.emit(TOALTSTACK)
        for key, value in dict_param.items():
            self.emit(DUPFROMALTSTACK)
            self.push_vm_param(key)
            self.push_vm_param(value)
            self.emit(SETITEM)
        self.emit(FROMALTSTACK)

    def create_code_params_script_builder(self, param_list: list):
        length = len(param_list)
        for j in range(length):
            i = length - 1 - j
            self.push_vm_param(param_list[i])
        return self.to_bytes()

    def push_struct(self, struct_param: Struct):
        self.push_int(0)
        self.emit(NEWSTRUCT)
        self.emit(TOALTSTACK)
        for item in struct_param.param_list:
            self.push_vm_param(item)
            self.emit(DUPFROMALTSTACK)
            self.emit(SWAP)
            self.emit(APPEND)
        self.emit(FROMALTSTACK)

    def push_bool(self, data: bool):
        if data:
            return self.emit(PUSH1)
        else:
            return self.emit(PUSH0)

    def push_int(self, num: int):
        if num == -1:
            return self.emit(PUSHM1)
        elif num == 0:
            return self.emit(PUSH0)
        elif 0 < num < 16:
            return self.emit(int.from_bytes(PUSH1, 'little') - 1 + num)
        else:
            bs = self.big_int_to_neo_bytearray(num)
            return self.push_bytearray(bs)

    def emit_push_call(self, address: bytes):
        self.emit(APPCALL)
        self.write_bytes(address)

    @staticmethod
    def int_to_bytearray(data: int):
        bit_length = data.bit_length() // 8
        t = data.bit_length() / 8
        if bit_length <= t:
            bit_length += 1
        return bytearray(data.to_bytes(bit_length, "big", signed=True))

    def big_int_to_neo_bytearray(self, data: int) -> bytearray:
        if data == 0:
            return bytearray()
        data_bytes = self.int_to_bytearray(data)
        if len(data_bytes) == 0:
            return bytearray()
        if data < 0:
            data_bytes2 = self.int_to_bytearray(-data)
            b = data_bytes2[0]
            data_bytes.reverse()
            if b >> 7 == 1:
                res = data_bytes[:] + bytearray([255])
                return res
            return data_bytes
        else:
            b = data_bytes[0]
            data_bytes.reverse()
            if b >> 7 == 1:
                res = data_bytes[:] + bytearray([0])
                return res
            return data_bytes
