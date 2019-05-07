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

from ontology.io.memory_stream import MemoryStream
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.vm.op_code import PUSHDATA1, PUSHDATA2, PUSHDATA4, PUSH0, PUSH1, PUSHM1, PUSHBYTES75, APPCALL


class ParamsBuilder:
    def __init__(self):
        self.ms = MemoryStream()

    def clear_up(self):
        self.ms.clean_up()

    def emit(self, op):
        self.write_bytes(op)

    def emit_push_bool(self, data: bool):
        if data:
            return self.emit(PUSH1)
        else:
            return self.emit(PUSH0)

    def emit_push_int(self, num: int):
        if num == -1:
            return self.emit(PUSHM1)
        elif num == 0:
            return self.emit(PUSH0)
        elif 0 < num < 16:
            return self.emit(int.from_bytes(PUSH1, 'little') - 1 + num)
        else:
            bs = self.big_int_to_neo_bytearray(num)
            return self.emit_push_bytearray(bs)

    def emit_push_bytearray(self, data):
        data_len = len(data)
        if data_len < int.from_bytes(PUSHBYTES75, 'little'):
            self.write_bytes(bytearray([data_len]))
        elif data_len < 0x100:
            self.emit(PUSHDATA1)
            self.write_bytes(bytearray([data_len]))
        elif data_len < 0x10000:
            self.emit(PUSHDATA2)
            self.write_bytes(len(data).to_bytes(2, "little"))
        else:
            self.emit(PUSHDATA4)
            self.write_bytes(len(data).to_bytes(4, "little"))
        self.write_bytes(data)

    def emit_push_call(self, address):
        self.emit(APPCALL)
        self.write_bytes(address)

    def write_bytes(self, value: bytearray or bytes or str or int):
        if isinstance(value, bytearray) or isinstance(value, bytes):
            self.ms.write(value)
        elif isinstance(value, str):
            self.ms.write(value.encode('utf-8'))
        elif isinstance(value, int):
            self.ms.write(bytes([value]))
        else:
            raise SDKException(ErrorCode.param_err('type error, write byte failed.'))

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

    def to_bytes(self) -> bytes:
        return self.ms.to_bytes()

    def to_bytearray(self) -> bytearray:
        return bytearray(self.ms.to_bytes())
