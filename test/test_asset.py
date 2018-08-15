#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from ontology.account.account import Account
from ontology.ont_sdk import OntologySdk
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.native_contract.asset import Asset

rpc_address = "http://polaris3.ont.io:20336"
sdk = OntologySdk()
sdk.rpc.set_address(rpc_address)
private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
acc = Account(private_key, SignatureScheme.SHA256withECDSA)
acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)


class TestAsset(unittest.TestCase):
    def test_new_transfer_transaction(self):
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
        gas = 20000 *500
        tx = sdk.native_vm().asset().new_transfer_transaction("ont", acc.get_address().to_base58(),
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

    def test_query_balance(self):
        a = Asset(sdk)
        res = a.query_balance("ont", acc.get_address().to_base58())
        self.assertTrue(isinstance(res, int))

    def test_query_allowance(self):
        a = Asset(sdk)
        res = a.query_allowance("ont", acc.get_address().to_base58(), acc2.get_address().to_base58())
        self.assertEqual(res, '01')

    def test_query_name(self):
        a = Asset(sdk)
        res = a.query_name('ont')
        self.assertEqual(res, 'ONT Token')

    def test_query_symbol(self):
        a = Asset(sdk)
        res = a.query_symbol('ont')
        self.assertEqual(res, 'ONT')

    def test_query_decimals(self):
        a = Asset(sdk)
        res = a.query_decimals("ong")
        self.assertEqual(res, '09')
        res = a.query_decimals("ont")
        self.assertEqual(res, '01')

    def test_send_withdraw_ong_transaction(self):
        a = Asset(sdk)
        res = a.send_withdraw_ong_transaction(acc, acc2.get_address_base58(), 1, acc3, 20000, 500)
        self.assertEqual(res, '01')

    def test_send_approve2(self):
        a = Asset(sdk)
        res = a.send_approve("ont", acc, acc2.get_address_base58(), 1, acc3, 20000, 500)
        self.assertEqual(len(res), 64)


if __name__ == '__main__':
    unittest.main()
