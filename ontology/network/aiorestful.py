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

from time import time
from typing import List
from aiohttp.client import ClientSession

from Cryptodome.Random.random import randint

from ontology.account.account import Account
from ontology.smart_contract.neo_vm import NeoVm
from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.transaction import ensure_bytearray_contract_address
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction

TEST_RESTFUL_ADDRESS = ['http://polaris1.ont.io:20334', 'http://polaris2.ont.io:20334', 'http://polaris3.ont.io:20334']
MAIN_RESTFUL_ADDRESS = ['http://dappnode1.ont.io:20334', 'http://dappnode2.ont.io:20334']


class RestfulMethod(object):
    @staticmethod
    def get_version(url: str):
        return f'{url}/api/v1/version'

    @staticmethod
    def get_network_id(url: str):
        return f'{url}/api/v1/networkid'

    @staticmethod
    def get_connection_count(url: str):
        return f'{url}/api/v1/node/connectioncount'

    @staticmethod
    def get_gas_price(url: str):
        return f'{url}/api/v1/gasprice'

    @staticmethod
    def get_block_by_height(url: str, height: int):
        return f'{url}/api/v1/block/details/height/{height}?raw=0'

    @staticmethod
    def get_block_height(url: str):
        return f'{url}/api/v1/block/height'

    @staticmethod
    def get_block_by_hash(url: str, block_hash: str):
        return f'{url}/api/v1/block/details/hash/{block_hash}?raw=0'

    @staticmethod
    def get_account_balance(url: str, b58_address: str):
        return f'{url}/api/v1/balance/{b58_address}'

    @staticmethod
    def get_allowance(url: str, asset: str, b58_from_address: str, b58_to_address: str) -> str:
        return f'{url}/api/v1/allowance/{asset}/{b58_from_address}/{b58_to_address}'

    @staticmethod
    def get_transaction(url: str, tx_hash: str):
        return f'{url}/api/v1/transaction/{tx_hash}'

    @staticmethod
    def send_transaction(url: str, ):
        return f'{url}/api/v1/transaction?preExec=0'

    @staticmethod
    def send_transaction_pre_exec(url: str, ):
        return f'{url}/api/v1/transaction?preExec=1'

    @staticmethod
    def get_generate_block_time(url: str):
        return f'{url}/api/v1/node/generateblocktime'

    @staticmethod
    def get_contract(url: str, contract_address: str):
        return f'{url}/api/v1/contract/{contract_address}'

    @staticmethod
    def get_contract_event_by_height(url: str, height: int):
        return f'{url}/api/v1/smartcode/event/transactions/{height}'

    @staticmethod
    def get_contract_event_by_tx_hash(url: str, tx_hash: str):
        return f'{url}/api/v1/smartcode/event/txhash/{tx_hash}'

    @staticmethod
    def get_block_height_by_tx_hash(url: str, tx_hash: str):
        return f'{url}/api/v1/block/height/txhash/{tx_hash}'

    @staticmethod
    def get_storage(url: str, hex_contract_address: str, hex_key: str):
        return f'{url}/api/v1/storage/{hex_contract_address}/{hex_key}'

    @staticmethod
    def get_merkle_proof(url: str, tx_hash: str):
        return f'{url}/api/v1/merkleproof/{tx_hash}'

    @staticmethod
    def get_mem_pool_tx_count(url: str):
        return f'{url}/api/v1/mempool/txcount'

    @staticmethod
    def get_mem_pool_tx_state(url: str, tx_hash: str):
        return f'{url}/api/v1/mempool/txstate/{tx_hash}'

    @staticmethod
    def get_grant_ong(url: str, b58_address: str):
        return f'{url}/api/v1/grantong/{b58_address}'


class AioRestful(object):
    def __init__(self, url: str = ''):
        self.__url = url

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

    def set_address(self, url: str):
        self.__url = url

    def get_address(self):
        return self.__url

    def connect_to_localhost(self):
        self.set_address('http://localhost:20334')

    def connect_to_test_net(self, index: int = 0):
        if index == 0:
            index = randint(1, 5)
        restful_address = f'http://polaris{index}.ont.io:20334'
        self.set_address(restful_address)

    def connect_to_main_net(self, index: int = 0):
        if index == 0:
            index = randint(1, 3)
        restful_address = f'http://dappnode{index}.ont.io:20334'
        self.set_address(restful_address)

    async def __post(self, session, url: str, data: str):
        if session is None:
            async with ClientSession() as session:
                async with session.post(url, data=data, timeout=10) as response:
                    return json.loads(await response.content.read(-1))
        else:
            async with session.post(url, data=data, timeout=10) as response:
                return json.loads(await response.content.read(-1))

    async def __get(self, session, url):
        try:
            if session is None:
                async with ClientSession() as session:

                    async with session.get(url, timeout=10) as response:
                        return json.loads(await response.content.read(-1))
            else:
                async with session.get(url, timeout=10) as response:
                    return json.loads(await response.content.read(-1))
        except asyncio.TimeoutError:
            raise SDKException(ErrorCode.connect_timeout(self.__url))

    async def get_version(self, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_version(self.__url)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_connection_count(self, session: ClientSession = None, is_full: bool = False) -> int:
        url = RestfulMethod.get_connection_count(self.__url)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_gas_price(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_gas_price(self.__url)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']['gasprice']

    async def get_network_id(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_network_id(self.__url)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_block_height(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_block_height(self.__url)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_block_height_by_tx_hash(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_block_height_by_tx_hash(self.__url, tx_hash)
        response = await self.__get(session, url)
        if response.get('Result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if is_full:
            return response
        return response['Result']

    async def get_block_count_by_tx_hash(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        response = await self.get_block_height_by_tx_hash(tx_hash, session, is_full=True)
        response['Result'] += 1
        if is_full:
            return response
        return response['Result']

    async def get_block_count(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        response = await self.get_block_height(session, is_full=True)
        response['Result'] += 1
        if is_full:
            return response
        return response['Result']

    async def get_block_by_hash(self, block_hash: str, session: ClientSession = None,
                                is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_block_by_hash(self.__url, block_hash)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_block_by_height(self, height: int, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_block_by_height(self.__url, height)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_balance(self, b58_address: str, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_account_balance(self.__url, b58_address)
        response = await self.__get(session, url)
        response['Result'] = dict((k.upper(), int(v)) for k, v in response.get('Result', dict()).items())
        if is_full:
            return response
        return response['Result']

    async def get_grant_ong(self, b58_address: str, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_grant_ong(self.__url, b58_address)
        response = await self.__get(session, url)
        if is_full:
            return response
        return int(response['Result'])

    async def get_allowance(self, asset: str, b58_from_address: str, b58_to_address: str, session: ClientSession = None,
                            is_full: bool = False):
        url = RestfulMethod.get_allowance(self.__url, asset, b58_from_address, b58_to_address)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_contract(self, contract_address: str, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_contract(self.__url, contract_address)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_contract_event_by_height(self, height: int, session: ClientSession = None, is_full: bool = False) -> \
            List[
                dict]:
        url = RestfulMethod.get_contract_event_by_height(self.__url, height)
        response = await self.__get(session, url)
        if is_full:
            return response
        result = response['Result']
        if result == '':
            result = list()
        return result

    async def get_contract_event_by_count(self, count: int, session: ClientSession = None, is_full: bool = False) -> \
            List[
                dict]:
        return await self.get_contract_event_by_height(count - 1, session, is_full)

    async def get_contract_event_by_tx_hash(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_contract_event_by_tx_hash(self.__url, tx_hash)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_storage(self, hex_contract_address: str, hex_key: str, session: ClientSession = None,
                          is_full: bool = False) -> str or dict:
        url = RestfulMethod.get_storage(self.__url, hex_contract_address, hex_key)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_transaction_by_tx_hash(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_transaction(self.__url, tx_hash)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def send_raw_transaction(self, tx: Transaction, session: ClientSession = None, is_full: bool = False):
        hex_tx_data = tx.serialize(is_hex=True)
        data = f'{{"Action":"sendrawtransaction", "Version":"1.0.0","Data":"{hex_tx_data}"}}'
        url = RestfulMethod.send_transaction(self.__url)
        response = await self.__post(session, url, data)
        if is_full:
            return response
        return response['Result']

    async def send_raw_transaction_pre_exec(self, tx: Transaction, session: ClientSession = None,
                                            is_full: bool = False):
        hex_tx_data = tx.serialize(is_hex=True)
        data = f'{{"Action":"sendrawtransaction", "Version":"1.0.0","Data":"{hex_tx_data}"}}'
        url = RestfulMethod.send_transaction_pre_exec(self.__url)
        response = await self.__post(session, url, data)
        if is_full:
            return response
        return response['Result']

    async def get_merkle_proof(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_merkle_proof(self.__url, tx_hash)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_memory_pool_tx_count(self, session: ClientSession = None, is_full: bool = False):
        url = RestfulMethod.get_mem_pool_tx_count(self.__url)
        response = await self.__get(session, url)
        if is_full:
            return response
        return response['Result']

    async def get_memory_pool_tx_state(self, tx_hash: str, session: ClientSession = None, is_full: bool = False) -> \
            List[dict] or dict:
        url = RestfulMethod.get_mem_pool_tx_state(self.__url, tx_hash)
        response = await self.__get(session, url)
        if response.get('Result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if is_full:
            return response
        return response['Result']['State']
