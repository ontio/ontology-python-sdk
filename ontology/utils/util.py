#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import os.path
from Cryptodome import Random

from ontology.common.define import *


def get_asset_address(asset: str) -> bytearray:
    if asset.upper() == 'ONT':
        contract_address = ONT_CONTRACT_ADDRESS
    elif asset.upper() == 'ONG':
        contract_address = ONG_CONTRACT_ADDRESS
    else:
        raise ValueError("asset is not equal to ONT or ONG")
    return contract_address  # [20]byte


def get_random_bytes(length):
    return Random.get_random_bytes(length)


def get_random_str(length):
    return Random.get_random_bytes(length).hex()[:length]


def hex_to_bytes(value: str) -> bytearray:
    return bytearray.fromhex(value)


def to_array_reverse(arr: bytearray) -> bytearray:
    bytearray.reverse(arr)
    return arr


def uint256_parse_from_bytes(f: bytearray) -> bytearray:
    if len(f) != UINT256_SIZE:
        raise ValueError("[util]: uint256_parse_from_bytes err, len != 32")
    return f


def uint256_from_hex_string(s: str) -> bytearray:
    hx = hex_to_bytes(s)
    return uint256_parse_from_bytes(to_array_reverse(hx))


def is_file_exist(file_path: str) -> bool:
    return os.path.isfile(file_path)


def parse_pre_exec_result(return_value, return_type):
    if isinstance(return_type, int) and return_type >= 1 and return_type <= 4:
        res = parse_neo_vm_contract_return_type(return_value, return_type)
    elif isinstance(return_type, list):
        if len(return_value) != len(return_type):
            raise ValueError("the length of return_value and return_type unmatch")
        res = []
        for i in range(len(return_type)):
            r_value = parse_pre_exec_result(return_value[i], return_type[i])
            res.append(r_value)
    else:
        raise ValueError("invalid return type")
    return res


def parse_neo_vm_contract_return_type(value, return_type):
    if return_type == NEOVM_TYPE_BOOL:
        return parse_neo_vm_contract_return_type_bool(value)
    elif return_type == NEOVM_TYPE_INTEGER:
        return parse_neo_vm_contract_return_type_integer(value)
    elif return_type == NEOVM_TYPE_STRING:
        return parse_neo_vm_contract_return_type_string(value)
    elif return_type == NEOVM_TYPE_BYTE_ARRAY:
        return parse_neo_vm_contract_return_type_bytearray(value)
    else:
        raise ValueError("unknown return type")


def parse_neo_vm_contract_return_type_bool(value) -> bool:
    if type(value) == str:
        return value == "01"
    else:
        raise ValueError("false, asset to string failed")


def parse_neo_vm_contract_return_type_integer(value) -> int:
    if type(value) == str:
        data = bytearray.fromhex(value)
        return int.from_bytes(data, byteorder='little', signed=False)
    else:
        raise ValueError("false, asset to string failed")


def parse_neo_vm_contract_return_type_bytearray(value) -> bytearray:
    if type(value) == str:
        data = bytearray.fromhex(value)
        return data
    else:
        raise ValueError("false, asset to string failed")


def parse_neo_vm_contract_return_type_string(value) -> str:
    data = parse_neo_vm_contract_return_type_bytearray(value)
    return data.decode()


def bytes_reverse(data: bytearray) -> bytearray:
    data.reverse()
    return data


def bytes_reader(b):
    res = bytearray()
    for i in range(len(b) // 2):
        res += bytearray.fromhex(b[2 * i:2 * i + 2].decode())
    return res


def bigint_to_neo_bytes(data: int):
    data_bytes = int_to_bytearray(data)
    if len(data_bytes) == 0:
        return bytearray()
    b = data_bytes[0]
    if data < 0:
        for i in len(data_bytes):
            data_bytes[i] = ~b
        temp = int.from_bytes(data_bytes, "little")
        temp2 = temp + 1
        bs = int_to_bytearray(temp2)
        if b >> 7 == 1:
            res = bs[:] + bytearray([255])
            return res
        return bs
    else:
        if b >> 7 == 1:
            res = data_bytes[:] + bytearray([0])
            return res
        return data_bytes


def int_to_bytearray(data: int):
    bit_length = data.bit_length() // 8
    t = data.bit_length() / 8
    if bit_length < t:
        bit_length += 1
    data_bytes = data.to_bytes(bit_length, "little")
    return bytearray(data_bytes)
