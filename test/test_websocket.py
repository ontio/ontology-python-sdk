#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import unittest

from test import sdk, acct1, acct2, acct3, acct4

from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.utils.contract_event import ContractEventParser


class TestWebsocketClient(unittest.TestCase):
    @staticmethod
    async def heartbeat_case():
        response = await sdk.websocket.send_heartbeat()
        await sdk.websocket.close_connect()
        return response

    def test_heartbeat(self):
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.heartbeat_case())
        self.assertEqual(None, response['ContractsFilter'])
        self.assertEqual(False, response['SubscribeEvent'])
        self.assertEqual(False, response['SubscribeJsonBlock'])
        self.assertEqual(False, response['SubscribeRawBlock'])
        self.assertEqual(False, response['SubscribeBlockTxHashs'])

    @staticmethod
    async def oep4_transfer(hex_contract_address, from_acct, b58_to_address, value):
        oep4 = sdk.neo_vm.oep4()
        oep4.hex_contract_address = hex_contract_address
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.transfer(from_acct, b58_to_address, value, acct3, gas_limit, gas_price)
        return tx_hash

    @staticmethod
    async def subscribe_oep4_transfer_event(hex_contract_address):
        response = await sdk.websocket.subscribe(hex_contract_address, True, False, False, False)
        event = await sdk.websocket.recv_subscribe_info()
        return response, event

    async def subscribe_oep4_case(self, event_loop):
        from_acct = acct1
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        b58_to_address = acct2.get_address_base58()
        value = 10
        subscribe_task = event_loop.create_task(TestWebsocketClient.subscribe_oep4_transfer_event(hex_contract_address))
        transfer_task = event_loop.create_task(
            TestWebsocketClient.oep4_transfer(hex_contract_address, from_acct, b58_to_address, value))

        try:
            response, event = await asyncio.wait_for(subscribe_task, timeout=10)
            self.assertEqual([hex_contract_address], response['ContractsFilter'])
            self.assertEqual(True, response['SubscribeEvent'])
            self.assertEqual(False, response['SubscribeJsonBlock'])
            self.assertEqual(False, response['SubscribeRawBlock'])
            self.assertEqual(False, response['SubscribeBlockTxHashs'])
            self.assertEqual(64, len(event['TxHash']))
            notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
            notify = ContractDataParser.parse_addr_addr_int_notify(notify)
            self.assertEqual(hex_contract_address, notify['ContractAddress'])
            self.assertEqual('transfer', notify['States'][0])
            self.assertEqual(from_acct.get_address_base58(), notify['States'][1])
            self.assertEqual(b58_to_address, notify['States'][2])
            self.assertEqual(value, notify['States'][3])
            tx_hash = await transfer_task
            self.assertEqual(64, len(tx_hash))
        except asyncio.TimeoutError:
            pass
        await sdk.websocket.close_connect()

    def test_subscribe(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.subscribe_oep4_case(event_loop))

    @staticmethod
    async def get_connection_count_case():
        response = await sdk.websocket.get_connection_count()
        await sdk.websocket.close_connect()
        return response

    def test_get_connection_count(self):
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_connection_count_case())
        self.assertGreater(response, 0)

    @staticmethod
    async def get_session_count():
        response = await sdk.websocket.get_session_count()
        await sdk.websocket.close_connect()
        return response

    def test_get_session_count(self):
        event_loop = asyncio.get_event_loop()
        count = event_loop.run_until_complete(TestWebsocketClient.get_session_count())
        self.assertGreaterEqual(count, 1)

    @staticmethod
    async def get_balance(b58_address: str):
        if not isinstance(b58_address, str):
            raise SDKException(ErrorCode.other_error('Invalid base58 encode address.'))
        balance = await sdk.websocket.get_balance(b58_address)
        return balance

    def test_get_balance(self):
        b58_address = acct4.get_address_base58()
        event_loop = asyncio.get_event_loop()
        balance = event_loop.run_until_complete(TestWebsocketClient.get_balance(b58_address))
        self.assertGreaterEqual(balance['ont'], 1)
        self.assertGreaterEqual(balance['ong'], 1)

    @staticmethod
    async def get_storage(hex_contract_address: str, key: str):
        storage = await sdk.websocket.get_storage(hex_contract_address, key)
        await sdk.websocket.close_connect()
        return storage

    def test_get_storage(self):
        hex_contract_address = '0100000000000000000000000000000000000000'
        key = '746f74616c537570706c79'
        event_loop = asyncio.get_event_loop()
        value = event_loop.run_until_complete(TestWebsocketClient.get_storage(hex_contract_address, key))
        value = ContractDataParser.to_int(value)
        self.assertEqual(1000000000, value)

    @staticmethod
    async def get_smart_contract_case(hex_contract_address: str):
        response = await sdk.websocket.get_smart_contract(hex_contract_address)
        await sdk.websocket.close_connect()
        return response

    def test_get_smart_contract(self):
        hex_contract_address = '0100000000000000000000000000000000000000'
        event_loop = asyncio.get_event_loop()
        response = event_loop.run_until_complete(TestWebsocketClient.get_smart_contract_case(hex_contract_address))
        self.assertEqual(True, response['NeedStorage'])
        self.assertEqual('ONT', response['Name'])
        self.assertEqual('1.0', response['CodeVersion'])
        self.assertEqual('Ontology Team', response['Author'])
        self.assertEqual('contact@ont.io', response['Email'])
        self.assertEqual('Ontology Network ONT Token', response['Description'])
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        response = event_loop.run_until_complete(TestWebsocketClient.get_smart_contract_case(hex_contract_address))
        self.assertEqual(True, response['NeedStorage'])
        self.assertEqual('DINGXIN', response['Author'])
        self.assertEqual('A sample of OEP4', response['Description'])

    @staticmethod
    async def get_smart_contract_event_by_tx_hash_case(tx_hash):
        response = await sdk.websocket.get_smart_contract_event_by_tx_hash(tx_hash)
        await sdk.websocket.close_connect()
        return response

    def test_get_smart_contract_event_by_tx_hash(self):
        tx_hash = '7bc2dd4693996133c15e6349c3f8dd1edeba2fcd3219c8bc2b854c939337c8ff'
        event_loop = asyncio.get_event_loop()
        response = event_loop.run_until_complete(TestWebsocketClient.get_smart_contract_event_by_tx_hash_case(tx_hash))
        self.assertEqual(tx_hash, response['TxHash'])
        self.assertEqual(1, response['State'])
        self.assertEqual(1, len(response['Notify']))

    @staticmethod
    async def get_smart_contract_event_by_height_case(height):
        response = await sdk.websocket.get_smart_contract_event_by_height(height)
        await sdk.websocket.close_connect()
        return response

    def test_get_smart_contract_event_by_height(self):
        height = 0
        event_loop = asyncio.get_event_loop()
        event_list = event_loop.run_until_complete(TestWebsocketClient.get_smart_contract_event_by_height_case(height))
        self.assertEqual(10, len(event_list))
        for tx in event_list:
            self.assertEqual(64, len(tx['TxHash']))
            self.assertEqual(1, tx['State'])
            self.assertEqual(0, tx['GasConsumed'])
            self.assertTrue(isinstance(tx['Notify'], list))
        height = 1309737
        event_list = event_loop.run_until_complete(TestWebsocketClient.get_smart_contract_event_by_height_case(height))
        self.assertEqual(0, len(event_list))

    @staticmethod
    async def get_block_height_case():
        response = await sdk.websocket.get_block_height()
        await sdk.websocket.close_connect()
        return response

    def test_get_block_height(self):
        height = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_block_height_case())
        self.assertGreater(height, 556748)

    @staticmethod
    async def get_block_height_by_tx_hash_case(tx_hash):
        response = await sdk.websocket.get_block_height_by_tx_hash(tx_hash)
        await sdk.websocket.close_connect()
        return response

    def test_get_block_height_by_tx_hash(self):
        tx_hash = '1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79'
        event_loop = asyncio.get_event_loop()
        height = event_loop.run_until_complete(TestWebsocketClient.get_block_height_by_tx_hash_case(tx_hash))
        self.assertEqual(0, height)
        tx_hash = '029b0a7f058cca73ed05651d7b5536eff8be5271a39452e91a1e758d0c36aecb'
        height = event_loop.run_until_complete(TestWebsocketClient.get_block_height_by_tx_hash_case(tx_hash))
        self.assertEqual(1024, height)

    @staticmethod
    async def get_block_hash_by_height_case(height):
        response = await sdk.websocket.get_block_hash_by_height(height)
        await sdk.websocket.close_connect()
        return response

    def test_get_block_hash_by_height(self):
        height = 1024
        response = asyncio.get_event_loop().run_until_complete(
            TestWebsocketClient.get_block_hash_by_height_case(height))
        self.assertEqual('2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f', response)

    @staticmethod
    async def get_block_by_height_case(height):
        response = await sdk.websocket.get_block_by_height(height)
        await sdk.websocket.close_connect()
        return response

    def test_get_block_by_height(self):
        height = 1024
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_block_by_height_case(height))
        self.assertEqual('2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f', response['Hash'])
        self.assertEqual(height, response['Header']['Height'])

    @staticmethod
    async def get_block_by_hash_case(block_hash):
        response = await sdk.websocket.get_block_by_hash(block_hash)
        await sdk.websocket.close_connect()
        return response

    def test_get_block_by_hash(self):
        block_hash = '2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f'
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_block_by_hash_case(block_hash))
        self.assertEqual(block_hash, response['Hash'])
        self.assertEqual(1024, response['Header']['Height'])

    @staticmethod
    async def send_raw_transaction_and_query_tx_case(tx):
        tx_hash = await sdk.websocket.send_raw_transaction(tx)
        await asyncio.sleep(6)
        event = await sdk.websocket.get_smart_contract_event_by_tx_hash(tx_hash)
        await sdk.websocket.close_connect()
        return tx_hash, event

    def test_send_raw_transaction(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, amount,
                                                            b58_from_address,
                                                            gas_limit, gas_price)
        tx.sign_transaction(acct)
        event_loop = asyncio.get_event_loop()
        tx_hash, event = event_loop.run_until_complete(TestWebsocketClient.send_raw_transaction_and_query_tx_case(tx))
        self.assertEqual(tx_hash, event['TxHash'])
        self.assertEqual(1, event['State'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])

    def test_send_raw_transaction_pre_exec(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, amount,
                                                            b58_from_address,
                                                            gas_limit, gas_price)
        tx.sign_transaction(acct)
        event_loop = asyncio.get_event_loop()
        response = event_loop.run_until_complete(sdk.websocket.send_raw_transaction_pre_exec(tx))
        self.assertEqual('01', response['Result'])
        self.assertEqual(1, response['State'])

    @staticmethod
    async def get_merkle_proof_case(tx_hash: str):
        merkle_proof = await sdk.websocket.get_merkle_proof(tx_hash)
        await sdk.websocket.close_connect()
        return merkle_proof

    def test_get_merkle_proof(self):
        event_loop = asyncio.get_event_loop()
        tx_hash_1 = '12943957b10643f04d89938925306fa342cec9d32925f5bd8e9ea7ce912d16d3'
        merkle_proof_1 = event_loop.run_until_complete(TestWebsocketClient.get_merkle_proof_case(tx_hash_1))
        self.assertEqual('MerkleProof', merkle_proof_1['Type'])
        self.assertEqual(0, merkle_proof_1['BlockHeight'])
        tx_hash_2 = '1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79'
        merkle_proof_2 = event_loop.run_until_complete(TestWebsocketClient.get_merkle_proof_case(tx_hash_2))
        self.assertEqual('MerkleProof', merkle_proof_2['Type'])
        self.assertEqual(0, merkle_proof_2['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_2['TransactionsRoot'])
        tx_hash_3 = '5d09b2b9ba302e9da8b9472ef10c824caf998e940cc5a73d7da16971d64c0290'
        merkle_proof_3 = event_loop.run_until_complete(TestWebsocketClient.get_merkle_proof_case(tx_hash_3))
        self.assertEqual('MerkleProof', merkle_proof_3['Type'])
        self.assertEqual(0, merkle_proof_3['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_3['TransactionsRoot'])
        tx_hash_4 = '65d3b2d3237743f21795e344563190ccbe50e9930520b8525142b075433fdd74'
        merkle_proof_4 = event_loop.run_until_complete(TestWebsocketClient.get_merkle_proof_case(tx_hash_4))
        self.assertEqual('MerkleProof', merkle_proof_4['Type'])
        self.assertEqual(0, merkle_proof_4['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_4['TransactionsRoot'])
        tx_hash_5 = '7842ed25e4f028529e666bcecda2795ec49d570120f82309e3d5b94f72d30ebb'
        merkle_proof_5 = event_loop.run_until_complete(TestWebsocketClient.get_merkle_proof_case(tx_hash_5))
        self.assertEqual('MerkleProof', merkle_proof_5['Type'])
        self.assertEqual(0, merkle_proof_5['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_5['TransactionsRoot'])
        tx_hash_6 = '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e'
        merkle_proof_6 = event_loop.run_until_complete(TestWebsocketClient.get_merkle_proof_case(tx_hash_6))
        self.assertEqual('MerkleProof', merkle_proof_6['Type'])
        self.assertEqual(0, merkle_proof_6['BlockHeight'])
        self.assertEqual(merkle_proof_1['TransactionsRoot'], merkle_proof_6['TransactionsRoot'])


if __name__ == '__main__':
    unittest.main()
