#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from test import sdk, acct1, acct2, acct3

from ontology.common.address import Address
from ontology.account.account import Account
from ontology.utils.utils import get_random_hex_str
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser

pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
multi_address = Address.address_from_multi_pub_keys(2, pub_keys)


class TestRpcClient(unittest.TestCase):
    def test_get_version(self):
        try:
            version = sdk.rpc.get_version()
            self.assertTrue(isinstance(version, str))
            if version != '':
                self.assertIn('v', version)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_connection_count(self):
        try:
            count = sdk.rpc.get_connection_count()
            self.assertGreaterEqual(count, 0)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_gas_price(self):
        try:
            price = sdk.rpc.get_gas_price()
            self.assertGreater(price, 0)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_network_id(self):
        try:
            network_id = sdk.rpc.get_network_id()
            self.assertGreaterEqual(network_id, 0)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_block_by_hash(self):
        try:
            block_hash = '44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c'
            block = sdk.rpc.get_block_by_hash(block_hash)
            self.assertEqual(block['Hash'], block_hash)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_block_by_height(self):
        try:
            height = 0
            block = sdk.rpc.get_block_by_height(height)
            self.assertEqual(block['Header']['Height'], height)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_block_height(self):
        try:
            height = sdk.rpc.get_block_height()
            self.assertGreater(height, 103712)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_block_height_by_tx_hash(self):
        tx_hash_lst = ['7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e',
                       'e96994829aa9f6cf402da56f427491458a730df1c3ff9158ef1cbed31b8628f2']
        height_lst = [0, 564235]
        try:
            for index, tx_hash in enumerate(tx_hash_lst):
                block_count = sdk.rpc.get_block_height_by_tx_hash(tx_hash)
                self.assertEqual(height_lst[index], block_count)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_block_count_by_tx_hash(self):
        tx_hash_lst = ['7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e',
                       'e96994829aa9f6cf402da56f427491458a730df1c3ff9158ef1cbed31b8628f2']
        count_lst = [1, 564236]
        try:
            for index, tx_hash in enumerate(tx_hash_lst):
                block_count = sdk.rpc.get_block_count_by_tx_hash(tx_hash)
                self.assertEqual(count_lst[index], block_count)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_current_block_hash(self):
        try:
            current_block_hash = sdk.rpc.get_current_block_hash()
            self.assertEqual(len(current_block_hash), 64)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_block_hash_by_height(self):
        height = 0
        try:
            block_hash = sdk.rpc.get_block_hash_by_height(height)
            self.assertEqual(len(block_hash), 64)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_balance(self):
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
        b58_address = 'AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA'
        grant_ong = sdk.rpc.get_grant_ong(b58_address)
        self.assertGreaterEqual(grant_ong, 0)

    def test_get_allowance(self):
        base58_address = 'AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA'
        try:
            allowance = sdk.rpc.get_allowance('ong', base58_address, base58_address)
            self.assertEqual(allowance, '0')
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_storage(self):
        hex_contract_address = "0100000000000000000000000000000000000000"
        key = "746f74616c537570706c79"
        try:
            value = sdk.rpc.get_storage(hex_contract_address, key)
            value = ContractDataParser.to_int(value)
            self.assertEqual(1000000000, value)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_smart_contract_event_by_tx_hash(self):
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        try:
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            self.assertEqual(event['TxHash'], tx_hash)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_smart_contract_event_by_height(self):
        height_lst = [0, 1309737]
        event_len_lst = [10, 0]
        try:
            for index, h in enumerate(height_lst):
                event_list = sdk.rpc.get_smart_contract_event_by_height(h)
                self.assertEqual(event_len_lst[index], len(event_list))
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_smart_contract_event_by_count(self):
        cnt_lst = [1, 1309738]
        event_len_lst = [10, 0]
        try:
            for index, cnt in enumerate(cnt_lst):
                event_list = sdk.rpc.get_smart_contract_event_by_count(cnt)
                self.assertEqual(event_len_lst[index], len(event_list))
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_sync_block(self):
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
        tx_hash = '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74'
        tx = sdk.rpc.get_transaction_by_tx_hash(tx_hash)
        self.assertEqual(tx['Hash'], tx_hash)

    def test_get_smart_contract(self):
        try:
            contract = sdk.rpc.get_smart_contract('0100000000000000000000000000000000000000')
            self.assertEqual(contract['Description'], 'Ontology Network ONT Token')
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])
        try:
            sdk.rpc.connect_to_main_net()
            contract = sdk.rpc.get_smart_contract('6c80f3a5c183edee7693a038ca8c476fb0d6ac91')
            self.assertEqual('Youle_le_service@fosun.com', contract.get('Email', ''))
            self.assertEqual('chentao', contract.get('Author', ''))
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])
        finally:
            sdk.rpc.connect_to_test_net()

    def test_get_merkle_proof(self):
        pre_tx_root = 0
        tx_hash_list = ['12943957b10643f04d89938925306fa342cec9d32925f5bd8e9ea7ce912d16d3',
                        '1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79',
                        '5d09b2b9ba302e9da8b9472ef10c824caf998e940cc5a73d7da16971d64c0290',
                        '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74',
                        '7842ed25e4f028529e666bcecda2795ec49d570120f82309e3d5b94f72d30ebb',
                        '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e']
        try:
            for tx_hash in tx_hash_list:
                merkle_proof = sdk.rpc.get_merkle_proof(tx_hash)
                self.assertEqual('MerkleProof', merkle_proof['Type'])
                self.assertEqual(0, merkle_proof['BlockHeight'])
                if pre_tx_root == 0:
                    pre_tx_root = merkle_proof['TransactionsRoot']
                else:
                    self.assertEqual(pre_tx_root, merkle_proof['TransactionsRoot'])
                    pre_tx_root = merkle_proof['TransactionsRoot']
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_send_raw_transaction(self):
        b58_from_address = acct2.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, 1,
                                                            b58_from_address, 20000, 500)
        tx.sign_transaction(acct2)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(tx_hash, tx.hash256_explorer())
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_send_raw_transaction_pre_exec(self):
        random_pk = get_random_hex_str(64)
        random_acct = Account(random_pk)
        b58_address_1 = acct2.get_address_base58()
        random_b58_address = random_acct.get_address_base58()
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_address_1, random_b58_address, 2, b58_address_1,
                                                            20000, 500)
        tx.sign_transaction(acct2)
        try:
            result = sdk.rpc.send_raw_transaction_pre_exec(tx)
            self.assertEqual(result['Result'], '01')
            self.assertEqual(result['Gas'], 20000)
            self.assertEqual(result['State'], 1)
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    def test_get_memory_pool_tx_count(self):
        tx_count = sdk.rpc.get_memory_pool_tx_count()
        self.assertGreaterEqual(tx_count, [0, 0])

    def test_get_memory_pool_tx_state(self):
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
