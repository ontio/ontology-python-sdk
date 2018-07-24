from ontology.utils.util import get_asset_address
from ontology.vm.build_vm import build_native_invoke_code
from time import time
from ontology.core.transaction import Transaction


def new_transfer_transaction(gas_price, gas_limit, asset, from_addr, to_addr, amount):
    contract_address = get_asset_address(asset)  # []bytes
    state = [{"from": from_addr, "to": to_addr, "amount": amount}]
    invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transfer", state)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, bytearray(), invoke_code, bytearray(),
                       [], bytearray())
