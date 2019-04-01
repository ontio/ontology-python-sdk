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

import inspect


def ws_runner(f):
    def wrapper(*args, **kwargs):
        if inspect.iscoroutinefunction(f):
            future = f(*args, **kwargs)
        else:
            coroutine = asyncio.coroutine(f)
            future = coroutine(*args, **kwargs)
        asyncio.get_event_loop().run_until_complete(future)

    return wrapper


class TestWebsocketClient(unittest.TestCase):
    @ws_runner
    async def test_heartbeat(self):
        response = await sdk.websocket.send_heartbeat()
        await sdk.websocket.close_connect()
        self.assertEqual(None, response['ContractsFilter'])
        self.assertEqual(False, response['SubscribeEvent'])
        self.assertEqual(False, response['SubscribeJsonBlock'])
        self.assertEqual(False, response['SubscribeRawBlock'])
        self.assertEqual(False, response['SubscribeBlockTxHashs'])

    @ws_runner
    async def test_subscribe(self):
        oep4 = sdk.neo_vm.oep4()
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4.hex_contract_address = hex_contract_address
        response = await sdk.websocket.subscribe(hex_contract_address, True, False, False, False)
        self.assertEqual([hex_contract_address], response['ContractsFilter'])
        self.assertEqual(True, response['SubscribeEvent'])
        self.assertEqual(False, response['SubscribeJsonBlock'])
        self.assertEqual(False, response['SubscribeRawBlock'])
        from_acct = acct1
        b58_to_address = acct2.get_address_base58()
        value = 10
        tx_hash = oep4.transfer(from_acct, b58_to_address, value, acct3, 20000000, 500)
        self.assertEqual(64, len(tx_hash))
        try:
            event = await asyncio.wait_for(sdk.websocket.recv_subscribe_info(), timeout=10)
            self.assertEqual(False, response['SubscribeBlockTxHashs'])
            self.assertEqual(64, len(event['TxHash']))
            notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
            notify = ContractDataParser.parse_addr_addr_int_notify(notify)
            self.assertEqual(hex_contract_address, notify['ContractAddress'])
            self.assertEqual('transfer', notify['States'][0])
            self.assertEqual(from_acct.get_address_base58(), notify['States'][1])
            self.assertEqual(b58_to_address, notify['States'][2])
            self.assertEqual(value, notify['States'][3])
        except asyncio.TimeoutError:
            pass
        finally:
            await sdk.websocket.close_connect()

    @ws_runner
    async def test_get_connection_count(self):
        response = await sdk.websocket.get_connection_count()
        await sdk.websocket.close_connect()
        self.assertGreater(response, 0)

    @ws_runner
    async def test_get_session_count(self):
        count = await sdk.websocket.get_session_count()
        await sdk.websocket.close_connect()
        self.assertGreaterEqual(count, 1)

    @ws_runner
    async def test_get_balance(self):
        b58_address = acct4.get_address_base58()
        balance = await sdk.websocket.get_balance(b58_address)
        await sdk.websocket.close_connect()
        self.assertGreaterEqual(balance['ont'], 1)
        self.assertGreaterEqual(balance['ong'], 1)

    @ws_runner
    async def test_get_storage(self):
        hex_contract_address = '0100000000000000000000000000000000000000'
        key = '746f74616c537570706c79'
        storage = await sdk.websocket.get_storage(hex_contract_address, key)
        await sdk.websocket.close_connect()
        value = ContractDataParser.to_int(storage)
        self.assertEqual(1000000000, value)

    @ws_runner
    async def test_get_smart_contract(self):
        hex_contract_address = '0100000000000000000000000000000000000000'
        response = await sdk.websocket.get_smart_contract(hex_contract_address)
        self.assertEqual(True, response['NeedStorage'])
        self.assertEqual('ONT', response['Name'])
        self.assertEqual('1.0', response['CodeVersion'])
        self.assertEqual('Ontology Team', response['Author'])
        self.assertEqual('contact@ont.io', response['Email'])
        self.assertEqual('Ontology Network ONT Token', response['Description'])
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        response = await sdk.websocket.get_smart_contract(hex_contract_address)
        self.assertEqual(True, response['NeedStorage'])
        self.assertEqual('DINGXIN', response['Author'])
        self.assertEqual('A sample of OEP4', response['Description'])
        await sdk.websocket.close_connect()

    @ws_runner
    async def test_get_smart_contract_event_by_tx_hash(self):
        tx_hash = '7bc2dd4693996133c15e6349c3f8dd1edeba2fcd3219c8bc2b854c939337c8ff'
        event_loop = asyncio.get_event_loop()
        response = await sdk.websocket.get_smart_contract_event_by_tx_hash(tx_hash)
        await sdk.websocket.close_connect()
        self.assertEqual(tx_hash, response['TxHash'])
        self.assertEqual(1, response['State'])
        self.assertEqual(1, len(response['Notify']))

    @ws_runner
    async def test_get_smart_contract_event_by_height(self):
        height = 0
        event_list = await sdk.websocket.get_smart_contract_event_by_height(height)
        self.assertEqual(10, len(event_list))
        for tx in event_list:
            self.assertEqual(64, len(tx['TxHash']))
            self.assertEqual(1, tx['State'])
            self.assertEqual(0, tx['GasConsumed'])
            self.assertTrue(isinstance(tx['Notify'], list))
        height = 1309737
        event_list = await sdk.websocket.get_smart_contract_event_by_height(height)
        self.assertEqual(0, len(event_list))
        await sdk.websocket.close_connect()

    @ws_runner
    async def test_get_block_height(self):
        try:
            height = await sdk.websocket.get_block_height()
            self.assertGreater(height, 556748)
        finally:
            await sdk.websocket.close_connect()

    @ws_runner
    async def test_get_block_height_by_tx_hash(self):
        try:
            tx_hash = '1ebde66ec3f309dad20a63f8929a779162a067c36ce7b00ffbe8f4cfc8050d79'
            height = await sdk.websocket.get_block_height_by_tx_hash(tx_hash)
            self.assertEqual(0, height)
            tx_hash = '029b0a7f058cca73ed05651d7b5536eff8be5271a39452e91a1e758d0c36aecb'
            height = await sdk.websocket.get_block_height_by_tx_hash(tx_hash)
            self.assertEqual(1024, height)
        finally:
            await sdk.websocket.close_connect()

    @ws_runner
    async def test_get_block_hash_by_height(self):
        try:
            response = await sdk.websocket.get_block_hash_by_height(1024)
            self.assertEqual('2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f', response)
        finally:
            await sdk.websocket.close_connect()

    @staticmethod
    async def get_block_by_height_case(height):
        response = await sdk.websocket.get_block_by_height(height)
        await sdk.websocket.close_connect()
        return response

    @ws_runner
    async def test_get_block_by_height(self):
        try:
            height = 1024
            response = await sdk.websocket.get_block_by_height(height)
            self.assertEqual('2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f', response['Hash'])
            self.assertEqual(height, response['Header']['Height'])
        finally:
            sdk.websocket.close_connect()

    @ws_runner
    async def test_get_block_by_hash(self):
        try:
            block_hash = '2e36db16c8faf0ea0f84172256e79b78a3d8d076114fe8aaa302794668b9396f'
            response = await sdk.websocket.get_block_by_hash(block_hash)
            self.assertEqual(block_hash, response['Hash'])
            self.assertEqual(1024, response['Header']['Height'])
        finally:
            await sdk.websocket.close_connect()

    @ws_runner
    async def test_send_raw_transaction(self):
        b58_from_address = acct1.get_address_base58()
        b58_to_address = acct2.get_address_base58()
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, 1,
                                                            b58_from_address, 20000, 500)
        tx.sign_transaction(acct1)
        tx_hash = await sdk.websocket.send_raw_transaction(tx)
        await asyncio.sleep(6)
        event = await sdk.websocket.get_smart_contract_event_by_tx_hash(tx_hash)
        await sdk.websocket.close_connect()
        self.assertEqual(tx_hash, event['TxHash'])
        self.assertEqual(1, event['State'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][0]['ContractAddress'])
        self.assertEqual('0200000000000000000000000000000000000000', event['Notify'][1]['ContractAddress'])

    @ws_runner
    async def test_send_raw_transaction_pre_exec(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_from_address = acct.get_address_base58()
        b58_to_address = 'AW352JufVwuZReSt7SCQpbYqrWeuERUNJr'
        tx = sdk.native_vm.asset().new_transfer_transaction('ong', b58_from_address, b58_to_address, 1,
                                                            b58_from_address, 20000, 500)
        tx.sign_transaction(acct)
        response = await sdk.websocket.send_raw_transaction_pre_exec(tx)
        self.assertEqual('01', response['Result'])
        self.assertEqual(1, response['State'])

    @ws_runner
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
                merkle_proof = await sdk.websocket.get_merkle_proof(tx_hash)
                self.assertEqual('MerkleProof', merkle_proof['Type'])
                self.assertEqual(0, merkle_proof['BlockHeight'])
                if pre_tx_root == 0:
                    pre_tx_root = merkle_proof['TransactionsRoot']
                else:
                    self.assertEqual(pre_tx_root, merkle_proof['TransactionsRoot'])
                    pre_tx_root = merkle_proof['TransactionsRoot']
        except SDKException as e:
            self.assertTrue('ConnectTimeout' in e.args[1])
        finally:
            await sdk.websocket.close_connect()


if __name__ == '__main__':
    unittest.main()
