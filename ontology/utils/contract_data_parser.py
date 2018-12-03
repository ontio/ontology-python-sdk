#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from ontology.common.address import Address
from ontology.common.error_code import ErrorCode
from ontology.exception.exception import SDKException


class ContractDataParser(object):
    @staticmethod
    def to_int(hex_str: str) -> int:
        array = bytearray(binascii.a2b_hex(hex_str.encode('ascii')))
        array.reverse()
        num = int(binascii.b2a_hex(array).decode('ascii'), 16)
        return num

    @staticmethod
    def to_utf8_str(hex_str: str) -> str:
        utf8_str = bytes.fromhex(hex_str).decode('utf-8')
        return utf8_str

    @staticmethod
    def to_b58_address(hex_address: str) -> str:
        try:
            bytes_address = binascii.a2b_hex(hex_address)
        except binascii.Error as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        address = Address(bytes_address)
        return address.b58encode()
