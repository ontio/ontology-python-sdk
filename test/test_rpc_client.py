#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import a2b_hex
import unittest

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.native_contract.asset import Asset
from ontology.utils.util import get_random_bytes

sdk = OntologySdk()
rpc_address = "http://polaris3.ont.io:20336"
sdk.rpc.set_address(rpc_address)
private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
acc = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acc2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
acc3 = Account(a2b_hex(private_key3.encode()), SignatureScheme.SHA256withECDSA)
pubkeys = [acc.get_public_key(), acc2.get_public_key(), acc3.get_public_key()]
multi_addr = Address.address_from_multi_pubKeys(2, pubkeys)


class TestRpcClient(unittest.TestCase):
    def test_get_version(self):
        res = sdk.rpc.get_version()
        self.assertEqual("v1.0.1", res)

    def test_get_block_by_hash(self):
        hash = "44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c"
        res = sdk.rpc.get_block_by_hash(hash)
        self.assertEqual(res['Hash'], hash)

    def test_get_block_by_height(self):
        height = 0
        res = sdk.rpc.get_block_by_hash(height)
        self.assertEqual(res['Header']['Height'], height)

    def test_get_block_count(self):
        res = sdk.rpc.get_block_count()
        self.assertGreater(res, 103712)

    def test_get_current_block_hash(self):
        res = sdk.rpc.get_current_block_hash()
        self.assertEqual(len(res), 64)

    def test_get_block_hash_by_height(self):
        res = sdk.rpc.get_block_hash_by_height(0)
        self.assertEqual(len(res), 64)

    def test_get_balance(self):
        s = "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"
        address_balance = sdk.rpc.get_balance(s)
        try:
            address_balance['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            address_balance['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

    def test_get_balance_by_acc(self):
        address_balance = sdk.rpc.get_balance(acc.get_address_base58())
        try:
            address_balance['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            address_balance['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        multi_address_balance = sdk.rpc.get_balance(multi_addr.to_base58())
        try:
            multi_address_balance['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            multi_address_balance['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

    def test_get_allowance(self):
        private_key = '99bbd375c745088b372c6fc2ab38e2fb6626bc552a9da47fc3d76baa21537a1c'
        scheme = SignatureScheme.SHA256withECDSA
        acct = Account(a2b_hex(private_key.encode()), scheme)
        res = sdk.rpc.get_allowance(acct.get_address_base58())
        self.assertEqual(res, '0')

    def test_get_storage(self):
        addr = "0100000000000000000000000000000000000000"
        key = "746f74616c537570706c79"
        res = sdk.rpc.get_storage(addr, key)
        self.assertEqual(res, 1000000000)

    def test_get_smart_contract_event_by_txhash(self):
        s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        res = sdk.rpc.get_smart_contract_event_by_txhash(s)
        self.assertEquals(res['TxHash'], s)

    def test_get_smart_contract_event_by_block(self):
        b = 0
        res = sdk.rpc.get_smart_contract_event_by_block(b)
        self.assertEqual(res[0]['State'], 1)

    def test_get_raw_transaction(self):
        hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        res = sdk.rpc.get_raw_transaction(hash)
        self.assertEqual(res['Hash'], hash)

    def test_get_smart_contract(self):
        s = "0239dcf9b4a46f15c5f23f20d52fac916a0bac0d"
        res = sdk.rpc.get_smart_contract(s)
        self.assertEqual(res['Description'], 'Ontology Network ONT Token')

    def test_get_merkle_proof(self):
        s = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        res = sdk.rpc.get_merkle_proof(s)
        self.assertEqual(res['Type'], 'MerkleProof')

    def test_send_raw_transaction(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(a2b_hex(private_key.encode()))
        private_key2 = get_random_bytes(32)
        acct2 = Account(private_key2)
        tx = Asset.new_transfer_transaction("ont", acct.get_address_base58(),
                                            acct2.get_address_base58(), 2, acct.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acct)
        res = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(len(res), 64)

    def test_send_raw_transaction_preexec(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(a2b_hex(private_key.encode()))
        private_key2 = get_random_bytes(32)
        acct2 = Account(private_key2)
        tx = Asset.new_transfer_transaction("ont", acct.get_address().to_base58(),
                                            acct2.get_address().to_base58(), 2, acct.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acct)
        res = sdk.rpc.send_raw_transaction_preexec(tx)
        self.assertEqual(res, '01')


if __name__ == '__main__':
    unittest.main()
