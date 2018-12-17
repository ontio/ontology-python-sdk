#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from random import choice

from ontology.network.rpc import RpcClient
from ontology.ont_sdk import OntologySdk
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.utils.utils import get_random_hex_str
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.network.connect_manager import TEST_RPC_ADDRESS
from ontology.smart_contract.native_contract.asset import Asset
from ontology.utils.contract_data_parser import ContractDataParser

rpc_address = choice(TEST_RPC_ADDRESS)
rpc_client = RpcClient(rpc_address)

private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
acc = Account(private_key1, SignatureScheme.SHA256withECDSA)
acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
pub_keys = [acc.get_public_key_bytes(), acc2.get_public_key_bytes(), acc3.get_public_key_bytes()]
multi_addr = Address.address_from_multi_pub_keys(2, pub_keys)


class TestRpcClient(unittest.TestCase):
    def test_get_version(self):
        version = rpc_client.get_version()
        self.assertIn('v', version)

    def test_get_connection_count(self):
        count = rpc_client.get_connection_count()
        self.assertGreaterEqual(count, 0)

    def test_get_gas_price(self):
        price = rpc_client.get_gas_price()
        self.assertGreater(price, 0)

    def test_get_network_id(self):
        network_id = rpc_client.get_network_id()
        self.assertGreaterEqual(network_id, 0)

    def test_get_block_by_hash(self):
        block_hash = "44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c"
        block = rpc_client.get_block_by_hash(block_hash)
        self.assertEqual(block['Hash'], block_hash)

    def test_get_block_by_height(self):
        height = 0
        block = rpc_client.get_block_by_height(height)
        self.assertEqual(block['Header']['Height'], height)

    def test_get_block_count(self):
        count = rpc_client.get_block_count()
        self.assertGreater(count, 103712)

    def test_get_current_block_hash(self):
        current_block_hash = rpc_client.get_current_block_hash()
        self.assertEqual(len(current_block_hash), 64)

    def test_get_block_hash_by_height(self):
        height = 0
        block_hash = rpc_client.get_block_hash_by_height(height)
        self.assertEqual(len(block_hash), 64)

    def test_get_balance(self):
        base58_address = "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"
        address_balance = rpc_client.get_balance(base58_address)
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
        address_balance = rpc_client.get_balance(acc.get_address_base58())
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

        multi_address_balance = rpc_client.get_balance(multi_addr.b58encode())
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
        base58_address = "AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA"
        allowance = rpc_client.get_allowance("ong", base58_address, base58_address)
        self.assertEqual(allowance, '0')

    def test_get_storage(self):
        contract_address = "0100000000000000000000000000000000000000"
        key = "746f74616c537570706c79"
        value = rpc_client.get_storage(contract_address, key)
        value = ContractDataParser.to_int(value)
        self.assertEqual(1000000000, value)

    def test_get_smart_contract_event_by_tx_hash(self):
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        event = rpc_client.get_smart_contract_event_by_tx_hash(tx_hash)
        self.assertEqual(event['TxHash'], tx_hash)

    def test_get_smart_contract_event_by_block(self):
        height = 0
        event = rpc_client.get_smart_contract_event_by_height(height)
        self.assertEqual(event[0]['State'], 1)

    def test_get_raw_transaction(self):
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        tx = rpc_client.get_raw_transaction(tx_hash)
        self.assertEqual(tx['Hash'], tx_hash)

    def test_get_smart_contract(self):
        contract_address = "0239dcf9b4a46f15c5f23f20d52fac916a0bac0d"
        contract = rpc_client.get_smart_contract(contract_address)
        self.assertEqual(contract['Description'], 'Ontology Network ONT Token')

    def test_get_merkle_proof(self):
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        proof = rpc_client.get_merkle_proof(tx_hash)
        self.assertEqual(proof['Type'], 'MerkleProof')

    def test_send_raw_transaction(self):
        sdk = OntologySdk()
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = Asset.new_transfer_transaction('ont', b58_from_address, b58_to_address, amount, b58_from_address,
                                            gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, acct)
        tx_hash = rpc_client.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.hash256_explorer())

    def test_send_raw_transaction_pre_exec(self):
        sdk = OntologySdk()
        pri_key_1 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(pri_key_1)
        pri_key2 = get_random_hex_str(64)
        acct2 = Account(pri_key2)
        b58_address_1 = acct.get_address_base58()
        b58_address_2 = acct2.get_address_base58()
        tx = Asset.new_transfer_transaction('ont', b58_address_1, b58_address_2, 2, b58_address_1, 20000, 500)
        tx = sdk.sign_transaction(tx, acct)
        result = rpc_client.send_raw_transaction_pre_exec(tx)
        self.assertEqual(result['Result'], '01')
        self.assertEqual(result['Gas'], 20000)
        self.assertEqual(result['State'], 1)


if __name__ == '__main__':
    unittest.main()
