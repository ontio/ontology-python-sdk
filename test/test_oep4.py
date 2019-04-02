#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from Cryptodome.Random.random import randint

from test import sdk, acct1, acct2, acct3, acct4

from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme


class TestOep4(unittest.TestCase):
    def test_set_contract_address(self):
        contract_address = '85848b5ec3b15617e396bdd62cb49575738dd413'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        self.assertEqual(contract_address, oep4.hex_contract_address)

    def test_get_name(self):
        contract_address = 'd7b6a47966770c1545bf74c16426b26c0a238b16'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        self.assertEqual('DXToken', oep4.get_name())

    def test_get_symbol(self):
        contract_address = 'd7b6a47966770c1545bf74c16426b26c0a238b16'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        self.assertEqual('DX', oep4.get_symbol())

    def test_get_decimal(self):
        contract_address1 = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address1
        self.assertEqual(10, oep4.get_decimal())
        contract_address2 = '165b1227311d47c22cd073ef8f285d3bddc858ca'
        oep4.hex_contract_address = contract_address2
        self.assertEqual(32, oep4.get_decimal())
        contract_address3 = '8fecd2740b10a7410026774cc1f99fe14860873b'
        oep4.hex_contract_address = contract_address3
        self.assertEqual(255, oep4.get_decimal())

    def test_init(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.init(acct, acct1, gas_limit, gas_price)
        self.assertEqual(len(tx_hash), 64)
        time.sleep(randint(6, 10))
        notify = sdk.rpc.get_contract_event_by_tx_hash(tx_hash)['Notify'][0]
        self.assertEqual('Already initialized!', bytes.fromhex(notify['States']).decode())

    def test_get_total_supply(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        self.assertEqual(10000000000000000000, oep4.get_total_supply())

    def test_transfer(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        from_acct = acct1
        gas_limit = 20000000
        gas_price = 500
        b58_to_address = acct2.get_address_base58()
        value = 10
        tx_hash = oep4.transfer(from_acct, b58_to_address, value, from_acct, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        time.sleep(6)
        notify = oep4.query_transfer_event(tx_hash)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(from_acct.get_address_base58(), notify['States'][1])
        self.assertEqual(b58_to_address, notify['States'][2])
        self.assertEqual(value, notify['States'][3])

    def test_balance_of(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        b58_address1 = acct3.get_address_base58()
        b58_address2 = acct4.get_address_base58()
        balance = oep4.balance_of(b58_address1)
        self.assertGreaterEqual(balance, 10)
        balance = oep4.balance_of(b58_address2)
        self.assertGreaterEqual(balance, 1)

    def test_transfer_multi(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        transfer_list = list()

        b58_from_address1 = acct1.get_address_base58()
        b58_from_address2 = acct2.get_address_base58()
        from_address_list = [b58_from_address1, b58_from_address2]

        b58_to_address1 = acct2.get_address_base58()
        b58_to_address2 = acct3.get_address_base58()
        to_address_list = [b58_to_address1, b58_to_address2]

        value_list = [1, 2]

        transfer1 = [b58_from_address1, b58_to_address1, value_list[0]]
        transfer2 = [b58_from_address2, b58_to_address2, value_list[1]]

        signers = [acct1, acct2, acct3]
        transfer_list.append(transfer1)
        transfer_list.append(transfer2)

        gas_limit = 20000000
        gas_price = 500

        tx_hash = oep4.transfer_multi(transfer_list, signers[0], signers, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(6, 10))
        notify_list = oep4.query_multi_transfer_event(tx_hash)
        try:
            self.assertEqual(len(transfer_list), len(notify_list))
            for index, notify in enumerate(notify_list):
                self.assertEqual('transfer', notify['States'][0])
                self.assertEqual(from_address_list[index], notify['States'][1])
                self.assertEqual(to_address_list[index], notify['States'][2])
                self.assertEqual(value_list[index], notify['States'][3])
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_approve(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        owner_acct = acct1
        spender = acct2
        b58_spender_address = spender.get_address_base58()
        amount = 100
        gas_limit = 20000000
        gas_price = 500
        try:
            tx_hash = oep4.approve(owner_acct, b58_spender_address, amount, owner_acct, gas_limit, gas_price)
        except SDKException as e:
            self.assertIn('ConnectTimeout', e.args[1])
            return
        self.assertEqual(len(tx_hash), 64)
        time.sleep(randint(6, 10))
        try:
            event = oep4.query_approve_event(tx_hash)
            states = event['States']
            self.assertEqual('approval', states[0])
            self.assertEqual(owner_acct.get_address_base58(), states[1])
            self.assertEqual(b58_spender_address, states[2])
            self.assertEqual(amount, states[3])
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_allowance(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        b58_owner_address = acct1.get_address_base58()
        b58_spender_address = acct2.get_address_base58()
        allowance = oep4.allowance(b58_owner_address, b58_spender_address)
        self.assertGreaterEqual(allowance, 1)

    def test_transfer_from(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        spender_acct = acct2

        from_acct = acct1
        b58_from_address = from_acct.get_address_base58()
        hex_from_address = from_acct.get_address_hex()

        to_acct = acct3
        b58_to_address = to_acct.get_address_base58()
        hex_to_address = to_acct.get_address_hex()

        gas_limit = 20000000
        gas_price = 500
        value = 1
        tx_hash = oep4.transfer_from(spender_acct, b58_from_address, b58_to_address, value, from_acct, gas_limit,
                                     gas_price)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(6, 10))
        try:
            event = sdk.rpc.get_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][0]
            self.assertEqual(2, len(notify))
            self.assertEqual('transfer', bytes.fromhex(notify['States'][0]).decode())
            self.assertEqual(hex_from_address, notify['States'][1])
            self.assertEqual(hex_to_address, notify['States'][2])
            bytearray_value = bytearray.fromhex(notify['States'][3])
            bytearray_value.reverse()
            notify_value = int(bytearray_value.hex(), 16)
            self.assertEqual(value, notify_value)
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)


if __name__ == '__main__':
    unittest.main()
