#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from random import choice

from ontology.common.address import Address
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.network.restful import RestfulClient
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.network.connect_manager import TEST_RESTFUL_ADDRESS
from ontology.ont_sdk import OntologySdk

restful_address = choice(TEST_RESTFUL_ADDRESS)

restful_client = RestfulClient(restful_address)

private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
acc = Account(private_key1, SignatureScheme.SHA256withECDSA)
acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
pub_keys = [acc.get_public_key_bytes(), acc2.get_public_key_bytes(), acc3.get_public_key_bytes()]
multi_addr = Address.address_from_multi_pub_keys(2, pub_keys)


class TestRestfulClient(unittest.TestCase):
    def test_get_version(self):
        version = restful_client.get_version()
        self.assertIn('v', version)

    def test_get_connection_count(self):
        count = restful_client.get_connection_count()
        self.assertGreaterEqual(count, 0)

    def test_get_block_height(self):
        height = restful_client.get_block_height()
        self.assertGreater(height, 1)

    def test_get_block_height_by_tx_hash(self):
        tx_hash = '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e'
        block_height = restful_client.get_block_height_by_tx_hash(tx_hash)
        self.assertEqual(0, block_height)
        tx_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.assertRaises(SDKException, restful_client.get_block_height_by_tx_hash, tx_hash)

    def test_get_gas_price(self):
        price = restful_client.get_gas_price()
        self.assertGreater(price, 0)

    def test_get_network_id(self):
        network_id = restful_client.get_network_id()
        self.assertGreaterEqual(network_id, 0)

    def test_get_block_by_hash(self):
        block_hash = "44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c"
        block = restful_client.get_block_by_hash(block_hash)
        self.assertEqual(block['Hash'], block_hash)

    def test_get_block_by_height(self):
        height = 0
        block = restful_client.get_block_by_height(height)
        self.assertEqual(block['Header']['Height'], height)

    def test_get_balance(self):
        base58_address = "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"
        address_balance = restful_client.get_balance(base58_address)
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
        address_balance = restful_client.get_balance(acc.get_address_base58())
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

        multi_address_balance = restful_client.get_balance(multi_addr.b58encode())
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

    def test_get_smart_contract(self):
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        contract = restful_client.get_smart_contract(hex_contract_address)
        self.assertEqual(True, contract['NeedStorage'])
        self.assertEqual('DINGXIN', contract['Author'])
        self.assertEqual('A sample of OEP4', contract['Description'])

    def test_get_smart_contract_event_by_height(self):
        height = 0
        event_list = restful_client.get_smart_contract_event_by_height(height)
        self.assertEqual(10, len(event_list))
        height = 1309737
        event_list = restful_client.get_smart_contract_event_by_height(height)
        print(event_list)
        self.assertEqual(0, len(event_list))

    def test_get_allowance(self):
        base58_address = "AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA"
        allowance = restful_client.get_allowance('ong', base58_address, base58_address)
        self.assertEqual(allowance, '0')

    def test_get_transaction_by_tx_hash(self):
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        tx = restful_client.get_transaction_by_tx_hash(tx_hash)
        self.assertEqual(tx['Hash'], tx_hash)

    def test_send_raw_transaction(self):
        sdk = OntologySdk()
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = sdk.native_vm().asset().new_transfer_transaction('ont', b58_from_address, b58_to_address, amount,
                                                              b58_from_address, gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, acct)
        tx_hash = restful_client.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.hash256_explorer())

    def test_send_raw_transaction_pre_exec(self):
        sdk = OntologySdk()
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = sdk.native_vm().asset().new_transfer_transaction('ont', b58_from_address, b58_to_address, amount,
                                                              b58_from_address, gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, acct)
        result = restful_client.send_raw_transaction_pre_exec(tx)
        self.assertEqual('01', result['Result'])
        self.assertEqual(20000, result['Gas'])
        self.assertEqual(1, result['State'])


if __name__ == '__main__':
    unittest.main()
