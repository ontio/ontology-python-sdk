from unittest import TestCase
from binascii import a2b_hex
from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.native_contract.asset import Asset
from ontology.utils.util import get_random_bytes

rpc_address = "http://polaris1.ont.io:20336"
sdk = OntologySdk.get_instance()
sdk.rpc.set_address(rpc_address)


class TestRpcClient(TestCase):
    def test_get_version(self):
        res = sdk.rpc.get_version()
        print(res)

    def test_get_block_by_hash(self):
        res = sdk.rpc.get_block_by_hash("44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c")
        print(res)

    def test_get_block_by_height(self):
        res = sdk.rpc.get_block_by_hash(0)
        print(res)

    def test_get_block_count(self):
        res = sdk.rpc.get_block_count()
        print(res)

    def test_get_current_block_hash(self):
        res = sdk.rpc.get_current_block_hash()
        print(res)

    def test_get_block_hash_by_height(self):
        res = sdk.rpc.get_block_hash_by_height(0)
        print(res)

    def test_get_balance(self):
        s = "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"
        res = sdk.rpc.get_balance(s)
        print(res)

    def test_get_allowance(self):
        private_key = '99bbd375c745088b372c6fc2ab38e2fb6626bc552a9da47fc3d76baa21537a1c'
        scheme = SignatureScheme.SHA256withECDSA
        acct = Account(a2b_hex(private_key.encode()), scheme)
        res = sdk.rpc.get_allowance(acct.get_address().to_base58())
        print(res)

    def test_get_storage(self):
        addr = "0100000000000000000000000000000000000000"
        key = "746f74616c537570706c79"
        res = sdk.rpc.get_storage(addr, key)
        print(res)

    def test_get_smart_contract_event_by_txhash(self):
        s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        res = sdk.rpc.get_smart_contract_event_by_txhash(s)
        print(res)

    def test_get_smart_contract_event_by_block(self):
        s = 0
        res = sdk.rpc.get_smart_contract_event_by_block(s)
        print(res)

    def test_get_raw_transaction(self):
        s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        res = sdk.rpc.get_raw_transaction(s)
        print(res)

    def test_get_smart_contract(self):
        s = "0239dcf9b4a46f15c5f23f20d52fac916a0bac0d"
        res = sdk.rpc.get_smart_contract(s)
        print(res)

    def test_get_generate_block_time(self):
        res = sdk.rpc.get_generate_block_time()
        print(res)

    def test_get_merkle_proof(self):
        s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        res = sdk.rpc.get_merkle_proof(s)
        print(res)

    def test_send_raw_transaction(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(a2b_hex(private_key.encode()))
        private_key2 = get_random_bytes(32)
        acct2 = Account(private_key2)
        tx = Asset.new_transfer_transaction("ont", acct.get_address().to_base58(),
                                            acct2.get_address().to_base58(), 2, 20000, 500)
        tx = sdk.sign_transaction(tx, acct)
        res = sdk.rpc.send_raw_transaction(tx)
        print(res)

    def test_send_raw_transaction_preexec(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(a2b_hex(private_key.encode()))
        private_key2 = get_random_bytes(32)
        acct2 = Account(private_key2)
        tx = Asset.new_transfer_transaction("ont", acct.get_address().to_base58(),
                                            acct2.get_address().to_base58(), 2, 20000, 500)
        tx = sdk.sign_transaction(tx, acct)
        res = sdk.rpc.send_raw_transaction_preexec(tx)
        print(res)
