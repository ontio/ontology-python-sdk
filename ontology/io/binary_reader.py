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

import sys
import struct
import binascii
import importlib

from ontology.io.memory_stream import StreamManager
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class BinaryReader(StreamManager):
    """
    Description:
    Binary Reader

    Usage:
        from ontology.io.binary_reader import BinaryReader
    """

    def __init__(self, stream):
        """
        Create an instance.

        Args:
            stream (BytesIO): a stream to operate on. i.e. a neo.IO.MemoryStream or raw BytesIO.
        """
        super().__init__()
        self.stream = stream

    def unpack(self, fmt, length=1):
        """
        Unpack the stream contents according to the specified format in `fmt`.
        For more information about the `fmt` format see: https://docs.python.org/3/library/struct.html

        Args:
            fmt (str): format string.
            length (int): amount of bytes to read.

        Returns:
            variable: the result according to the specified format.
        """
        try:
            info = struct.unpack(fmt, self.stream.read(length))[0]
        except struct.error as e:
            raise SDKException(ErrorCode.unpack_error(e.args[0]))
        return info

    def read_byte(self, do_ord=True) -> int:
        """
        Read a single byte.
        Args:
            do_ord (bool): (default True) convert the byte to an ordinal first.
        Returns:
            bytes: a single byte if successful. 0 (int) if an exception occurred.
        """
        try:
            if do_ord:
                return ord(self.stream.read(1))
            else:
                return self.stream.read(1)
        except Exception as e:
            raise SDKException(ErrorCode.read_byte_error(e.args[0]))

    def read_bytes(self, length) -> bytes:
        """
        Read the specified number of bytes from the stream.

        Args:
            length (int): number of bytes to read.

        Returns:
            bytes: `length` number of bytes.
        """
        value = self.stream.read(length)
        return value

    def read_bool(self):
        """
        Read 1 byte as a boolean value from the stream.

        Returns:
            bool:
        """
        return self.unpack('?')

    def read_char(self):
        """
        Read 1 byte as a character from the stream.

        Returns:
            str: a single character.
        """
        return self.unpack('c')

    def read_float(self, little_endian=True):
        """
        Read 4 bytes as a float value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            float:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack("%sf" % endian, 4)

    def read_double(self, little_endian=True):
        """
        Read 8 bytes as a double value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            float:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack("%sd" % endian, 8)

    def read_int8(self, little_endian=True):
        """
        Read 1 byte as a signed integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%sb' % endian)

    def read_uint8(self, little_endian=True):
        """
        Read 1 byte as an unsigned integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%sB' % endian)

    def read_int16(self, little_endian=True):
        """
        Read 2 byte as a signed integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%sh' % endian, 2)

    def read_uint16(self, little_endian=True):
        """
        Read 2 byte as an unsigned integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%sH' % endian, 2)

    def read_int32(self, little_endian=True):
        """
        Read 4 bytes as a signed integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%si' % endian, 4)

    def read_uint32(self, little_endian=True):
        """
        Read 4 bytes as an unsigned integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%sI' % endian, 4)

    def read_int64(self, little_endian=True):
        """
        Read 8 bytes as a signed integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%sq' % endian, 8)

    def read_uint64(self, little_endian=True):
        """
        Read 8 bytes as an unsigned integer value from the stream.

        Args:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int:
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.unpack('%sQ' % endian, 8)

    def read_var_int(self, max_size=sys.maxsize):
        """
        Read a variable length integer from the stream.
        The NEO network protocol supports encoded storage for space saving. See: http://docs.neo.org/en-us/node/network-protocol.html#convention

        Args:
            max_size (int): (Optional) maximum number of bytes to read.

        Returns:
            int:
        """
        fb = self.read_byte()
        if fb is 0:
            return fb
        if hex(fb) == '0xfd':
            value = self.read_uint16()
        elif hex(fb) == '0xfe':
            value = self.read_uint32()
        elif hex(fb) == '0xff':
            value = self.read_uint64()
        else:
            value = fb
        if value > max_size:
            raise SDKException(ErrorCode.param_err('Invalid format'))
        return int(value)

    def read_var_bytes(self, max_size=sys.maxsize) -> bytes:
        """
        Read a variable length of bytes from the stream.

        Args:
            max_size (int): (Optional) maximum number of bytes to read.

        Returns:
            bytes:
        """
        length = self.read_var_int(max_size)
        return self.read_bytes(length)

    def read_str(self):
        """
        Read a string from the stream.

        Returns:
            str:
        """
        length = self.read_uint8()
        return self.unpack(str(length) + 's', length)

    def read_var_str(self, max_size=sys.maxsize):
        """
        Similar to `ReadString` but expects a variable length indicator instead of the fixed 1 byte indicator.

        Args:
            max_size (int): (Optional) maximum number of bytes to read.

        Returns:
            bytes:
        """
        length = self.read_var_int(max_size)
        return self.unpack(str(length) + 's', length)

    def read_fixed_str(self, length):
        """
        Read a fixed length string from the stream.
        Args:
            length (int): length of string to read.

        Returns:
            bytes:
        """
        return self.read_bytes(length).rstrip(b'\x00')

    def read_serializable_array(self, class_name, max_size=sys.maxsize):
        """
        Deserialize a stream into the object specific by `class_name`.

        Args:
            class_name (str): a full path to the class to be deserialized into. e.g. 'neo.Core.Block.Block'
            max_size (int): (Optional) maximum number of bytes to read.

        Returns:
            list: list of `class_name` objects deserialized from the stream.
        """
        module = '.'.join(class_name.split('.')[:-1])
        class_name = class_name.split('.')[-1]
        class_attr = getattr(importlib.import_module(module), class_name)
        length = self.read_var_int(max_size=max_size)
        items = []
        try:
            for _ in range(0, length):
                item = class_attr()
                item.Deserialize(self)
                items.append(item)
        except Exception as e:
            raise SDKException(ErrorCode.param_err("Couldn't deserialize %s" % e))
        return items

    def read_2000256_list(self):
        """
        Read 2000 times a 64 byte value from the stream.

        Returns:
            list: a list containing 2000 64 byte values in reversed form.
        """
        items = []
        for _ in range(0, 2000):
            data = self.read_bytes(64)
            ba = bytearray(binascii.unhexlify(data))
            ba.reverse()
            items.append(ba.hex().encode('utf-8'))
        return items

    def read_hashes(self):
        """
        Read Hash values from the stream.

        Returns:
            list: a list of hash values. Each value is of the bytearray type.
        """
        var_len = self.read_var_int()
        items = []
        for _ in range(0, var_len):
            ba = bytearray(self.read_bytes(32))
            ba.reverse()
            items.append(ba.hex())
        return items
