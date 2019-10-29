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

from ontology.common.address import Address
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.base_params_builder import BaseParamsBuilder

WASM_INT128_SIZE = 16
WASM_INT128_FF = b'\xff' * WASM_INT128_SIZE
WASM_INT128_MAX = 2 ** 127 - 1
WASM_INT128_MIN = -2 ** 127

WASM_TRUE = b'\x01'
WASM_FALSE = b'\x00'


class WasmParamsBuilder(BaseParamsBuilder):
    def __init__(self):
        super().__init__()

    def push_vm_param(self, param):
        if isinstance(param, str):
            self.push_str(param)
        elif isinstance(param, bool):
            self.push_bool(param)
        elif isinstance(param, int):
            self.push_int(param)
        elif isinstance(param, Address):
            self.push_address(param)
        elif isinstance(param, bytes):
            self.push_bytes(param)
        elif isinstance(param, bytearray):
            self.push_bytearray(param)
        elif isinstance(param, list):
            self.push_list(param)
        else:
            raise SDKException(ErrorCode.other_error('parameter type is error'))

    def pack_as_bytearray(self) -> bytearray:
        data = self.to_bytearray()
        self.clear_up()
        self.push_bytearray(data)
        return self.to_bytearray()

    def push_list(self, value: list):
        if not isinstance(value, list):
            raise SDKException(ErrorCode.other_error('invalid data'))
        self.write_var_uint(len(value))
        for param in value:
            self.push_vm_param(param)

    def write_var_uint(self, value: int):
        if not isinstance(value, int):
            raise SDKException(ErrorCode.other_error('invalid data'))
        if value < 0:
            raise SDKException(ErrorCode.other_error('invalid data'))
        elif value < 0xFD:
            self.write_bytes(value.to_bytes(length=1, byteorder='little', signed=False))
        elif value < 0xFFFF:
            self.write_bytes(b'\xFD')
            self.write_bytes(value.to_bytes(length=2, byteorder='little', signed=False))
        elif value < 0xFFFFFFFF:
            self.write_bytes(b'\xFE')
            self.write_bytes(value.to_bytes(length=4, byteorder='little', signed=False))
        else:
            self.write_bytes(b'\xFF')
            self.write_bytes(value.to_bytes(length=8, byteorder='little', signed=False))

    def push_int(self, value: int):
        if not isinstance(value, int):
            raise SDKException(ErrorCode.other_error('invalid data'))
        if value < WASM_INT128_MIN or value > WASM_INT128_MAX:
            raise SDKException(ErrorCode.other_error("out of range"))
        self.write_bytes(value.to_bytes(length=WASM_INT128_SIZE, byteorder='little', signed=True))

    def push_str(self, value: str):
        if not isinstance(value, str):
            raise SDKException(ErrorCode.other_error('invalid data'))
        self.push_bytes(value.encode('utf-8'))

    def push_address(self, value: Address):
        if not isinstance(value, Address):
            raise SDKException(ErrorCode.other_error('invalid data'))
        self.write_bytes(value.to_bytearray())

    def push_bool(self, value: bool):
        if not isinstance(value, bool):
            raise SDKException(ErrorCode.other_error('invalid data'))
        if value:
            self.write_bytes(WASM_TRUE)
        else:
            self.write_bytes(WASM_FALSE)

    def push_bytearray(self, value: bytearray):
        if not isinstance(value, bytearray):
            raise SDKException(ErrorCode.other_error('invalid data'))
        self.write_var_uint(len(value))
        self.write_bytes(value)

    def push_bytes(self, value: bytes):
        if not isinstance(value, bytes):
            raise SDKException(ErrorCode.other_error('invalid data'))
        self.write_var_uint(len(value))
        self.write_bytes(value)
