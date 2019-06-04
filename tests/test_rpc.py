#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2018-2019 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
import unittest

from ontology.utils.contract import Data
from ontology.common.address import Address
from ontology.exception.exception import SDKException

from tests import sdk, acct1, acct2, acct3, acct4, not_panic_exception


class TestRpcClient(unittest.TestCase):
    def setUp(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        multi_address = Address.from_multi_pub_keys(2, pub_keys)
        self.address_list = [acct1.get_address_base58(), acct2.get_address_base58(), acct3.get_address_base58(),
                             acct4.get_address_base58(), multi_address.b58encode()]

    @not_panic_exception
    def test_get_version(self):
        version = sdk.rpc.get_version()
        self.assertTrue(isinstance(version, str))
        if version != '':
            self.assertIn('v', version)

    @not_panic_exception
    def test_get_connection_count(self):
        count = sdk.rpc.get_connection_count()
        self.assertGreaterEqual(count, 0)

    @not_panic_exception
    def test_get_gas_price(self):
        price = sdk.rpc.get_gas_price()
        self.assertGreater(price, 0)

    @not_panic_exception
    def test_get_network_id(self):
        network_id = sdk.rpc.get_network_id()
        self.assertEqual(2, network_id)
        try:
            sdk.rpc.connect_to_main_net()
            network_id = sdk.rpc.get_network_id()
            self.assertEqual(1, network_id)
        finally:
            sdk.rpc.connect_to_test_net()

    @not_panic_exception
    def test_get_block_by_hash(self):
        block_hash = '44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c'
        block = sdk.rpc.get_block_by_hash(block_hash)
        self.assertEqual(block['Hash'], block_hash)

    @not_panic_exception
    def test_get_block_by_height(self):
        height = 0
        block = sdk.rpc.get_block_by_height(height)
        self.assertEqual(block['Header']['Height'], height)

    @not_panic_exception
    def test_get_block_height(self):
        height = sdk.rpc.get_block_height()
        self.assertGreater(height, 103712)

    @not_panic_exception
    def test_get_block_height_by_tx_hash(self):
        tx_hash_list = ['1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79',
                        '029b0a7f058cca73ed05651d7b5536eff8be5271a39452e91a1e758d0c36aecb',
                        'e96994829aa9f6cf402da56f427491458a730df1c3ff9158ef1cbed31b8628f2',
                        '0000000000000000000000000000000000000000000000000000000000000000']
        height_list = [0, 1024, 564235, -1]
        for index, tx_hash in enumerate(tx_hash_list):
            if height_list[index] == -1:
                self.assertRaises(SDKException, sdk.rpc.get_block_height_by_tx_hash, tx_hash)
                continue
            height = sdk.rpc.get_block_height_by_tx_hash(tx_hash)
            self.assertEqual(height_list[index], height)

    @not_panic_exception
    def test_get_block_count_by_tx_hash(self):
        tx_hash_lst = ['7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e',
                       'e96994829aa9f6cf402da56f427491458a730df1c3ff9158ef1cbed31b8628f2']
        count_lst = [1, 564236]
        for index, tx_hash in enumerate(tx_hash_lst):
            block_count = sdk.rpc.get_block_count_by_tx_hash(tx_hash)
            self.assertEqual(count_lst[index], block_count)

    @not_panic_exception
    def test_get_current_block_hash(self):
        current_block_hash = sdk.rpc.get_current_block_hash()
        self.assertEqual(len(current_block_hash), 64)

    @not_panic_exception
    def test_get_block_hash_by_height(self):
        height = 0
        block_hash = sdk.rpc.get_block_hash_by_height(height)
        self.assertEqual(len(block_hash), 64)

    @not_panic_exception
    def test_get_balance(self):
        for address in self.address_list:
            balance = sdk.rpc.get_balance(address)
            self.assertTrue(isinstance(balance, dict))
            self.assertGreaterEqual(balance['ONT'], 0)
            self.assertGreaterEqual(balance['ONG'], 0)

    @not_panic_exception
    def test_get_unbound_ong(self):
        for address in self.address_list:
            self.assertEqual(sdk.rpc.get_unbound_ong(address), sdk.native_vm.ong().unbound(address))

    @not_panic_exception
    def test_get_grant_ong(self):
        grant_ong = sdk.rpc.get_grant_ong('ASaZccBEzdjZQe2p9d1rcyNQqHrv82UmSg')
        self.assertGreaterEqual(grant_ong, 0)

    @not_panic_exception
    def test_get_allowance(self):
        base58_address = 'AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA'
        allowance = sdk.rpc.get_allowance('ong', base58_address, base58_address)
        self.assertEqual(allowance, '0')

    @not_panic_exception
    def test_get_storage(self):
        hex_contract_address = "0100000000000000000000000000000000000000"
        key = "746f74616c537570706c79"
        value = sdk.rpc.get_storage(hex_contract_address, key)
        value = Data.to_int(value)
        self.assertEqual(1000000000, value)

    @not_panic_exception
    def test_get_smart_contract_event_by_tx_hash(self):
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        event = sdk.rpc.get_contract_event_by_tx_hash(tx_hash)
        self.assertEqual(event['TxHash'], tx_hash)

    @not_panic_exception
    def test_get_smart_contract_event_by_height(self):
        height_lst = [0, 1309737]
        event_len_lst = [10, 0]
        for index, h in enumerate(height_lst):
            event_list = sdk.rpc.get_contract_event_by_height(h)
            self.assertEqual(event_len_lst[index], len(event_list))

    @not_panic_exception
    def test_get_smart_contract_event_by_count(self):
        cnt_lst = [1, 1309738]
        event_len_lst = [10, 0]
        for index, cnt in enumerate(cnt_lst):
            event_list = sdk.rpc.get_contract_event_by_count(cnt)
            self.assertEqual(event_len_lst[index], len(event_list))

    @not_panic_exception
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
                event_list = sdk.rpc.get_contract_event_by_height(height)
                self.assertGreaterEqual(len(event_list), 0)

    @not_panic_exception
    def test_get_transaction_by_tx_hash(self):
        tx_hash = '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74'
        tx = sdk.rpc.get_transaction_by_tx_hash(tx_hash)
        self.assertEqual(tx['Hash'], tx_hash)

    @not_panic_exception
    def test_get_smart_contract(self):
        address_list = ['1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9', '0100000000000000000000000000000000000000']
        info_list = [[True, 'DINGXIN', 'A sample of OEP4'], [True, 'Ontology Team', 'Ontology Network ONT Token']]
        for index, address in enumerate(address_list):
            contract = sdk.rpc.get_contract(address)
            self.assertEqual(info_list[index][0], contract['NeedStorage'])
            self.assertEqual(info_list[index][1], contract['Author'])
            self.assertEqual(info_list[index][2], contract['Description'])
        try:
            sdk.rpc.connect_to_main_net()
            contract = sdk.rpc.get_contract('6c80f3a5c183edee7693a038ca8c476fb0d6ac91')
            self.assertEqual('Youle_le_service@fosun.com', contract.get('Email', ''))
            self.assertEqual('chentao', contract.get('Author', ''))
        finally:
            sdk.rpc.connect_to_test_net()

    @not_panic_exception
    def test_get_merkle_proof(self):
        pre_tx_root = 0
        tx_hash_list = ['12943957b10643f04d89938925306fa342cec9d32925f5bd8e9ea7ce912d16d3',
                        '1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79',
                        '5d09b2b9ba302e9da8b9472ef10c824caf998e940cc5a73d7da16971d64c0290',
                        '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74',
                        '7842ed25e4f028529e666bcecda2795ec49d570120f82309e3d5b94f72d30ebb',
                        '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e']
        for tx_hash in tx_hash_list:
            merkle_proof = sdk.rpc.get_merkle_proof(tx_hash)
            self.assertEqual('MerkleProof', merkle_proof['Type'])
            self.assertEqual(0, merkle_proof['BlockHeight'])
            if pre_tx_root == 0:
                pre_tx_root = merkle_proof['TransactionsRoot']
            else:
                self.assertEqual(pre_tx_root, merkle_proof['TransactionsRoot'])
                pre_tx_root = merkle_proof['TransactionsRoot']

    @not_panic_exception
    def test_send_raw_transaction(self):
        b58_from_address = acct2.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        tx = sdk.native_vm.ong().new_transfer_tx(b58_from_address, b58_to_address, 1, b58_from_address, 500, 20000)
        tx.sign_transaction(acct2)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.hash256_explorer())

    @not_panic_exception
    def test_send_raw_transaction_pre_exec(self):
        b58_address = acct1.get_address_base58()
        tx = sdk.native_vm.ong().new_transfer_tx(b58_address, acct2.get_address(), 2, b58_address, 500, 20000)
        tx.sign_transaction(acct1)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertTrue(Data.to_bool(result['Result']))
        self.assertEqual(result['Gas'], 20000)
        self.assertEqual(result['State'], 1)

    @not_panic_exception
    def test_get_memory_pool_tx_count(self):
        tx_count = sdk.rpc.get_memory_pool_tx_count()
        self.assertGreaterEqual(tx_count, [0, 0])

    @not_panic_exception
    def test_get_memory_pool_tx_state(self):
        tx_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        with self.assertRaises(SDKException):
            sdk.rpc.get_memory_pool_tx_state(tx_hash)
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        b58_to_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        tx = oep4.new_transfer_tx(acct1.get_address(), b58_to_address, 10, acct1.get_address(), 500, 20000000)
        tx.sign_transaction(acct1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))
        try:
            tx_state = sdk.rpc.get_memory_pool_tx_state(tx_hash)
            self.assertTrue(isinstance(tx_state, list))
        except SDKException as e:
            self.assertEqual(59000, e.args[0])


if __name__ == '__main__':
    unittest.main()
