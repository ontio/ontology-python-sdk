import hashlib
import os.path
from ontology.common import address
from ontology.common.define import *


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


def address_from_vm_code(code: bytearray) -> bytearray:
    m = hashlib.sha256()
    m.update(code)
    temp = m.digest()
    h = hashlib.new('ripemd160')
    h.update(temp)
    return h.digest()  # [20]byte


def get_contract_address(contract_code: str) -> bytearray:
    code = bytearray.fromhex(contract_code)
    return address_from_vm_code(code)  # [20]byte


def get_asset_address(asset: str) -> bytearray:
    if asset.upper() == 'ONT':
        contract_address = address.ont_contract_address
    elif asset.upper() == 'ONG':
        contract_address = address.ong_contract_address
    else:
        raise ValueError("asset is not equal to ONT or ONG")
    return contract_address  # [20]byte


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


def print_byte_array(byte_array):
    for i in range(len(byte_array)):
        print(byte_array[i], end=' ')
    print()


def print_byte_content(byte_array):
    for i in range(len(byte_array)):
        print(chr(byte_array[i]), end='')


def add_comma(l):
    res = "["
    for i in l:
        if i == "[" or i == "]":
            continue
        elif i == " ":
            res += ", "
        else:
            res += i
    return res + ']'


def bytes_reader(b):
    res = bytearray()
    for i in range(len(b) // 2):
        res += bytearray.fromhex(b[2 * i:2 * i + 2].decode())
    return res
