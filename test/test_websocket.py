#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import asyncio
import time
import unittest

from random import choice

from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.network.websocket import WebsocketClient
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.native_contract.asset import Asset
from ontology.network.connect_manager import TEST_WS_ADDRESS, TEST_RPC_ADDRESS
from ontology.utils.contract_data_parser import ContractDataParser
from ontology.utils.contract_event_parser import ContractEventParser

remote_rpc_address = choice(TEST_RPC_ADDRESS)
websocket_address = choice(TEST_WS_ADDRESS)
websocket_client = WebsocketClient()
websocket_client.set_address(websocket_address)


class TestWebsocketClient(unittest.TestCase):
    @staticmethod
    async def heartbeat_case():
        response = await websocket_client.send_heartbeat()
        await websocket_client.close_connect()
        return response

    def test_heartbeat(self):
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.heartbeat_case())
        self.assertEqual(None, response['ConstractsFilter'])
        self.assertEqual(False, response['SubscribeEvent'])
        self.assertEqual(False, response['SubscribeJsonBlock'])
        self.assertEqual(False, response['SubscribeRawBlock'])
        self.assertEqual(False, response['SubscribeBlockTxHashs'])

    @staticmethod
    async def oep4_transfer(hex_contract_address, from_acct, b58_to_address, value):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(hex_contract_address)
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.transfer(from_acct, b58_to_address, value, from_acct, gas_limit, gas_price)
        return tx_hash

    @staticmethod
    async def subscribe_oep4_transfer_event(hex_contract_address):
        response = await websocket_client.subscribe(hex_contract_address, True, False, False, False)
        event = await websocket_client.recv_subscribe_info()
        return response, event

    async def subscribe_oep4_case(self, event_loop):
        private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        from_acct = Account(private_key1, SignatureScheme.SHA256withECDSA)
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        b58_to_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        value = 10
        subscribe_task = event_loop.create_task(TestWebsocketClient.subscribe_oep4_transfer_event(hex_contract_address))
        transfer_task = event_loop.create_task(
            TestWebsocketClient.oep4_transfer(hex_contract_address, from_acct, b58_to_address, value))

        try:
            response, event = await asyncio.wait_for(subscribe_task, timeout=10)
            self.assertEqual([hex_contract_address], response['ConstractsFilter'])
            self.assertEqual(True, response['SubscribeEvent'])
            self.assertEqual(False, response['SubscribeJsonBlock'])
            self.assertEqual(False, response['SubscribeRawBlock'])
            self.assertEqual(False, response['SubscribeBlockTxHashs'])
            self.assertEqual(64, len(event['TxHash']))
            notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
            notify = ContractDataParser.parser_oep4_transfer_notify(notify)
            self.assertEqual(hex_contract_address, notify['ContractAddress'])
            self.assertEqual('transfer', notify['States'][0])
            self.assertEqual(from_acct.get_address_base58(), notify['States'][1])
            self.assertEqual(b58_to_address, notify['States'][2])
            self.assertEqual(value, notify['States'][3])
            tx_hash = await transfer_task
            self.assertEqual(64, len(tx_hash))
        except asyncio.TimeoutError:
            pass
        await websocket_client.close_connect()

    def test_subscribe(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.subscribe_oep4_case(event_loop))

    @staticmethod
    async def get_connection_count_case():
        response = await websocket_client.get_connection_count()
        await websocket_client.close_connect()
        return response

    def test_get_connection_count(self):
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_connection_count_case())
        self.assertGreater(response, 0)

    @staticmethod
    async def get_smart_contract_event_by_tx_hash_case(tx_hash):
        response = await websocket_client.get_smart_contract_event_by_tx_hash(tx_hash)
        await websocket_client.close_connect()
        return response

    def test_get_smart_contract_event_by_tx_hash(self):
        tx_hash = '7bc2dd4693996133c15e6349c3f8dd1edeba2fcd3219c8bc2b854c939337c8ff'
        event_loop = asyncio.get_event_loop()
        response = event_loop.run_until_complete(TestWebsocketClient.get_smart_contract_event_by_tx_hash_case(tx_hash))
        self.assertEqual(500, response['GasPrice'])
        self.assertEqual(21000000, response['GasLimit'])
        self.assertEqual(208, response['TxType'])

    @staticmethod
    async def get_block_height_case():
        response = await websocket_client.get_block_height()
        await websocket_client.close_connect()
        return response

    def test_get_block_height(self):
        height = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_block_height_case())
        self.assertGreater(height, 556748)

    @staticmethod
    async def get_block_hash_by_height_case(height):
        response = await websocket_client.get_block_hash_by_height(height)
        await websocket_client.close_connect()
        return response

    def test_get_block_hash_by_height(self):
        height = 1024
        response = asyncio.get_event_loop().run_until_complete(
            TestWebsocketClient.get_block_hash_by_height_case(height))
        self.assertEqual('2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f', response)

    @staticmethod
    async def get_block_by_height_case(height):
        response = await websocket_client.get_block_by_height(height)
        await websocket_client.close_connect()
        return response

    def test_get_block_by_height(self):
        height = 1024
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_block_by_height_case(height))
        self.assertEqual('2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f', response['Hash'])
        self.assertEqual(height, response['Header']['Height'])

    @staticmethod
    async def get_block_by_hash_case(block_hash):
        response = await websocket_client.get_block_by_hash(block_hash)
        await websocket_client.close_connect()
        return response

    def test_get_block_by_hash(self):
        block_hash = '2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f'
        response = asyncio.get_event_loop().run_until_complete(TestWebsocketClient.get_block_by_hash_case(block_hash))
        self.assertEqual(block_hash, response['Hash'])
        self.assertEqual(1024, response['Header']['Height'])

    @staticmethod
    async def send_raw_transaction_and_query_tx_case(tx):
        tx_hash = await websocket_client.send_raw_transaction(tx)
        await asyncio.sleep(6)
        event = await websocket_client.get_smart_contract_event_by_tx_hash(tx_hash)
        await websocket_client.close_connect()
        return tx_hash, event

    def test_send_raw_transaction(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx = Asset.new_transfer_transaction('ong', b58_from_address, b58_to_address, amount, b58_from_address,
                                            gas_limit, gas_price)
        sdk = OntologySdk()
        tx = sdk.sign_transaction(tx, acct)
        event_loop = asyncio.get_event_loop()
        tx_hash, event = event_loop.run_until_complete(TestWebsocketClient.send_raw_transaction_and_query_tx_case(tx))
        self.assertEqual(tx_hash, event['TxHash'])
        self.assertEqual(1, event['State'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])


if __name__ == '__main__':
    unittest.main()
