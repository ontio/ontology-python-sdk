#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.native_contract.asset import Asset
from ontology.utils import util

rpc_address = "http://polaris3.ont.io:20336"
sdk = OntologySdk()
sdk.rpc.set_address(rpc_address)


class TestAsset(unittest.TestCase):
    def test_get_asset_address(self):
        asset = sdk.native_vm().asset()
        ont_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        ong_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
        self.assertEqual(ont_address, asset.get_asset_address('ont'))
        self.assertEqual(ong_address, asset.get_asset_address('ong'))

    def test_query_name(self):
        asset = sdk.native_vm().asset()
        token_name = asset.query_name('ont')
        self.assertEqual('ONT Token', token_name)
        token_name = asset.query_name('ong')
        self.assertEqual('ONG Token', token_name)

    def test_query_symbol(self):
        asset = sdk.native_vm().asset()
        token_symbol = asset.query_symbol('ont')
        self.assertEqual('ONT', token_symbol)
        token_symbol = asset.query_symbol('ong')
        self.assertEqual('ONG', token_symbol)

    def test_query_decimals(self):
        asset = sdk.native_vm().asset()
        decimals = asset.query_decimals('ong')
        self.assertEqual(9, decimals)
        decimals = asset.query_decimals('ont')
        self.assertEqual(1, decimals)

    def test_query_balance(self):
        asset = Asset(sdk)
        private_key = util.get_random_str(64)
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_address = acct.get_address_base58()
        balance = asset.query_balance('ont', b58_address)
        self.assertTrue(isinstance(balance, int))
        self.assertGreaterEqual(balance, 0)
        balance = asset.query_balance('ong', b58_address)
        self.assertTrue(isinstance(balance, int))
        self.assertGreaterEqual(balance, 0)

    def test_query_allowance(self):
        asset = sdk.native_vm().asset()
        b58_from_address = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6'
        b58_to_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        allowance = asset.query_allowance("ont", b58_from_address, b58_to_address)
        self.assertEqual(1, allowance)

    def test_new_transfer_transaction(self):
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        acc = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)

        balance_1 = sdk.rpc.get_balance(acc.get_address_base58())
        balance_2 = sdk.rpc.get_balance(acc2.get_address_base58())

        old_ont_balance_1 = 0
        old_ont_balance_2 = 0
        old_ong_balance_1 = 0
        old_ong_balance_2 = 0
        try:
            old_ont_balance_1 = balance_1['ont']
            old_ont_balance_2 = balance_2['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            old_ong_balance_1 = balance_1['ong']
            old_ong_balance_2 = balance_2['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        gas_limit = 20000
        gas_price = 500
        gas = 20000 * 500
        tx = sdk.native_vm().asset().new_transfer_transaction("ont", acc.get_address_base58(),
                                                              acc2.get_address_base58(), 1, acc2.get_address_base58(),
                                                              gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, acc)
        tx = sdk.add_sign_transaction(tx, acc2)
        sdk.rpc.send_raw_transaction(tx)

        time.sleep(6)
        balance_1 = sdk.rpc.get_balance(acc.get_address_base58())
        balance_2 = sdk.rpc.get_balance(acc2.get_address_base58())

        new_ont_balance_1 = 0
        new_ont_balance_2 = 0
        new_ong_balance_1 = 0
        new_ong_balance_2 = 0
        try:
            new_ont_balance_1 = balance_1['ont']
            new_ont_balance_2 = balance_2['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            new_ong_balance_1 = balance_1['ong']
            new_ong_balance_2 = balance_2['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        self.assertEqual(int(old_ont_balance_1) - 1, int(new_ont_balance_1))
        self.assertEqual(int(old_ont_balance_2) + 1, int(new_ont_balance_2))
        self.assertEqual(int(old_ong_balance_1), int(new_ong_balance_1))
        self.assertEqual((int(old_ong_balance_2) - int(new_ong_balance_2)), gas)

    def test_send_transfer(self):
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
        acc = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
        print(sdk.native_vm().asset().query_balance("ont", acc.get_address_base58()))
        print(sdk.native_vm().asset().query_balance("ont", acc3.get_address_base58()))
        txhash = sdk.native_vm().asset().send_transfer("ont", acc, acc3.get_address_base58(), 100, acc, 20000, 500)
        time.sleep(6)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))
        print(sdk.native_vm().asset().query_balance("ont", acc.get_address_base58()))
        print(sdk.native_vm().asset().query_balance("ont", acc3.get_address_base58()))

    def test_send_withdraw_ong_transaction(self):
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
        acc = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
        asset = sdk.native_vm().asset()
        res = asset.send_withdraw_ong_transaction(acc, acc2.get_address_base58(), 1, acc3, 20000, 500)
        self.assertEqual(res, '01')

    def test_send_approve(self):
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
        acc = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
        asset = sdk.native_vm().asset()
        tx_hash = asset.send_approve("ont", acc, acc2.get_address_base58(), 1, acc3, 20000, 500)
        self.assertEqual(len(tx_hash), 64)


if __name__ == '__main__':
    unittest.main()
