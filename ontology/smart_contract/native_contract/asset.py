
from ontology.vm.build_vm import build_native_invoke_code,build_neo_vm_param
from time import time
from ontology.core.transaction import Transaction
from ontology.vm.params_builder import ParamsBuilder
from binascii import b2a_hex, a2b_hex
from ontology.common.address import Address
from ontology.vm.params_builder import ParamsBuilder
from ontology.vm.op_code import *
from ontology.common.define import *


def get_asset_address(asset: str) -> bytearray:
    if asset.upper() == 'ONT':
        contract_address = ONT_CONTRACT_ADDRESS
    elif asset.upper() == 'ONG':
        contract_address = ONG_CONTRACT_ADDRESS
    else:
        raise ValueError("asset is not equal to ONT or ONG")
    return contract_address  # [20]byte


def new_transfer_transaction( asset:str, from_addr :str, to_addr :str, amount :int, payer: str, gas_limit:int,gas_price:int):
    contract_address = get_asset_address(asset)  # []bytes
    state = [{"from": Address.decodeBase58(from_addr).to_array(), "to": Address.decodeBase58(to_addr).to_array(), "amount": amount}]
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transfer", state)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                       [], bytearray())


def new_get_balance_transaction(asset: str, addr:str):
    contract_address = get_asset_address(asset)
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "balanceOf", Address.decodeBase58(addr).to_array())
    unix_timenow = int(time())
    payer = Address(a2b_hex("0000000000000000000000000000000000000000".encode())).to_array()
    return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(),
                       [], bytearray())


def new_get_allowance_transaction(asset: str, from_addr:str, to_addr:str):
    contract_address = get_asset_address(asset)
    args = {"from": Address.decodeBase58(from_addr).to_array(), "to": Address.decodeBase58(to_addr).to_array()}
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "allowance", args)
    unix_timenow = int(time())
    payer = Address(a2b_hex("0000000000000000000000000000000000000000".encode())).to_array()
    return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(), [], bytearray())


def unboundong(cli, addr:str):
    return cli.get_allowance(addr)


def new_get_name_transaction(asset: str):
    contract_address = get_asset_address(asset)
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "name", bytearray())
    unix_timenow = int(time())
    payer = Address(a2b_hex("0000000000000000000000000000000000000000".encode())).to_array()
    return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(), [], bytearray())


def new_get_symbol_transaction(asset: str):
    contract_address = get_asset_address(asset)
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "symbol", bytearray())
    unix_timenow = int(time())
    payer = Address(a2b_hex("0000000000000000000000000000000000000000".encode())).to_array()
    return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(), [], bytearray())


def new_get_decimals_transaction(asset: str):
    contract_address = get_asset_address(asset)
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "decimals", bytearray())
    unix_timenow = int(time())
    payer = Address(a2b_hex("0000000000000000000000000000000000000000".encode())).to_array()
    return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(), [], bytearray())


def new_withdraw_ong_transaction(claimer_addr :str, recv_addr :str, amount :int, payer: str, gas_limit :int, gas_price :int):
    ont_contract_address = get_asset_address("ont")
    ong_contract_address = get_asset_address("ong")
    args = {"sender": Address.decodeBase58(claimer_addr).to_array(), "from": ont_contract_address, "to": Address.decodeBase58(recv_addr).to_array(),
             "value": amount}
    invoke_code = build_native_invoke_code(ong_contract_address, bytes([0]), "transferFrom", args)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                       [], bytearray())


def new_approve_transaction(asset: str, send_addr:str, recv_addr:str, amount:int, payer: str, gas_limit:int, gas_price:int):
    contract_address = get_asset_address(asset)  # []bytes
    args = {"from": Address.decodeBase58(send_addr).to_array(), "to": Address.decodeBase58(recv_addr).to_array(), "amount": amount}
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "approve", args)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                       [], bytearray())


def new_transferfrom_transaction(asset: str, send_addr:str, from_addr:str, recv_addr:str, amount:int, payer: str, gas_limit:int, gas_price:int):
    contract_address = get_asset_address(asset)  # []bytes
    args = {"sender": Address.decodeBase58(send_addr).to_array(), "from": Address.decodeBase58(from_addr).to_array(), "to": Address.decodeBase58(recv_addr).to_array(),
                                                                                                                   "amount": amount}
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transferFrom", args)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                       [], bytearray())