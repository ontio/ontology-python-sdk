#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from typing import List

from ontology.common.address import Address
from ontology.common.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.io.binary_reader import BinaryReader
from ontology.io.memory_stream import StreamManager
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_contract.abi.struct_type import Struct


class ContractDataParser(object):
    @staticmethod
    def to_bool(hex_str) -> bool:
        if len(hex_str) != 2:
            raise SDKException(ErrorCode.other_error('invalid str'))
        return bool(hex_str)

    @staticmethod
    def to_int(hex_str: str) -> int:
        try:
            array = bytearray(binascii.a2b_hex(hex_str.encode('ascii')))
        except binascii.Error as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        array.reverse()
        num = int(binascii.b2a_hex(array).decode('ascii'), 16)
        return num

    @staticmethod
    def to_int_list(hex_str_list: list) -> List[int]:
        for index in range(len(hex_str_list)):
            item = hex_str_list[index]
            if isinstance(item, list):
                hex_str_list[index] = ContractDataParser.to_int_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = ContractDataParser.to_int(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_bytes(hex_str: str) -> bytes:
        try:
            bytes_str = binascii.a2b_hex(hex_str)
        except binascii.Error as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        return bytes_str

    @staticmethod
    def to_bytes_list(hex_str_list: list) -> List[bytes]:
        for index in range(len(hex_str_list)):
            item = hex_str_list[index]
            if isinstance(item, list):
                hex_str_list[index] = ContractDataParser.to_bytes_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = ContractDataParser.to_bytes(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_utf8_str(hex_str: str) -> str:
        try:
            utf8_str = binascii.a2b_hex(hex_str)
            utf8_str = utf8_str.decode('utf-8')
        except (ValueError, binascii.Error)as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        return utf8_str

    @staticmethod
    def to_utf8_str_list(hex_str_list: list) -> List[bytes]:
        for index in range(len(hex_str_list)):
            item = hex_str_list[index]
            if isinstance(item, list):
                hex_str_list[index] = ContractDataParser.to_utf8_str_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = ContractDataParser.to_utf8_str(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_b58_address(hex_address: str) -> str:
        try:
            bytes_address = binascii.a2b_hex(hex_address)
        except binascii.Error as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        address = Address(bytes_address)
        return address.b58encode()

    @staticmethod
    def to_b58_address_list(hex_str_list: list) -> List[bytes]:
        for index in range(len(hex_str_list)):
            item = hex_str_list[index]
            if isinstance(item, list):
                hex_str_list[index] = ContractDataParser.to_b58_address_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = ContractDataParser.to_b58_address(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_bytes_address(hex_address: str) -> bytes:
        try:
            bytes_address = binascii.a2b_hex(hex_address)
        except binascii.Error as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        address = Address(bytes_address)
        return address.to_bytes()

    @staticmethod
    def to_bytes_address_list(hex_str_list: list) -> List[bytes]:
        for index in range(len(hex_str_list)):
            item = hex_str_list[index]
            if isinstance(item, list):
                hex_str_list[index] = ContractDataParser.to_bytes_address_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = ContractDataParser.to_bytes_address(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_dict(item_serialize: str):
        stream = StreamManager.GetStream(bytearray.fromhex(item_serialize))
        reader = BinaryReader(stream)
        return ContractDataParser.__deserialize_stack_item(reader)

    @staticmethod
    def __deserialize_stack_item(reader: BinaryReader):
        t = reader.read_byte()
        if t == BuildParams.Type.bytearray_type.value:
            b = reader.read_var_bytes()
            return b
        elif t == BuildParams.Type.bool_type.value:
            return reader.read_bool()
        elif t == BuildParams.Type.int_type.value:
            b = reader.read_var_bytes()
            return ContractDataParser.__big_int_from_bytes(bytearray(b))
        elif t == BuildParams.Type.struct_type.value or t == BuildParams.Type.array_type.value:
            count = reader.read_var_int()
            item_list = list()
            for i in range(count):
                item = ContractDataParser.__deserialize_stack_item(reader)
                item_list.append(item)
            if t == BuildParams.Type.struct_type.value:
                return Struct(item_list)
            return item_list
        elif t == BuildParams.Type.dict_type.value:
            count = reader.read_var_int()
            item_dict = dict()
            for i in range(count):
                key = ContractDataParser.__deserialize_stack_item(reader)
                value = ContractDataParser.__deserialize_stack_item(reader)
                item_dict[key] = value
            return item_dict
        else:
            raise SDKException(ErrorCode.other_error('type error'))

    @staticmethod
    def __big_int_from_bytes(ba: bytearray):
        if len(ba) == 0:
            return 0
        ba_temp = ba[:]
        ba_temp.reverse()
        if ba_temp[0] >> 7 == 1:
            res = int.from_bytes(ba_temp, 'big', signed=True)
            return res
        return int.from_bytes(ba_temp, 'big', signed=True)
