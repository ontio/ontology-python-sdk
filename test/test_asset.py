#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from Cryptodome.Random.random import randint

from test import acct1, acct2, acct3, acct4

from ontology.utils import utils
from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.native_contract.asset import Asset
from ontology.utils.contract_event_parser import ContractEventParser


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
        sender = acct2
        b58_send_address = sender.get_address_base58()
        b58_payer_address = sender.get_address_base58()
        b58_recv_address = acct1.get_address_base58()
        amount = 5
        gas_price = 500
        gas_limit = 20000
        try:
            tx = Asset.new_approve_transaction('ont', b58_send_address, b58_recv_address, amount, b58_payer_address,
                                               gas_limit, gas_price)
            tx.sign_transaction(sender)
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('balance insufficient', e.args[1])

    def test_new_transfer_transaction(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        from_acct = acct1
        to_acct = acct2

        b58_from_address = from_acct.get_address_base58()
        b58_to_address = to_acct.get_address_base58()
        b58_payer_address = b58_to_address

        amount = 1
        gas_price = 500
        gas_limit = 20000

        tx = asset.new_transfer_transaction('ont', b58_from_address, b58_to_address, amount, b58_payer_address,
                                            gas_limit, gas_price)
        tx.sign_transaction(from_acct)
        tx.add_sign_transaction(to_acct)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('balance insufficient', e.args[1])
            return

        time.sleep(randint(6, 10))

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

    def test_send_transfer(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        from_acct = acct2
        payer = acct4
        b58_to_address = acct1.get_address_base58()
        amount = 1
        gas_price = 500
        gas_limit = 20000
        try:
            tx_hash = asset.send_transfer('ont', from_acct, b58_to_address, amount, payer, gas_limit, gas_price)
        except SDKException as e:
            self.assertIn('balance insufficient', e.args[1])
            return
        time.sleep(randint(6, 10))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        self.assertEqual('0100000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])

    def test_new_transfer_from_transaction(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        sender = acct2
        b58_sender_address = sender.get_address_base58()
        b58_payer_address = sender.get_address_base58()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = sender.get_address_base58()
        amount = 1
        gas_limit = 20000
        gas_price = 500
        tx = Asset.new_transfer_from_transaction('ont', b58_sender_address, b58_from_address, b58_recv_address, amount,
                                                 b58_payer_address, gas_limit, gas_price)
        sdk.add_sign_transaction(tx, sender)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg1 = 'balance insufficient'
            msg2 = 'already in the tx pool'
            self.assertTrue(msg1 in e.args[1] or msg2 in e.args[1])
            return
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(6, 10))
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
            msg = 'no balance enough'
            self.assertEqual(59000, e.args[0])
            self.assertIn(msg, e.args[1])

    def test_send_approve(self):
        sender = acct1
        payer = acct2
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        asset = sdk.native_vm.asset()
        b58_recv_address = acct2.get_address_base58()
        amount = 10
        gas_limit = 20000
        gas_price = 500
        try:
            tx_hash = asset.send_approve('ont', sender, b58_recv_address, amount, payer, gas_limit, gas_price)
            self.assertEqual(len(tx_hash), 64)
        except SDKException as e:
            msg = 'no balance enough'
            self.assertEqual(59000, e.args[0])
            self.assertIn(msg, e.args[1])
        try:
            tx_hash = asset.send_approve('ong', sender, b58_recv_address, amount, payer, gas_limit, gas_price)
            self.assertEqual(len(tx_hash), 64)
        except SDKException as e:
            msg = 'no balance enough'
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
        amount = 1
        gas_limit = 20000
        gas_price = 500
        try:
            tx_hash = asset.send_transfer_from('ont', sender, b58_from_address, b58_recv_address, amount, payer,
                                               gas_limit, gas_price)
            self.assertEqual(64, len(tx_hash))
            time.sleep(randint(6, 10))
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            self.assertEqual('0100000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
            self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])
        except SDKException as e:
            self.assertIn('balance insufficient', e.args[1])


if __name__ == '__main__':
    unittest.main()
