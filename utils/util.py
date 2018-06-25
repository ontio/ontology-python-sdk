import hashlib
import os.path
from common import address
from common import define


def print_byte_array(barray):
    for i in range(len(barray)):
        print(barray[i], end=' ')


def address_from_vm_code(code):
    '''
    :param code: []byte
    :return: [20]byte
    '''
    m = hashlib.sha256()
    m.update(code)
    temp = m.digest()
    h = hashlib.new('ripemd160')
    h.update(temp)
    return h.digest()


def get_contract_address(contract_code):
    '''
    :param contract_code: string
    :return: [20]byte
    '''
    code = bytearray.fromhex(contract_code)
    return address_from_vm_code(code)


def get_asset_address(asset):
    '''
    :param asset: string
    :return: [20]byte
    '''
    if asset.upper() == 'ONT':
        contract_address = address.ont_contract_address
    elif asset.upper() == 'ONG':
        contract_address = address.ong_contract_address
    else:
        raise ValueError("asset is not equal to ONT or ONG")
    return contract_address


def is_file_exist(file_path):
    '''
    :param file_path: string
    :return: True / False
    '''
    return os.path.isfile(file_path) or os.path.isdir(file_path)


def parse_pre_exec_result(return_value, return_type):
    '''
    :param return_value:
    :param return_type: must be one of NeoVMReturnType
    :return:
    '''
    if type(return_type)==int and return_type >= 1 and return_type <= 4:
        res = parse_neo_vm_contract_return_type(return_value, return_type)
    elif return_type:
        # TODO: maybe have some errors here
        if len(return_value)!=len(return_type):
            raise ValueError("return type unmatch")
    else:
        raise ValueError("invalid return type")
    return res



def parse_neo_vm_contract_return_type(value, return_type):
    if return_type == define.NEOVM_TYPE_BOOL:
        return parse_neo_vm_contract_return_type_bool(value)
    elif return_type == define.NEOVM_TYPE_INTEGER:
        return parse_neo_vm_contract_return_type_integer(value)
    elif return_type == define.NEOVM_TYPE_STRING:
        return parse_neo_vm_contract_return_type_string(value)
    elif return_type == define.NEOVM_TYPE_BYTE_ARRAY:
        return parse_neo_vm_contract_return_type_bytearray(value)
    else:
        raise ValueError("unknown return type")


def parse_neo_vm_contract_return_type_bool(value):
    if type(value) == str:
        return value == "01"
    else:
        raise ValueError("false, asset to string failed")


def parse_neo_vm_contract_return_type_integer(value):
    if type(value) == str:
        data = bytearray.fromhex(value)
        return int.from_bytes(data, byteorder='little', signed=False)
    else:
        raise ValueError("false, asset to string failed")


def parse_neo_vm_contract_return_type_bytearray(value):
    if type(value) == str:
        data = bytearray.fromhex(value)
        return data
    else:
        raise ValueError("false, asset to string failed")


def parse_neo_vm_contract_return_type_string(value):
    data = parse_neo_vm_contract_return_type_bytearray(value)
    return data.decode()


def bytes_reverse(data):
    '''
    :param data: must be bytearray
    :return: bytearray.reverse()
    '''
    return data.reverse()


if __name__ == '__main__':
    res = parse_neo_vm_contract_return_type_integer("1234")
    print(res)
