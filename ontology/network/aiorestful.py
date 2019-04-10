"""
Copyright (C) 2018 The ontology Authors
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

import json
import asyncio
import inspect

from typing import List
from aiohttp.client import ClientSession

from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.network.restful import Restful, RestfulMethod


class AioRestful(Restful):
    def __init__(self, url: str = '', session: ClientSession = None):
        super().__init__(url)
        self.__session = session

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session: ClientSession):
        if not isinstance(session, ClientSession):
            raise SDKException(ErrorCode.param_error)
        self.__session = session

    @staticmethod
    def runner(func):
        def wrapper(*args, **kwargs):
            if inspect.iscoroutinefunction(func):
                future = func(*args, **kwargs)
            else:
                coroutine = asyncio.coroutine(func)
                future = coroutine(*args, **kwargs)
            asyncio.get_event_loop().run_until_complete(future)

        return wrapper

    async def __post(self, url: str, data: str):
        if self.__session is None:
            async with ClientSession() as session:
                async with session.post(url, data=data, timeout=10) as response:
                    return json.loads(await response.content.read(-1))
        else:
            async with self.__session.post(url, data=data, timeout=10) as response:
                return json.loads(await response.content.read(-1))

    async def __get(self, url):
        try:
            if self.__session is None:
                async with ClientSession() as session:

                    async with session.get(url, timeout=10) as response:
                        return json.loads(await response.content.read(-1))
            else:
                async with self.__session.get(url, timeout=10) as response:
                    return json.loads(await response.content.read(-1))
        except asyncio.TimeoutError:
            raise SDKException(ErrorCode.connect_timeout(self.__url))

    async def get_version(self, is_full: bool = False):
        url = RestfulMethod.get_version(self.__url)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_connection_count(self, is_full: bool = False) -> int:
        url = RestfulMethod.get_connection_count(self.__url)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_gas_price(self, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_gas_price(self.__url)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']['gasprice']

    async def get_network_id(self, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_network_id(self.__url)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_block_height(self, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_block_height(self.__url)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_block_height_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_block_height_by_tx_hash(self.__url, tx_hash)
        response = await self.__get(url)
        if response.get('Result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if is_full:
            return response
        return response['Result']

    async def get_block_count_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        response = await self.get_block_height_by_tx_hash(tx_hash, is_full=True)
        response['Result'] += 1
        if is_full:
            return response
        return response['Result']

    async def get_block_count(self, is_full: bool = False) -> int or dict:
        response = await self.get_block_height(is_full=True)
        response['Result'] += 1
        if is_full:
            return response
        return response['Result']

    async def get_block_by_hash(self, block_hash: str,
                                is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_block_by_hash(self.__url, block_hash)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_block_by_height(self, height: int, is_full: bool = False):
        url = RestfulMethod.get_block_by_height(self.__url, height)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_balance(self, b58_address: str, is_full: bool = False):
        url = RestfulMethod.get_account_balance(self.__url, b58_address)
        response = await self.__get(url)
        response['Result'] = dict((k.upper(), int(v)) for k, v in response.get('Result', dict()).items())
        if is_full:
            return response
        return response['Result']

    async def get_grant_ong(self, b58_address: str, is_full: bool = False):
        url = RestfulMethod.get_grant_ong(self.__url, b58_address)
        response = await self.__get(url)
        if is_full:
            return response
        return int(response['Result'])

    async def get_allowance(self, asset: str, b58_from_address: str, b58_to_address: str,
                            is_full: bool = False):
        url = RestfulMethod.get_allowance(self.__url, asset, b58_from_address, b58_to_address)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_contract(self, contract_address: str, is_full: bool = False):
        url = RestfulMethod.get_contract(self.__url, contract_address)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_contract_event_by_height(self, height: int, is_full: bool = False) -> \
            List[
                dict]:
        url = RestfulMethod.get_contract_event_by_height(self.__url, height)
        response = await self.__get(url)
        if is_full:
            return response
        result = response['Result']
        if result == '':
            result = list()
        return result

    async def get_contract_event_by_count(self, count: int, is_full: bool = False) -> \
            List[
                dict]:
        return await self.get_contract_event_by_height(count - 1, is_full)

    async def get_contract_event_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_contract_event_by_tx_hash(self.__url, tx_hash)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_storage(self, hex_contract_address: str, hex_key: str,
                          is_full: bool = False) -> str or dict:
        url = RestfulMethod.get_storage(self.__url, hex_contract_address, hex_key)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_transaction_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_transaction(self.__url, tx_hash)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def send_raw_transaction(self, tx: Transaction, is_full: bool = False):
        hex_tx_data = tx.serialize(is_hex=True)
        data = f'{{"Action":"sendrawtransaction", "Version":"1.0.0","Data":"{hex_tx_data}"}}'
        url = RestfulMethod.send_transaction(self.__url)
        response = await self.__post(url, data)
        if is_full:
            return response
        return response['Result']

    async def send_raw_transaction_pre_exec(self, tx: Transaction,
                                            is_full: bool = False):
        hex_tx_data = tx.serialize(is_hex=True)
        data = f'{{"Action":"sendrawtransaction", "Version":"1.0.0","Data":"{hex_tx_data}"}}'
        url = RestfulMethod.send_transaction_pre_exec(self.__url)
        response = await self.__post(url, data)
        if is_full:
            return response
        return response['Result']

    async def get_merkle_proof(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_merkle_proof(self.__url, tx_hash)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_memory_pool_tx_count(self, is_full: bool = False):
        url = RestfulMethod.get_mem_pool_tx_count(self.__url)
        response = await self.__get(url)
        if is_full:
            return response
        return response['Result']

    async def get_memory_pool_tx_state(self, tx_hash: str, is_full: bool = False) -> \
            List[dict] or dict:
        url = RestfulMethod.get_mem_pool_tx_state(self.__url, tx_hash)
        response = await self.__get(url)
        if response.get('Result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if is_full:
            return response
        return response['Result']['State']
