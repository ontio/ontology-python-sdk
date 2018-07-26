from ontology.utils.util import get_asset_address
from ontology.vm.build_vm import build_native_invoke_code
from time import time
from ontology.core.transaction import Transaction
from ontology.vm.params_builder import ParamsBuilder
from binascii import b2a_hex, a2b_hex
from ontology.common.address import Address

def new_transfer_transaction( asset:str, from_addr :str, to_addr :str, amount :int, gas_limit:int,gas_price:int):
    contract_address = get_asset_address(asset)  # []bytes
    state = [{"from": Address.decodeBase58(from_addr).to_array(), "to": Address.decodeBase58(to_addr).to_array(), "amount": amount}]
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transfer", state)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, bytearray(), invoke_code, bytearray(),
                       [], bytearray())

def new_get_balance_transaction(asset, addr:str):
    contract_address = get_asset_address(asset)
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "balanceOf", Address.decodeBase58(addr).to_array())
    unix_timenow = int(time())
    payer = Address("0000000000000000000000000000000000000000").to_array()
    return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(),
                       [], bytearray())