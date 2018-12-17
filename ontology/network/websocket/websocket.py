#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import List
from sys import maxsize
from websockets import client
from Cryptodome.Random.random import randint

from ontology.common.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException


class WebsocketClient(object):
    def __init__(self, url: str = ''):
        self.__url = url
        self.__id = 0
        self.__ws_client = None

    def __generate_ws_id(self):
        if self.__id == 0:
            self.__id = randint(0, maxsize)
        return self.__id

    def set_address(self, address):
        self.__url = address

    async def connect(self):
        self.__ws_client = await client.connect(self.__url)

    async def __send_recv(self, msg: dict, is_full: bool):
        await self.__ws_client.send(json.dumps(msg))
        response = await self.__ws_client.recv()
        response = json.loads(response)
        if is_full:
            return response
        if response['Error'] != 0:
            raise SDKException(ErrorCode.other_error(response.get('Result', '')))
        return response.get('Result', dict())

    async def send_heartbeat(self, is_full: bool = False):
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='heartbeat', Version='V1.0.0', Id=self.__id)
        return await self.__send_recv(msg, is_full)

    async def get_connection_count(self, is_full: bool = False) -> int:
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='getconnectioncount', Id=self.__id, Version='1.0.0')
        return await self.__send_recv(msg, is_full)

    async def get_transaction_by_tx_hash(self, tx_hash: str, is_full: bool = False) -> dict:
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='gettransaction', Id=self.__id, Version='1.0.0', Hash=tx_hash, Raw=0)
        return await self.__send_recv(msg, is_full)

    async def get_block_height(self, is_full: bool = False) -> dict:
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='getblockheight', Id=self.__id, Version='1.0.0')
        return await self.__send_recv(msg, is_full)

    async def get_block_hash_by_height(self, height: int, is_full: bool = False):
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='getblockhash', Id=self.__id, Version='1.0.0', Height=height)
        return await self.__send_recv(msg, is_full)

    async def get_block_by_height(self, height: int, is_full: bool = False) -> dict:
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='getblockbyheight', Version='1.0.0', Id=self.__id, Raw=0, Height=height)
        return await self.__send_recv(msg, is_full)

    async def get_block_by_hash(self, block_hash: str, is_full: bool = False) -> dict:
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='getblockbyhash', Version='1.0.0', Id=self.__id, Hash=block_hash)
        return await self.__send_recv(msg, is_full)

    async def subscribe(self, contract_address_list: List[str], is_event: bool = False, is_json_block: bool = False,
                        is_raw_block: bool = False, is_tx_hash: bool = False, is_full: bool = False) -> dict:
        if self.__id == 0:
            self.__id = self.__generate_ws_id()
        msg = dict(Action='subscribe', Version='1.0.0', Id=self.__id, ConstractsFilter=contract_address_list,
                   SubscribeEvent=is_event, SubscribeJsonBlock=is_json_block, SubscribeRawBlock=is_raw_block,
                   SubscribeBlockTxHashs=is_tx_hash)
        return await self.__send_recv(msg, is_full)

    async def send_raw_transaction(self, tx: Transaction, is_full: bool = False):
        tx_data = tx.serialize(is_hex=True).decode('ascii')
        msg = dict(Action='sendrawtransaction', Version='1.0.0', Id=self.__id, PreExec=0, Data=tx_data)
        return await self.__send_recv(msg, is_full)
