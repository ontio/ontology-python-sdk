from ontology.utils import util
from ontology.account import client
from ontology.rpc import rpc
from ontology.rest import rest_client
from ontology.ont_sdk import OntologySdk
import json

rpc_address = "http://polaris1.ont.io:20336"
sdk = OntologySdk()
sdk.rpc_client.set_address(rpc_address)


def test_get_version():
    res = sdk.rpc_client.get_version()
    print(res)


def test_get_block_by_hash():
    res = sdk.rpc_client.get_block_by_hash("44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c")
    # the first output method
    print(res)


def test_get_block_by_height():
    res = sdk.rpc_client.get_block_by_hash(27893)
    print(res)


def test_get_block_count():
    res = sdk.rpc_client.get_block_count()
    print(res)


def test_get_current_block_hash():
    res = sdk.rpc_client.get_current_block_hash()
    print(res)


def test_get_block_hash_by_height(height):
    res = sdk.rpc_client.get_block_hash_by_height(height)
    print(res)


def test_smart_contract_event():
    s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
    res = sdk.rpc_client.get_smart_contract_event_by_txhash(s)
    print(res)


def test_smart_contract_event_by_block():
    s = 0
    res = sdk.rpc_client.get_smart_contract_event_by_block(s)
    print(res)


def test_get_raw_transaction():
    s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
    res = sdk.rpc_client.get_raw_transaction(s)
    print(res)


def test_get_smart_contract():
    s = "0239dcf9b4a46f15c5f23f20d52fac916a0bac0d"
    res = sdk.rpc_client.get_smart_contract(s)
    print(res)


def test_get_generate_block_time():
    res = sdk.rpc_client.get_generate_block_time()
    print(res)


def test_get_merkle_proof():
    s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
    res = sdk.rpc_client.get_merkle_proof(s)
    print(res)


def test_get_balance():
    s = "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"
    res = sdk.rpc_client.get_balance(s)
    print(res)


def test_get_storage():
    addr = "0100000000000000000000000000000000000000"
    key = "746f74616c537570706c79"
    res = sdk.rpc_client.get_storage(addr, key)
    print(res)


def test_new_transfer_transaction():
    gas_price = 0
    gas_limit = 0
    asset = "ont"
    from_addr = ""
    to_addr = ""
    amount = 1
    res = sdk.rpc_client.new_transfer_transaction(gas_price, gas_limit, asset, from_addr, to_addr, amount)
    print(res)


s = "transfer"
print(s.encode())
util.print_byte_array(s.encode())