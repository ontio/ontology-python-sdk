#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ontology Binary Writer
"""

import struct
import binascii

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


def swap32(i):
    """
    Change the endianness from little endian to big endian.
    Args:
        i (int):

    Returns:
        int:
    """
    return struct.unpack("<I", struct.pack(">I", i))[0]


class BinaryWriter(object):
    """
    Description:
    Binary Writer

    Usage:
        from ontology.io.binary_writer import BinaryWriter
    """

    def __init__(self, stream):
        """
        Create an instance.

        Args:
            stream (BytesIO): a stream to operate on. i.e. a neo.IO.MemoryStream or raw BytesIO.
        """
        super(BinaryWriter, self).__init__()
        self.stream = stream

    def write_byte(self, value):
        """
        Write a single byte to the stream.

        Args:
            value (bytes, str or int): value to write to the stream.
        """
        if type(value) is bytes:
            self.stream.write(value)
        elif type(value) is str:
            self.stream.write(value.encode('utf-8'))
        elif type(value) is int:
            self.stream.write(bytes([value]))

    def write_bytes(self, value, unhex=True):
        """
        Write a `bytes` type to the stream.

        Args:
            value (bytes): array of bytes to write to the stream.
            unhex (bool): (Default) True. Set to unhexlify the stream. Use when the bytes are not raw bytes; i.e. b'aabb'

        Returns:
            int: the number of bytes written.
        """
        if unhex:
            try:
                value = binascii.unhexlify(value)
            except binascii.Error:
                pass
        return self.stream.write(value)

    def pack(self, fmt, data):
        """
        Write bytes by packing them according to the provided format `fmt`.
        For more information about the `fmt` format see: https://docs.python.org/3/library/struct.html

        Args:
            fmt (str): format string.
            data (object): the data to write to the raw stream.

        Returns:
            int: the number of bytes written.
        """
        return self.write_bytes(struct.pack(fmt, data), unhex=False)

    def WriteChar(self, value):
        """
        Write a 1 byte character value to the stream.

        Args:
            value: value to write.

        Returns:
            int: the number of bytes written.
        """
        return self.pack('c', value)

    def write_float(self, value, little_endian=True):
        """
        Pack the value as a float and write 4 bytes to the stream.

        Args:
            value (number): the value to write to the stream.
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sf' % endian, value)

    def write_double(self, value, little_endian=True):
        """
        Pack the value as a double and write 8 bytes to the stream.

        Args:
            value (number): the value to write to the stream.
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sd' % endian, value)

    def write_int8(self, value, little_endian=True):
        """
        Pack the value as a signed byte and write 1 byte to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sb' % endian, value)

    def write_uint8(self, value, little_endian=True):
        """
        Pack the value as an unsigned byte and write 1 byte to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sB' % endian, value)

    def write_bool(self, value):
        """
        Pack the value as a bool and write 1 byte to the stream.

        Args:
            value: the boolean value to write.

        Returns:
            int: the number of bytes written.
        """
        return self.pack('?', value)

    def write_int16(self, value, little_endian=True):
        """
        Pack the value as a signed integer and write 2 bytes to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sh' % endian, value)

    def write_uint16(self, value, little_endian=True):
        """
        Pack the value as an unsigned integer and write 2 bytes to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sH' % endian, value)

    def write_int32(self, value, little_endian=True):
        """
        Pack the value as a signed integer and write 4 bytes to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%si' % endian, value)

    def write_uint32(self, value, little_endian=True):
        """
        Pack the value as an unsigned integer and write 4 bytes to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sI' % endian, value)

    def write_int64(self, value, little_endian=True):
        """
        Pack the value as a signed integer and write 8 bytes to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sq' % endian, value)

    def write_uint64(self, value, little_endian=True):
        """
        Pack the value as an unsigned integer and write 8 bytes to the stream.

        Args:
            value:
            little_endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"
        return self.pack('%sQ' % endian, value)

    def write_var_int(self, value, little_endian=True):
        """
        Write an integer value in a space saving way to the stream.

        Args:
            value (int):
            little_endian (bool): specify the endianness. (Default) Little endian.

        Raises:
            SDKException: if `value` is not of type int.
            SDKException: if `value` is < 0.

        Returns:
            int: the number of bytes written.
        """
        if little_endian:
            endian = "<"
        else:
            endian = ">"

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

    def write_var_bytes(self, value, little_endian=True):
        """
        Write an integer value in a space saving way to the stream.

        Args:
            value (bytes):
            little_endian=endian (bool): specify the endianness. (Default) Little endian.

        Returns:
            int: the number of bytes written.
        """
        length = len(value)
        self.write_var_int(length, little_endian)

        return self.write_bytes(value, unhex=False)

    def write_var_str(self, value, encoding="utf-8"):
        """
        Write a string value to the stream.

        Args:
            value (string): value to write to the stream.
            encoding (str): string encoding format.
        """
        if type(value) is str:
            value = value.encode(encoding)

        length = len(value)
        ba = bytearray(value)
        byts = binascii.hexlify(ba)
        string = byts.decode(encoding)
        self.write_var_int(length)
        self.write_bytes(string)

    def write_fixed_str(self, value, length):
        """
        Write a string value to the stream.

        Args:
            value (str): value to write to the stream.
            length (int): length of the string to write.
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

        Args:
            array(list): a list of serializable objects. i.e. extending neo.IO.Mixins.SerializableMixin
        """
        if array is None:
            self.write_byte(0)
        else:
            self.write_var_int(len(array))
            for item in array:
                item.Serialize(self)

    def write_2000256_list(self, arr):
        """
        Write an array of 64 byte items to the stream.

        Args:
            arr (list): a list of 2000 items of 64 bytes in size.
        """
        for item in arr:
            ba = bytearray(binascii.unhexlify(item))
            ba.reverse()
            self.write_bytes(ba)

    def write_hashes(self, arr):
        """
        Write an array of hashes to the stream.

        Args:
            arr (list): a list of 32 byte hashes.
        """
        length = len(arr)
        self.write_var_int(length)
        for item in arr:
            ba = bytearray(binascii.unhexlify(item))
            ba.reverse()
            #            logger.info("WRITING HASH %s " % ba)
            self.write_bytes(ba)

    def write_fixed8(self, value, unsigned=False):
        """
        Write a Fixed8 value to the stream.

        Args:
            value (neo.Fixed8):
            unsigned: (Not used)

        Returns:
            int: the number of bytes written
        """
        #        if unsigned:
        #            return self.write_uint64(int(value.value))
        return self.write_int64(value.value)
