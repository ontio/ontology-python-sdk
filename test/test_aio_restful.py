#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from test import sdk, acct4, acct3, acct2, acct1

from ontology.common.address import Address
from ontology.account.account import Account
from ontology.network.aiorestful import AioRestful
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser
from ontology.crypto.signature_scheme import SignatureScheme


class TestAioRestful(unittest.TestCase):
    @AioRestful.runner
    async def test_get_version(self):
        version = await sdk.aio_restful.get_version()
        self.assertTrue(isinstance(version, str))
        if version != '':
            self.assertIn('v', version)

    @AioRestful.runner
    async def test_get_connection_count(self):
        count = await sdk.aio_restful.get_connection_count()
        self.assertGreaterEqual(count, 0)

    @AioRestful.runner
    async def test_get_block_height(self):
        height = await sdk.aio_restful.get_block_height()
        self.assertGreater(height, 1)

    @AioRestful.runner
    async def test_get_block_height_by_tx_hash(self):
        tx_hash_list = ['1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79',
                        '029b0a7f058cca73ed05651d7b5536eff8be5271a39452e91a1e758d0c36aecb',
                        'e96994829aa9f6cf402da56f427491458a730df1c3ff9158ef1cbed31b8628f2',
                        '0000000000000000000000000000000000000000000000000000000000000000']
        height_list = [0, 1024, 564235, -1]
        for index, tx_hash in enumerate(tx_hash_list):
            if height_list[index] == -1:
                with self.assertRaises(SDKException):
                    await sdk.aio_restful.get_block_height_by_tx_hash(tx_hash)
                continue
            height = await sdk.aio_restful.get_block_height_by_tx_hash(tx_hash)
            self.assertEqual(height_list[index], height)

    @AioRestful.runner
    async def test_get_gas_price(self):
        price = await sdk.aio_restful.get_gas_price()
        self.assertGreater(price, 0)

    @AioRestful.runner
    async def test_get_network_id(self):
        network_id = await sdk.aio_restful.get_network_id()
        self.assertEqual(network_id, 2)
        try:
            sdk.aio_restful.connect_to_main_net()
            network_id = await sdk.aio_restful.get_network_id()
            self.assertEqual(network_id, 1)
        finally:
            sdk.aio_restful.connect_to_test_net()

    @AioRestful.runner
    async def test_get_block_by_hash(self):
        block_hash = "1aae9881945b42a30072c608674687c6d9845b29c8c34f91c65081d6bc631868"
        block = await sdk.aio_restful.get_block_by_hash(block_hash)
        self.assertEqual(block['Hash'], block_hash)

    @AioRestful.runner
    async def test_get_block_by_height(self):
        height = 0
        block = await sdk.aio_restful.get_block_by_height(height)
        self.assertEqual(block['Header']['Height'], height)

    @AioRestful.runner
    async def test_get_balance(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        multi_address = Address.address_from_multi_pub_keys(2, pub_keys)
        address_list = [acct1.get_address_base58(), acct2.get_address_base58(), acct3.get_address_base58(),
                        acct4.get_address_base58(), multi_address.b58encode()]
        for address in address_list:
            balance = await sdk.aio_restful.get_balance(address)
            self.assertTrue(isinstance(balance, dict))
            self.assertGreaterEqual(balance['ONT'], 0)
            self.assertGreaterEqual(balance['ONG'], 0)

    @AioRestful.runner
    async def test_get_grant_ong(self):
        b58_address = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6'
        grant_ong = await sdk.aio_restful.get_grant_ong(b58_address)
        self.assertGreaterEqual(grant_ong, 0)

    @AioRestful.runner
    async def test_get_smart_contract(self):
        address_list = ['1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9', '0100000000000000000000000000000000000000']
        info_list = [[True, 'DINGXIN', 'A sample of OEP4'], [True, 'Ontology Team', 'Ontology Network ONT Token']]
        for index, address in enumerate(address_list):
            contract = await sdk.aio_restful.get_contract(address)
            self.assertEqual(info_list[index][0], contract['NeedStorage'])
            self.assertEqual(info_list[index][1], contract['Author'])
            self.assertEqual(info_list[index][2], contract['Description'])
        try:
            sdk.aio_restful.connect_to_main_net()
            contract = await sdk.aio_restful.get_contract('6c80f3a5c183edee7693a038ca8c476fb0d6ac91')
            self.assertEqual('Youle_le_service@fosun.com', contract.get('Email', ''))
            self.assertEqual('chentao', contract.get('Author', ''))
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])
        finally:
            sdk.aio_restful.connect_to_test_net()

    @AioRestful.runner
    async def test_get_smart_contract_event_by_height(self):
        height_list = [0, 1309737]
        len_list = [10, 0]
        for index, height in enumerate(height_list):
            event_list = await sdk.aio_restful.get_contract_event_by_height(height)
            self.assertEqual(len_list[index], len(event_list))

    @AioRestful.runner
    async def test_get_storage(self):
        contract_address = "0100000000000000000000000000000000000000"
        key = "746f74616c537570706c79"
        value = await sdk.aio_restful.get_storage(contract_address, key)
        value = ContractDataParser.to_int(value)
        self.assertEqual(1000000000, value)

    @AioRestful.runner
    async def test_get_allowance(self):
        base58_address = 'AKDFapcoUhewN9Kaj6XhHusurfHzUiZqUA'
        allowance = await sdk.aio_restful.get_allowance('ong', base58_address, base58_address)
        self.assertEqual(allowance, '0')

    @AioRestful.runner
    async def test_get_transaction_by_tx_hash(self):
        tx_hash = "65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74"
        tx = await sdk.aio_restful.get_transaction_by_tx_hash(tx_hash)
        self.assertEqual(tx['Hash'], tx_hash)

    @AioRestful.runner
    async def test_send_raw_transaction(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, 1,
                                                            b58_from_address, 20000, 500)
        tx.sign_transaction(acct)
        tx_hash = await sdk.aio_restful.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.hash256_explorer())

    @AioRestful.runner
    async def test_send_raw_transaction_pre_exec(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, 1,
                                                            b58_from_address, 20000, 500)
        tx.sign_transaction(acct)
        result = await sdk.aio_restful.send_raw_transaction_pre_exec(tx)
        self.assertEqual('01', result['Result'])
        self.assertEqual(20000, result['Gas'])
        self.assertEqual(1, result['State'])

    @AioRestful.runner
    async def test_get_merkle_proof(self):
        pre_tx_root = 0
        tx_hash_list = ['12943957b10643f04d89938925306fa342cec9d32925f5bd8e9ea7ce912d16d3',
                        '1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79',
                        '5d09b2b9ba302e9da8b9472ef10c824caf998e940cc5a73d7da16971d64c0290',
                        '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74',
                        '7842ed25e4f028529e666bcecda2795ec49d570120f82309e3d5b94f72d30ebb',
                        '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e']
        try:
            for tx_hash in tx_hash_list:
                merkle_proof = await sdk.aio_restful.get_merkle_proof(tx_hash)
                self.assertEqual('MerkleProof', merkle_proof['Type'])
                self.assertEqual(0, merkle_proof['BlockHeight'])
                if pre_tx_root == 0:
                    pre_tx_root = merkle_proof['TransactionsRoot']
                else:
                    self.assertEqual(pre_tx_root, merkle_proof['TransactionsRoot'])
                    pre_tx_root = merkle_proof['TransactionsRoot']
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])

    @AioRestful.runner
    async def test_get_memory_pool_tx_count(self):
        tx_count = await sdk.aio_restful.get_memory_pool_tx_count()
        self.assertGreaterEqual(tx_count, [0, 0])

    @AioRestful.runner
    async def test_get_memory_pool_tx_state(self):
        tx_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        with self.assertRaises(SDKException):
            await sdk.aio_restful.get_memory_pool_tx_state(tx_hash)
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        b58_from_address = acct4.get_address_base58()
        b58_to_address = acct3.get_address_base58()
        tx = oep4.transfer(b58_from_address, b58_to_address, 10, b58_from_address, 20000000, 500)
        tx.sign_transaction(acct4)
        tx_hash = await sdk.aio_restful.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))
        try:
            tx_state = await sdk.aio_restful.get_memory_pool_tx_state(tx_hash)
            self.assertGreaterEqual(tx_state[0]['Height'], 0)
            self.assertGreaterEqual(tx_state[1]['Height'], 0)
        except SDKException:
            pass


if __name__ == '__main__':
    unittest.main()
