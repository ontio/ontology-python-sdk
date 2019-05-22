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

import struct
import binascii
from typing import Union

from ontology.io.memory_stream import StreamManager, MemoryStream
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class BinaryWriter(StreamManager):
    def __init__(self, stream: MemoryStream):
        """
        Create an instance from a stream to operate on. i.e. a ontology.io.memory_stream or raw BytesIO.
        """
        super().__init__()
        self.stream = stream

    def write_byte(self, value: Union[bytes, str, int]):
        """
        Write a single byte to the stream.
        """
        if isinstance(value, bytes):
            self.stream.write(value[:1])
        elif isinstance(value, str):
            self.stream.write(value.encode('utf-8')[:1])
        elif isinstance(value, int):
            self.stream.write(bytes([value]))

    def write_bytes(self, value, to_bytes: bool = False):
        if to_bytes:
            try:
                value = bytes.fromhex(value)
            except ValueError:
                pass
        return self.stream.write(value)

    def pack(self, fmt, data):
        """
        Write bytes by packing them according to the provided format `fmt`.
        For more information about the `fmt` format see: https://docs.python.org/3/library/struct.html
        """
        return self.write_bytes(struct.pack(fmt, data))

    def write_char(self, value):
        """
        Write a 1 byte character value to the stream.
        """
        return self.pack('c', value)

    def write_int8(self, value, little_endian=True):
        """
        Pack the value as a signed byte and write 1 byte to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%sb' % endian, value)

    def write_uint8(self, value, little_endian=True):
        """
        Pack the value as an unsigned byte and write 1 byte to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%sB' % endian, value)

    def write_bool(self, value: bool):
        """
        Pack the value as a bool and write 1 byte to the stream.
        """
        return self.pack('?', value)

    def write_int16(self, value, little_endian=True):
        """
        Pack the value as a signed integer and write 2 bytes to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%sh' % endian, value)

    def write_uint16(self, value, little_endian=True):
        """
        Pack the value as an unsigned integer and write 2 bytes to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%sH' % endian, value)

    def write_int32(self, value, little_endian=True):
        """
        Pack the value as a signed integer and write 4 bytes to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%si' % endian, value)

    def write_uint32(self, value, little_endian=True):
        """
        Pack the value as an unsigned integer and write 4 bytes to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%sI' % endian, value)

    def write_int64(self, value, little_endian=True):
        """
        Pack the value as a signed integer and write 8 bytes to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%sq' % endian, value)

    def write_uint64(self, value, little_endian=True):
        """
        Pack the value as an unsigned integer and write 8 bytes to the stream.
        """
        if little_endian:
            endian = '<'
        else:
            endian = '>'
        return self.pack('%sQ' % endian, value)

    def write_var_int(self, value: int, little_endian=True):
        """
        Write an integer value in a space saving way to the stream.
        """
        if not isinstance(value, int):
            raise SDKException(ErrorCode.param_err('%s not int type.' % value))

        if value < 0:
            raise SDKException(ErrorCode.param_err('%d too small.' % value))

        elif value < 0xfd:
            return self.write_byte(value)

        elif value <= 0xffff:
            self.write_byte(0xfd)
            return self.write_uint16(value, little_endian)

        elif value <= 0xFFFFFFFF:
            self.write_byte(0xfe)
            return self.write_uint32(value, little_endian)

        else:
            self.write_byte(0xff)
            return self.write_uint64(value, little_endian)

    def write_var_bytes(self, value: bytes, little_endian: bool = True):
        """
        Write an integer value in a space saving way to the stream.
        """
        length = len(value)
        self.write_var_int(length, little_endian)
        return self.write_bytes(value, to_bytes=False)

    def write_var_str(self, value: str, encoding: str = 'utf-8'):
        """
        Write a string value to the stream.
        """
        if isinstance(value, str):
            value = value.encode(encoding)
        self.write_var_int(len(value))
        self.write_bytes(value)

    def write_fixed_str(self, value, length):
        """
        Write a string value to the stream.
        """
        towrite = value.encode('utf-8')
        slen = len(towrite)
        if slen > length:
            raise SDKException(ErrorCode.param_err('string longer than fixed length: %s' % length))
        self.write_bytes(towrite)
        diff = length - slen

        while diff > 0:
            self.write_byte(0)
            diff -= 1

    def write_serializable_array(self, array):
        """
        Write an array of serializable objects to the stream.
        """
        if array is None:
            self.write_byte(0)
        else:
            self.write_var_int(len(array))
            for item in array:
                item.Serialize(self)

    def write_hashes(self, arr):
        """
        Write an array of hashes to the stream.
        """
        length = len(arr)
        self.write_var_int(length)
        for item in arr:
            ba = bytearray(binascii.unhexlify(item))
            ba.reverse()
            self.write_bytes(ba)

    def write_fixed8(self, value, unsigned=False):
        """
        Write a Fixed8 value to the stream.
        """
        if unsigned:
            return self.write_uint64(int(value.value))
        return self.write_int64(value.value)
