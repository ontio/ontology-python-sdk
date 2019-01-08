#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from test import acct1, acct2, acct3

from ontology.exception.exception import SDKException
from ontology.ont_sdk import OntologySdk
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.utils.utils import get_random_hex_str
from ontology.smart_contract.native_contract.asset import Asset
from ontology.utils.contract_data_parser import ContractDataParser

pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
multi_address = Address.address_from_multi_pub_keys(2, pub_keys)


class TestRpcClient(unittest.TestCase):
    def test_get_version(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        version = sdk.rpc.get_version()
        self.assertIn('v', version)

    def test_get_connection_count(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        count = sdk.rpc.get_connection_count()
        self.assertGreaterEqual(count, 0)

    def test_get_gas_price(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        price = sdk.rpc.get_gas_price()
        self.assertGreater(price, 0)

    def test_get_network_id(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        network_id = sdk.rpc.get_network_id()
        self.assertGreaterEqual(network_id, 0)

    def test_get_block_by_hash(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        block_hash = '44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c'
        block = sdk.rpc.get_block_by_hash(block_hash)
        self.assertEqual(block['Hash'], block_hash)

    def test_get_block_by_height(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        height = 0
        block = sdk.rpc.get_block_by_height(height)
        self.assertEqual(block['Header']['Height'], height)

    def test_get_block_height(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        count = sdk.rpc.get_block_height()
        self.assertGreater(count, 103712)

    def test_get_block_height_by_tx_hash(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        tx_hash = '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e'
        block_height = sdk.rpc.get_block_height_by_tx_hash(tx_hash)
        self.assertEqual(0, block_height)
        tx_hash = 'e96994829aa9f6cf402da56f427491458a730df1c3ff9158ef1cbed31b8628f2'
        block_height = sdk.rpc.get_block_height_by_tx_hash(tx_hash)
        self.assertEqual(564235, block_height)

    def test_get_block_count_by_tx_hash(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        tx_hash = '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e'
        block_count = sdk.rpc.get_block_count_by_tx_hash(tx_hash)
        self.assertEqual(1, block_count)
        tx_hash = 'e96994829aa9f6cf402da56f427491458a730df1c3ff9158ef1cbed31b8628f2'
        block_count = sdk.rpc.get_block_count_by_tx_hash(tx_hash)
        self.assertEqual(564236, block_count)

    def test_get_current_block_hash(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        current_block_hash = sdk.rpc.get_current_block_hash()
        self.assertEqual(len(current_block_hash), 64)

    def test_get_block_hash_by_height(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        height = 0
        block_hash = sdk.rpc.get_block_hash_by_height(height)
        self.assertEqual(len(block_hash), 64)

    def test_get_balance(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        base58_address = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6'
        address_balance = sdk.rpc.get_balance(base58_address)
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
        address_balance = sdk.rpc.get_balance(acct1.get_address_base58())
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

        multi_address_balance = sdk.rpc.get_balance(multi_address.b58encode())
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

    def test_get_grant_ong(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        b58_address = 'AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA'
        grant_ong = sdk.rpc.get_grant_ong(b58_address)
        self.assertGreaterEqual(grant_ong, 0)

    def test_get_allowance(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        base58_address = 'AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA'
        allowance = sdk.rpc.get_allowance('ong', base58_address, base58_address)
        self.assertEqual(allowance, '0')

    def test_get_storage(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        contract_address = "0100000000000000000000000000000000000000"
        key = "746f74616c537570706c79"
        value = sdk.rpc.get_storage(contract_address, key)
        value = ContractDataParser.to_int(value)
        self.assertEqual(1000000000, value)

    def test_get_smart_contract_event_by_tx_hash(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        self.assertEqual(event['TxHash'], tx_hash)

    def test_get_smart_contract_event_by_height(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        height = 0
        event_list = sdk.rpc.get_smart_contract_event_by_height(height)
        self.assertEqual(10, len(event_list))
        height = 1309737
        event_list = sdk.rpc.get_smart_contract_event_by_height(height)
        self.assertEqual(0, len(event_list))

    def test_get_smart_contract_event_by_count(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        count = 1
        event_list = sdk.rpc.get_smart_contract_event_by_count(count)
        self.assertEqual(10, len(event_list))
        count = 1309738
        event_list = sdk.rpc.get_smart_contract_event_by_count(count)
        self.assertEqual(0, len(event_list))

    def test_sync_block(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        current_height = sdk.rpc.get_block_height()
        start_time = time.perf_counter()
        while True:
            end_time = time.perf_counter()
            if end_time - start_time > 10:
                break
            time.sleep(1)
            height = sdk.rpc.get_block_height()
            current_height = (height, current_height)[height - current_height == 1]
            if height != current_height:
                current_height = height
                event_list = sdk.rpc.get_smart_contract_event_by_height(height)
                self.assertGreaterEqual(len(event_list), 0)

    def test_get_transaction_by_tx_hash(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        tx_hash = '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74'
        tx = sdk.rpc.get_transaction_by_tx_hash(tx_hash)
        self.assertEqual(tx['Hash'], tx_hash)

    def test_get_smart_contract(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        hex_contract_address = '0100000000000000000000000000000000000000'
        contract = sdk.rpc.get_smart_contract(hex_contract_address)
        self.assertEqual(contract['Description'], 'Ontology Network ONT Token')

    def test_get_merkle_proof(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        tx_hash_1 = '12943957b10643f04d89938925306fa342cec9d32925f5bd8e9ea7ce912d16d3'
        merkle_proof_1 = sdk.rpc.get_merkle_proof(tx_hash_1)
        self.assertEqual('MerkleProof', merkle_proof_1['Type'])
        self.assertEqual(0, merkle_proof_1['BlockHeight'])
        tx_hash_2 = '1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79'
        merkle_proof_2 = sdk.rpc.get_merkle_proof(tx_hash_2)
        self.assertEqual('MerkleProof', merkle_proof_2['Type'])
        self.assertEqual(0, merkle_proof_2['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_2['TransactionsRoot'])
        tx_hash_3 = '5d09b2b9ba302e9da8b9472ef10c824caf998e940cc5a73d7da16971d64c0290'
        merkle_proof_3 = sdk.rpc.get_merkle_proof(tx_hash_3)
        self.assertEqual('MerkleProof', merkle_proof_3['Type'])
        self.assertEqual(0, merkle_proof_3['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_3['TransactionsRoot'])
        tx_hash_4 = '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74'
        merkle_proof_4 = sdk.rpc.get_merkle_proof(tx_hash_4)
        self.assertEqual('MerkleProof', merkle_proof_4['Type'])
        self.assertEqual(0, merkle_proof_4['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_4['TransactionsRoot'])
        tx_hash_5 = '7842ed25e4f028529e666bcecda2795ec49d570120f82309e3d5b94f72d30ebb'
        merkle_proof_5 = sdk.rpc.get_merkle_proof(tx_hash_5)
        self.assertEqual('MerkleProof', merkle_proof_5['Type'])
        self.assertEqual(0, merkle_proof_5['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_5['TransactionsRoot'])
        tx_hash_6 = '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e'
        merkle_proof_6 = sdk.rpc.get_merkle_proof(tx_hash_6)
        self.assertEqual('MerkleProof', merkle_proof_6['Type'])
        self.assertEqual(0, merkle_proof_6['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_6['TransactionsRoot'])

    def test_send_raw_transaction(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        b58_from_address = acct2.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, amount,
                                                            b58_from_address,
                                                            gas_limit, gas_price)
        tx.sign_transaction(acct2)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.hash256_explorer())

    def test_send_raw_transaction_pre_exec(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        random_pk = get_random_hex_str(64)
        random_acct = Account(random_pk)
        b58_address_1 = acct2.get_address_base58()
        random_b58_address = random_acct.get_address_base58()
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_address_1, random_b58_address, 2, b58_address_1,
                                                            20000, 500)
        tx.sign_transaction(acct2)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(result['Result'], '01')
        self.assertEqual(result['Gas'], 20000)
        self.assertEqual(result['State'], 1)

    def test_get_memory_pool_tx_count(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        tx_count = sdk.rpc.get_memory_pool_tx_count()
        self.assertGreaterEqual(tx_count, [0, 0])

    def test_get_memory_pool_tx_state(self):
        sdk = OntologySdk()
        sdk.rpc.connect_to_test_net()
        tx_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        try:
            sdk.rpc.get_memory_pool_tx_state(tx_hash)
        except SDKException as e:
            self.assertIn('unknown transaction', e.args[1])
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = contract_address
        from_acct = acct1
        gas_limit = 20000000
        gas_price = 500
        b58_to_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        value = 10
        tx_hash = oep4.transfer(from_acct, b58_to_address, value, from_acct, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        try:
            tx_state = sdk.rpc.get_memory_pool_tx_state(tx_hash)
            self.assertTrue(isinstance(tx_state, list))
        except SDKException as e:
            self.assertEqual(59000, e.args[0])


if __name__ == '__main__':
    unittest.main()
