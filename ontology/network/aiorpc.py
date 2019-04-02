#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import asyncio
import inspect

from time import time
from sys import maxsize
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

TEST_RPC_ADDRESS = ['http://polaris1.ont.io:20336', 'http://polaris2.ont.io:20336', 'http://polaris3.ont.io:20336',
                    'http://polaris4.ont.io:20336']
MAIN_RPC_ADDRESS = ['http://dappnode1.ont.io:20336', 'http://dappnode2.ont.io:20336']


class RpcMethod(object):
    GET_VERSION = 'getversion'
    GET_NODE_COUNT = 'getconnectioncount'
    GET_GAS_PRICE = 'getgasprice'
    GET_NETWORK_ID = 'getnetworkid'
    GET_TRANSACTION = 'getrawtransaction'
    SEND_TRANSACTION = 'sendrawtransaction'
    GET_BLOCK = 'getblock'
    GET_BLOCK_COUNT = 'getblockcount'
    GET_BLOCK_HASH = 'getblockhash'
    GET_CURRENT_BLOCK_HASH = 'getbestblockhash'
    GET_BLOCK_HEIGHT_BY_HASH = 'getblockheightbytxhash'
    GET_BALANCE = 'getbalance'
    GET_GRANT_ONG = 'getgrantong'
    GET_ALLOWANCE = 'getallowance'
    GET_SMART_CONTRACT_EVENT = 'getsmartcodeevent'
    GET_STORAGE = 'getstorage'
    GET_SMART_CONTRACT = 'getcontractstate'
    GET_GENERATE_BLOCK_TIME = 'getgenerateblocktime'
    GET_MERKLE_PROOF = 'getmerkleproof'
    SEND_EMERGENCY_GOV_REQ = 'sendemergencygovreq'
    GET_BLOCK_ROOT_WITH_NEW_TX_ROOT = 'getblockrootwithnewtxroot'
    GET_MEM_POOL_TX_COUNT = 'getmempooltxcount'
    GET_MEM_POOL_TX_STATE = 'getmempooltxstate'

    RPC_VERSION = '2.0'


class AioRpc(object):
    def __init__(self, url: str = '', qid: int = 0):
        self.__url = url
        self.__qid = qid
        self.__generate_qid()

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

    def __generate_qid(self):
        if self.__qid == 0:
            self.__qid = randint(0, maxsize)
        return self.__qid

    def connect_to_localhost(self):
        self.set_address('http://localhost:20336')

    def connect_to_test_net(self, index: int = 0):
        if index == 0:
            index = randint(1, 5)
        rpc_address = f'http://polaris{index}.ont.io:20336'
        self.set_address(rpc_address)

    def connect_to_main_net(self, index: int = 0):
        if index == 0:
            index = randint(1, 4)
        rpc_address = f'http://dappnode{index}.ont.io:20336'
        self.set_address(rpc_address)

    def generate_json_rpc_payload(self, method, param=None):
        if param is None:
            param = list()
        json_rpc_payload = dict(jsonrpc=RpcMethod.RPC_VERSION, id=self.__qid, method=method, params=param)
        return json_rpc_payload

    async def __post(self, session, payload):
        header = {'Content-type': 'application/json'}
        if session is None:
            async with ClientSession() as session:
                async with session.post(self.__url, json=payload, headers=header, timeout=10) as response:
                    return json.loads(await response.content.read(-1))
        else:
            async with session.post(self.__url, json=payload, headers=header, timeout=10) as response:
                return json.loads(await response.content.read(-1))

    async def get_version(self, session: ClientSession = None, is_full: bool = False):
        """
        This interface is used to get the version information of the connected node in current network.

        Return:
            the version information of the connected node.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_VERSION)
        if session is None:
            async with ClientSession() as session:
                response = await self.__post(session, payload)
        else:
            response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_connection_count(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the current number of connections for the node in current network.

        Return:
            the number of connections.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_NODE_COUNT)
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_gas_price(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the gas price in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_GAS_PRICE)
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']['gasprice']

    async def get_network_id(self, session: ClientSession = None, is_full: bool = False) -> int:
        """
        This interface is used to get the network id of current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_NETWORK_ID)
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_block_by_hash(self, block_hash: str, session: ClientSession = None, is_full: bool = False) -> dict:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK, [block_hash, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_block_by_height(self, height: int, session: ClientSession = None, is_full: bool = False) -> dict:
        """
        This interface is used to get the block information by block height in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK, [height, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_block_count(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the decimal block number in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_COUNT)
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_block_height(self, session: ClientSession = None, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the decimal block height in current network.
        """
        response = await self.get_block_count(session, is_full=True)
        response['result'] -= 1
        if is_full:
            return response
        return response['result']

    async def get_block_height_by_tx_hash(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_HEIGHT_BY_HASH, [tx_hash])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_block_count_by_tx_hash(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        response = await self.get_block_height_by_tx_hash(tx_hash, session, is_full=True)
        response['result'] += 1
        if is_full:
            return response
        return response['result']

    async def get_current_block_hash(self, session: ClientSession = None, is_full: bool = False) -> str:
        """
        This interface is used to get the hexadecimal hash value of the highest block in current network.

        Return:
            the hexadecimal hash value of the highest block in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_CURRENT_BLOCK_HASH)
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_block_hash_by_height(self, height: int, session: ClientSession = None, is_full: bool = False) -> str:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_HASH, [height, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_balance(self, b58_address: str, session: ClientSession = None, is_full: bool = False) -> dict:
        """
        This interface is used to get the account balance of specified base58 encoded address in current network.

        :param b58_address: a base58 encoded account address.
        :param is_full:
        :return: the value of account balance in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BALANCE, [b58_address, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_grant_ong(self, b58_address: str, session: ClientSession = None, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_GRANT_ONG, [b58_address])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return int(response['result'])

    async def get_allowance(self, asset_name: str, from_address: str, to_address: str, session: ClientSession = None,
                            is_full: bool = False) -> str:
        """
        This interface is used to get the the allowance
        from transfer-from account to transfer-to account in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_ALLOWANCE, [asset_name, from_address, to_address])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_storage(self, hex_contract_address: str, hex_key: str, session: ClientSession = None,
                          is_full: bool = False) -> str:
        """
        This interface is used to get the corresponding stored value
        based on hexadecimal contract address and stored key.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_STORAGE, [hex_contract_address, hex_key, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_contract_event_by_tx_hash(self, tx_hash: str, session: ClientSession = None,
                                            is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [tx_hash, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_contract_event_by_height(self, height: int, session: ClientSession = None, is_full: bool = False):
        """
        This interface is used to get the corresponding smart contract event based on the height of block.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [height, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        event_list = response['result']
        if event_list is None:
            event_list = list()
        return event_list

    async def get_contract_event_by_count(self, count: int, session: ClientSession = None,
                                          is_full: bool = False) -> List[dict]:
        return await self.get_contract_event_by_height(count - 1, session, is_full)

    async def get_transaction_by_tx_hash(self, tx_hash: str, session: ClientSession = None,
                                         is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding transaction information based on the specified hash value.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_TRANSACTION, [tx_hash, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_smart_contract(self, hex_contract_address: str, session: ClientSession = None,
                                 is_full: bool = False) -> dict:
        """
        This interface is used to get the information of smart contract based on the specified hexadecimal hash value.
        """
        if not isinstance(hex_contract_address, str):
            raise SDKException(ErrorCode.param_err('a hexadecimal contract address is required.'))
        if len(hex_contract_address) != 40:
            raise SDKException(ErrorCode.param_err('the length of the contract address should be 40 bytes.'))
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT, [hex_contract_address, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_merkle_proof(self, tx_hash: str, session: ClientSession = None, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding merkle proof based on the specified hexadecimal hash value.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MERKLE_PROOF, [tx_hash, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_memory_pool_tx_count(self, session: ClientSession = None, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MEM_POOL_TX_COUNT)
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def get_memory_pool_tx_state(self, tx_hash: str, session: ClientSession = None, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MEM_POOL_TX_STATE, [tx_hash])
        response = await self.__post(session, payload)
        if is_full:
            return response
        if isinstance(response['result'], str):
            return response['result']
        return response['result']['State']

    async def send_raw_transaction(self, tx: Transaction, session: ClientSession = None, is_full: bool = False) -> str:
        """
        This interface is used to send the transaction into the network.
        """
        tx_data = tx.serialize(is_hex=True)
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def send_raw_transaction_pre_exec(self, tx: Transaction, session: ClientSession = None,
                                            is_full: bool = False):
        """
        This interface is used to send the transaction that is prepare to execute.
        """
        tx_data = tx.serialize(is_hex=True)
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data, 1])
        response = await self.__post(session, payload)
        if is_full:
            return response
        return response['result']

    async def send_neo_vm_transaction_pre_exec(self, contract_address: str or bytes or bytearray,
                                               signer: Account or None, func: AbiFunction or InvokeFunction,
                                               session: ClientSession = None,
                                               is_full: bool = False):
        contract_address = ensure_bytearray_contract_address(contract_address)
        tx = NeoVm.make_invoke_transaction(contract_address, func)
        if signer is not None:
            tx.sign_transaction(signer)
        return await self.send_raw_transaction_pre_exec(tx, session, is_full)

    async def send_neo_vm_transaction(self, contract_address: str or bytes or bytearray, signer: Account or None,
                                      payer: Account or None, gas_limit: int, gas_price: int,
                                      func: AbiFunction or InvokeFunction, session: ClientSession = None,
                                      is_full: bool = False):
        if isinstance(func, AbiFunction):
            params = BuildParams.serialize_abi_function(func)
        elif isinstance(func, InvokeFunction):
            params = func.create_invoke_code()
        else:
            raise SDKException(ErrorCode.other_error('the type of func is error.'))
        contract_address = ensure_bytearray_contract_address(contract_address)
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        if payer is None:
            raise SDKException(ErrorCode.param_err('payer account is None.'))
        tx = Transaction(0, 0xd1, int(time()), gas_price, gas_limit, payer.get_address_bytes(), params, bytearray(), [])
        tx.sign_transaction(payer)
        if isinstance(signer, Account) and signer.get_address_base58() != payer.get_address_base58():
            tx.add_sign_transaction(signer)
        return await self.send_raw_transaction(tx, session, is_full)
