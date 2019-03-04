#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from Cryptodome.Random.random import randint

from test import sdk, acct1, acct2, acct3, acct4

from ontology.exception.exception import SDKException
from ontology.utils.contract_event import ContractEventParser


class TestAsset(unittest.TestCase):
    def test_get_asset_address(self):
        ont_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        ong_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
        self.assertEqual(ont_address, sdk.native_vm.asset().get_asset_address('ont'))
        self.assertEqual(ong_address, sdk.native_vm.asset().get_asset_address('ong'))

    def test_query_name(self):
        sdk.rpc.connect_to_test_net()
        token_name = sdk.native_vm.asset().query_name('ont')
        self.assertEqual('ONT Token', token_name)
        token_name = sdk.native_vm.asset().query_name('ong')
        self.assertEqual('ONG Token', token_name)

    def test_query_symbol(self):
        sdk.rpc.connect_to_test_net()
        try:
            token_symbol = sdk.native_vm.asset().query_symbol('ont')
            self.assertEqual('ONT', token_symbol)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            token_symbol = sdk.native_vm.asset().query_symbol('ong')
            self.assertEqual('ONG', token_symbol)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])

    def test_query_decimals(self):
        sdk.rpc.connect_to_test_net()
        decimals = sdk.native_vm.asset().query_decimals('ong')
        self.assertEqual(9, decimals)
        decimals = sdk.native_vm.asset().query_decimals('ont')
        self.assertEqual(0, decimals)

    def test_unbound_ong(self):
        b58_address1 = acct1.get_address_base58()
        b58_address2 = acct2.get_address_base58()
        b58_address3 = acct3.get_address_base58()
        b58_address4 = acct4.get_address_base58()
        try:
            acct1_unbound_ong = sdk.native_vm.asset().query_unbound_ong(b58_address1)
            self.assertGreaterEqual(acct1_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            acct2_unbound_ong = sdk.native_vm.asset().query_unbound_ong(b58_address2)
            self.assertGreaterEqual(acct2_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            acct3_unbound_ong = sdk.native_vm.asset().query_unbound_ong(b58_address3)
            self.assertGreaterEqual(acct3_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            acct4_unbound_ong = sdk.native_vm.asset().query_unbound_ong(b58_address4)
            self.assertGreaterEqual(acct4_unbound_ong, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])

    def test_query_balance(self):
        b58_address = acct1.get_address_base58()
        try:
            balance = sdk.native_vm.asset().query_balance('ont', b58_address)
            self.assertTrue(isinstance(balance, int))
            self.assertGreaterEqual(balance, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        try:
            balance = sdk.native_vm.asset().query_balance('ong', b58_address)
            self.assertTrue(isinstance(balance, int))
            self.assertGreaterEqual(balance, 0)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
        b58_address = acct2.get_address_base58()
        try:
            balance = sdk.native_vm.asset().query_balance('ong', b58_address)
            self.assertTrue(isinstance(balance, int))
            self.assertGreaterEqual(balance, 1)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])

    def test_query_allowance(self):
        b58_from_address = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6'
        b58_to_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        allowance = sdk.native_vm.asset().query_allowance('ont', b58_from_address, b58_to_address)
        self.assertGreaterEqual(allowance, 0)
        allowance = sdk.native_vm.asset().query_allowance('ong', b58_from_address, b58_to_address)
        self.assertGreaterEqual(allowance, 0)

    def test_new_approve_transaction(self):
        b58_send_address = acct2.get_address_base58()
        b58_payer_address = acct2.get_address_base58()
        b58_recv_address = acct1.get_address_base58()
        amount = 5
        gas_price = 500
        gas_limit = 20000
        try:
            tx = sdk.native_vm.asset().new_approve_transaction('ont', b58_send_address, b58_recv_address, amount,
                                                               b58_payer_address, gas_limit, gas_price)
            tx.sign_transaction(acct2)
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('balance insufficient', e.args[1])

    def test_new_transfer_transaction(self):
        sdk.rpc.connect_to_test_net()
        b58_from_address = acct1.get_address_base58()
        b58_to_address = acct2.get_address_base58()
        b58_payer_address = b58_to_address
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = sdk.native_vm.asset().new_transfer_transaction('ont', b58_from_address, b58_to_address, amount,
                                                            b58_payer_address, gas_limit, gas_price)
        tx.sign_transaction(acct1)
        tx.add_sign_transaction(acct2)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('balance insufficient', e.args[1])
            return

        time.sleep(randint(7, 12))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        ont_contract_address = '0100000000000000000000000000000000000000'
        notify = ContractEventParser.get_notify_list_by_contract_address(event, ont_contract_address)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(b58_from_address, notify['States'][1])
        self.assertEqual(b58_to_address, notify['States'][2])
        self.assertEqual(amount, notify['States'][3])
        ong_contract_address = '0200000000000000000000000000000000000000'
        notify = ContractEventParser.get_notify_list_by_contract_address(event, ong_contract_address)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(b58_payer_address, notify['States'][1])
        self.assertEqual(gas_price * gas_limit, notify['States'][3])

    def test_transfer(self):
        sdk.rpc.connect_to_test_net()
        b58_to_address = acct1.get_address_base58()
        try:
            tx_hash = sdk.native_vm.asset().transfer('ont', acct2, b58_to_address, 1, acct4, 20000, 500)
        except SDKException as e:
            self.assertIn('balance insufficient', e.args[1])
            return
        time.sleep(randint(7, 12))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        self.assertEqual('0100000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])

    def test_new_transfer_from_transaction(self):
        sdk.rpc.connect_to_test_net()
        b58_sender_address = acct2.get_address_base58()
        b58_payer_address = acct2.get_address_base58()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = acct2.get_address_base58()
        tx = sdk.native_vm.asset().new_transfer_from_transaction('ont', b58_sender_address, b58_from_address,
                                                                 b58_recv_address, 1, b58_payer_address, 20000, 500)
        tx.add_sign_transaction(acct2)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg1 = 'balance insufficient'
            msg2 = 'already in the tx pool'
            self.assertTrue(msg1 in e.args[1] or msg2 in e.args[1])
            return
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(7, 12))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        self.assertEqual('0100000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])

    def test_new_withdraw_ong_transaction(self):
        sdk.rpc.connect_to_test_net()
        b58_claimer_address = acct1.get_address_base58()
        b58_recv_address = acct1.get_address_base58()
        b58_payer_address = acct1.get_address_base58()
        amount = 1
        gas_price = 500
        gas_limit = 20000
        for _ in range(3):
            tx = sdk.native_vm.asset().new_withdraw_ong_transaction(b58_claimer_address, b58_recv_address, amount,
                                                                    b58_payer_address, gas_limit, gas_price)
            tx.add_sign_transaction(acct1)
            try:
                tx_hash = sdk.rpc.send_raw_transaction(tx)
                self.assertEqual(64, len(tx_hash))
            except SDKException as e:
                msg = 'already in the tx pool'
                self.assertTrue(msg in e.args[1])

    def test_withdraw_ong(self):
        claimer = acct1
        payer = acct2
        b58_recv_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        for _ in range(5):
            try:
                tx_hash = sdk.native_vm.asset().withdraw_ong(claimer, b58_recv_address, 1, payer, 20000, 500)
                self.assertEqual(64, len(tx_hash))
            except SDKException as e:
                msg1 = 'no balance enough'
                msg2 = 'ConnectTimeout'
                msg3 = 'already in the tx pool'
                self.assertTrue(msg1 in e.args[1] or msg2 in e.args[1] or msg3 in e.args[1])

    def test_approve(self):
        b58_recv_address = acct2.get_address_base58()
        for _ in range(3):
            try:
                tx_hash = sdk.native_vm.asset().approve('ont', acct1, b58_recv_address, 10, acct2, 20000, 500)
                self.assertEqual(len(tx_hash), 64)
            except SDKException as e:
                msg1 = 'no balance enough'
                msg2 = 'ConnectTimeout'
                msg3 = 'already in the tx pool'
                self.assertTrue(msg1 in e.args[1] or msg2 in e.args[1] or msg3 in e.args[1])

    def test_transfer_from(self):
        sdk.rpc.connect_to_test_net()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = acct2.get_address_base58()
        for _ in range(3):
            try:
                tx_hash = sdk.native_vm.asset().transfer_from('ont', acct2, b58_from_address, b58_recv_address, 1,
                                                              acct2, 20000, 500)
                self.assertEqual(64, len(tx_hash))
                time.sleep(randint(7, 12))
                event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
                self.assertEqual('0100000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
                self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])
            except SDKException as e:
                msg1 = 'balance insufficient'
                msg2 = 'ConnectTimeout'
                msg3 = 'already in the tx pool'
                self.assertTrue(msg1 in e.args[1] or msg2 in e.args[1] or msg3 in e.args[1])


if __name__ == '__main__':
    unittest.main()
