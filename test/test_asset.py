#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import unittest

from test import acct1, acct2, acct3, acct4

from ontology.exception.exception import SDKException
from ontology.utils import utils
from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.native_contract.asset import Asset


class TestAsset(unittest.TestCase):
    def test_get_asset_address(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        ont_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        ong_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
        self.assertEqual(ont_address, asset.get_asset_address('ont'))
        self.assertEqual(ong_address, asset.get_asset_address('ong'))

    def test_query_name(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        token_name = asset.query_name('ont')
        self.assertEqual('ONT Token', token_name)
        token_name = asset.query_name('ong')
        self.assertEqual('ONG Token', token_name)

    def test_query_symbol(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        try:
            token_symbol = asset.query_symbol('ont')
            self.assertEqual('ONT', token_symbol)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            token_symbol = asset.query_symbol('ong')
            self.assertEqual('ONG', token_symbol)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])

    def test_query_decimals(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        decimals = asset.query_decimals('ong')
        self.assertEqual(9, decimals)
        decimals = asset.query_decimals('ont')
        self.assertEqual(1, decimals)

    def test_unbound_ong(self):
        b58_address1 = acct1.get_address_base58()
        b58_address2 = acct2.get_address_base58()
        b58_address3 = acct3.get_address_base58()
        b58_address4 = acct4.get_address_base58()
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        try:
            acct1_unbound_ong = asset.query_unbound_ong(b58_address1)
            self.assertGreaterEqual(acct1_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            acct2_unbound_ong = asset.query_unbound_ong(b58_address2)
            self.assertGreaterEqual(acct2_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            acct3_unbound_ong = asset.query_unbound_ong(b58_address3)
            self.assertGreaterEqual(acct3_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            acct4_unbound_ong = asset.query_unbound_ong(b58_address4)
            self.assertGreaterEqual(acct4_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])

    def test_query_balance(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        private_key = utils.get_random_hex_str(64)
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_address = acct.get_address_base58()
        try:
            balance = asset.query_balance('ont', b58_address)
            self.assertTrue(isinstance(balance, int))
            self.assertGreaterEqual(balance, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            balance = asset.query_balance('ong', b58_address)
            self.assertTrue(isinstance(balance, int))
            self.assertGreaterEqual(balance, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        b58_address = acct2.get_address_base58()
        try:
            balance = asset.query_balance('ong', b58_address)
            self.assertTrue(isinstance(balance, int))
            self.assertGreaterEqual(balance, 1)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])

    def test_query_allowance(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        b58_from_address = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6'
        b58_to_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        allowance = asset.query_allowance('ont', b58_from_address, b58_to_address)
        self.assertGreaterEqual(allowance, 0)
        allowance = asset.query_allowance('ong', b58_from_address, b58_to_address)
        self.assertGreaterEqual(allowance, 0)

    def test_new_approve_transaction(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        sender = acct1
        b58_send_address = sender.get_address_base58()
        b58_payer_address = sender.get_address_base58()
        b58_recv_address = acct2.get_address_base58()
        amount = 5
        gas_price = 500
        gas_limit = 20000
        tx = Asset.new_approve_transaction('ont', b58_send_address, b58_recv_address, amount, b58_payer_address,
                                           gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, sender)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))

    def test_new_transfer_transaction(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        from_acct = acct1
        to_acct = acct2

        b58_from_address = from_acct.get_address_base58()
        b58_to_address = to_acct.get_address_base58()
        b58_payer_address = b58_from_address

        balance_1 = sdk.rpc.get_balance(b58_from_address)
        balance_2 = sdk.rpc.get_balance(b58_to_address)

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
        amount = 1
        gas_price = 500
        gas_limit = 20000

        tx = asset.new_transfer_transaction('ont', b58_from_address, b58_to_address, amount, b58_payer_address,
                                            gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, from_acct)
        tx = sdk.add_sign_transaction(tx, to_acct)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))

        time.sleep(random.randint(6, 10))

        balance_1 = sdk.rpc.get_balance(b58_from_address)
        balance_2 = sdk.rpc.get_balance(b58_to_address)

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
        gas = gas_limit * gas_price
        self.assertEqual(int(old_ont_balance_1) - amount, int(new_ont_balance_1))
        self.assertEqual(int(old_ont_balance_2) + amount, int(new_ont_balance_2))
        self.assertEqual((int(old_ong_balance_1) - int(new_ong_balance_1)), gas)
        self.assertEqual(int(old_ong_balance_2), int(new_ong_balance_2))

    def test_new_transfer_from_transaction(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        sender = acct2
        b58_sender_address = sender.get_address_base58()
        b58_payer_address = sender.get_address_base58()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = sender.get_address_base58()
        old_from_balance = sdk.rpc.get_balance(b58_from_address)
        old_recv_balance = sdk.rpc.get_balance(b58_recv_address)
        amount = 1
        gas_limit = 20000
        gas_price = 500
        tx = Asset.new_transfer_from_transaction('ont', b58_sender_address, b58_from_address, b58_recv_address, amount,
                                                 b58_payer_address, gas_limit, gas_price)
        sdk.add_sign_transaction(tx, sender)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
            time.sleep(random.randint(6, 10))
            new_from_balance = sdk.rpc.get_balance(b58_from_address)
            new_recv_balance = sdk.rpc.get_balance(b58_recv_address)
            self.assertEqual(int(old_from_balance['ont']) - amount, int(new_from_balance['ont']))
            self.assertEqual(int(old_recv_balance['ont']) + amount, int(new_recv_balance['ont']))
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            self.assertEqual('0100000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
            self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])
        except SDKException as e:
            msg = '[TransferFrom] approve balance insufficient!'
            self.assertEqual(59000, e.args[0])
            self.assertIn(msg, e.args[1])

    def test_send_transfer(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        from_acct = acct3
        payer = acct4
        b58_from_address = from_acct.get_address_base58()
        b58_to_address = acct1.get_address_base58()
        old_from_acct_balance = asset.query_balance('ont', b58_from_address)
        old_to_acct_balance = asset.query_balance('ont', b58_to_address)
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx_hash = asset.send_transfer('ont', from_acct, b58_to_address, amount, payer, gas_limit, gas_price)
        time.sleep(random.randint(6, 10))
        new_from_acct_balance = asset.query_balance('ont', b58_from_address)
        new_to_acct_balance = asset.query_balance('ont', b58_to_address)
        self.assertEqual(old_from_acct_balance - amount, new_from_acct_balance)
        self.assertEqual(old_to_acct_balance + amount, new_to_acct_balance)
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        self.assertEqual('0100000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])

    def test_new_withdraw_ong_transaction(self):
        claimer = acct1
        b58_claimer_address = claimer.get_address_base58()
        b58_recv_address = claimer.get_address_base58()
        b58_payer_address = claimer.get_address_base58()
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = Asset.new_withdraw_ong_transaction(b58_claimer_address, b58_recv_address, amount, b58_payer_address,
                                                gas_limit, gas_price)
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        sdk.add_sign_transaction(tx, claimer)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))

    def test_send_withdraw_ong_transaction(self):
        claimer = acct1
        payer = acct2
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        b58_recv_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        gas_limit = 20000
        gas_price = 500
        try:
            tx_hash = asset.send_withdraw_ong_transaction(claimer, b58_recv_address, 1, payer, gas_limit, gas_price)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            msg = 'has no balance enough to cover gas cost 10000000'
            self.assertEqual(59000, e.args[0])
            self.assertIn(msg, e.args[1])

    def test_send_approve(self):
        sender = acct1
        payer = acct2
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        b58_recv_address = acct2.get_address_base58()
        amount = 1
        gas_limit = 20000
        gas_price = 500
        try:
            tx_hash = asset.send_approve('ont', sender, b58_recv_address, amount, payer, gas_limit, gas_price)
            self.assertEqual(len(tx_hash), 64)
        except SDKException as e:
            msg = 'has no balance enough to cover gas cost 10000000'
            self.assertEqual(59000, e.args[0])
            self.assertIn(msg, e.args[1])
        try:
            tx_hash = asset.send_approve('ong', sender, b58_recv_address, amount, payer, gas_limit, gas_price)
            self.assertEqual(len(tx_hash), 64)
        except SDKException as e:
            msg = 'has no balance enough to cover gas cost 10000000'
            self.assertEqual(59000, e.args[0])
            self.assertIn(msg, e.args[1])

    def test_send_transfer_from(self):
        sender = acct2
        payer = sender
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = sender.get_address_base58()
        old_from_balance = sdk.rpc.get_balance(b58_from_address)
        old_recv_balance = sdk.rpc.get_balance(b58_recv_address)
        amount = 1
        gas_limit = 20000
        gas_price = 500
        try:
            tx_hash = asset.send_transfer_from('ont', sender, b58_from_address, b58_recv_address, amount, payer,
                                               gas_limit, gas_price)
            self.assertEqual(64, len(tx_hash))
            time.sleep(random.randint(6, 10))
            new_from_balance = sdk.rpc.get_balance(b58_from_address)
            new_recv_balance = sdk.rpc.get_balance(b58_recv_address)
            self.assertEqual(int(old_from_balance['ont']) - amount, int(new_from_balance['ont']))
            self.assertEqual(int(old_recv_balance['ont']) + amount, int(new_recv_balance['ont']))
        except SDKException as e:
            self.assertIn('[Transfer] balance insufficient', e.args[1])


if __name__ == '__main__':
    unittest.main()
