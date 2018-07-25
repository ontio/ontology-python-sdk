from time import time
from ontology.utils import util
from ontology.vm import build_vm
from ontology.core.transaction import Transaction, Sig
from ontology.account.account import Account
from ontology.crypto.KeyType import KeyType
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.common.address import ont_id_contract_address

def new_registry_ontid_transaction(ontid,pubkey,gas_limit,gas_price):
    contract_address = ont_id_contract_address # []bytes
    args = {"ontid": ontid.encode(), "pubkey": pubkey}
    invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "regIDWithPublicKey", args)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, bytearray(), invoke_code, bytearray(),
                       [], bytearray())

def new_get_ddo_transaction(ontid:str):
    contract_address = ont_id_contract_address # []bytes
    args = {"ontid": ontid.encode()}
    invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "getDDO", args)
    unix_timenow = int(time())
    return Transaction(0, 0xd1, unix_timenow, 0, 0, bytearray(), invoke_code, bytearray(),
                       [], bytearray())