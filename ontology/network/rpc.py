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
import requests

from sys import maxsize
from typing import List

from Cryptodome.Random.random import randint

from ontology.account.account import Account
from ontology.contract.neo.vm import NeoVm
from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.transaction import ensure_bytearray_contract_address
from ontology.contract.neo.abi.abi_function import AbiFunction
from ontology.contract.neo.abi.build_params import BuildParams
from ontology.contract.neo.invoke_function import InvokeFunction

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


class Rpc(object):
    def __init__(self, url: str = '', qid: int = 0):
        self._url = url
        self._qid = qid
        self._generate_qid()

    def set_address(self, url: str):
        self._url = url

    def get_address(self):
        return self._url

    def _generate_qid(self):
        if self._qid == 0:
            self._qid = randint(0, maxsize)
        return self._qid

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

    @staticmethod
    def __post(url, payload):
        header = {'Content-type': 'application/json'}
        try:
            response = requests.post(url, json=payload, headers=header, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0])) from None
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout):
            raise SDKException(ErrorCode.connect_timeout(url)) from None
        try:
            content = response.content.decode('utf-8')
        except Exception as e:
            raise SDKException(ErrorCode.other_error(e.args[0])) from None
        if response.status_code != 200:
            raise SDKException(ErrorCode.other_error(content))
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError as e:
            raise SDKException(ErrorCode.other_error(e.args[0])) from None
        if content['error'] != 0:
            if content['result'] != '':
                raise SDKException(ErrorCode.other_error(content['result']))
            else:
                raise SDKException(ErrorCode.other_error(content['desc']))
        return content

    @staticmethod
    def __get(url, payload):
        header = {'Content-type': 'application/json'}
        try:
            response = requests.get(url, params=json.dumps(payload), headers=header, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0]))
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            raise SDKException(ErrorCode.connect_timeout(url)) from None
        try:
            content = response.content.decode('utf-8')
        except Exception as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        if response.status_code != 200:
            raise SDKException(ErrorCode.other_error(content))
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        if content['error'] != 0:
            if content['result'] != '':
                raise SDKException(ErrorCode.other_error(content['result']))
            else:
                raise SDKException(ErrorCode.other_error(content['desc']))
        return content

    def generate_json_rpc_payload(self, method, param=None):
        if param is None:
            param = list()
        json_rpc_payload = dict(jsonrpc=RpcMethod.RPC_VERSION, id=self._qid, method=method, params=param)
        return json_rpc_payload

    def get_version(self, is_full: bool = False) -> dict or str:
        """
        This interface is used to get the version information of the connected node in current network.
        Return:
            the version information of the connected node.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_VERSION)
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_connection_count(self, is_full: bool = False) -> int:
        """
        This interface is used to get the current number of connections for the node in current network.
        Return:
            the number of connections.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_NODE_COUNT)
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_gas_price(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the gas price in current network.
        Return:
            the value of gas price.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_GAS_PRICE)
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']['gasprice']

    def get_network_id(self, is_full: bool = False) -> int:
        """
        This interface is used to get the network id of current network.
        Return:
            the network id of current network.
        """

        payload = self.generate_json_rpc_payload(RpcMethod.GET_NETWORK_ID)
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_block_by_hash(self, block_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.
        :param block_hash: a hexadecimal value of block hash.
        :param is_full:
        :return: the block information of the specified block hash.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK, [block_hash, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_block_by_height(self, height: int, is_full: bool = False) -> dict:
        """
        This interface is used to get the block information by block height in current network.
        Return:
            the decimal total number of blocks in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK, [height, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_block_count(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the decimal block number in current network.
        Return:
            the decimal total number of blocks in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_COUNT)
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_block_height(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the decimal block height in current network.
        Return:
            the decimal total height of blocks in current network.
        """
        response = self.get_block_count(is_full=True)
        response['result'] -= 1
        if is_full:
            return response
        return response['result']

    def get_block_height_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_HEIGHT_BY_HASH, [tx_hash])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_block_count_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        response = self.get_block_height_by_tx_hash(tx_hash, is_full=True)
        response['result'] += 1
        if is_full:
            return response
        return response['result']

    def get_current_block_hash(self, is_full: bool = False) -> str:
        """
        This interface is used to get the hexadecimal hash value of the highest block in current network.
        Return:
            the hexadecimal hash value of the highest block in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_CURRENT_BLOCK_HASH)
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_block_hash_by_height(self, height: int, is_full: bool = False) -> str:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.
        :param height: a decimal block height value.
        :param is_full:
        :return: the hexadecimal hash value of the specified block height.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_HASH, [height, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_balance(self, b58_address: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the account balance of specified base58 encoded address in current network.
        :param b58_address: a base58 encoded account address.
        :param is_full:
        :return: the value of account balance in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BALANCE, [b58_address, 1])
        response = self.__post(self._url, payload)
        response['result'] = dict((k.upper(), int(v)) for k, v in response.get('result', dict()).items())
        if is_full:
            return response
        return response['result']

    def get_grant_ong(self, b58_address: str, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_GRANT_ONG, [b58_address])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return int(response['result'])

    def get_allowance(self, asset_name: str, from_address: str, to_address: str, is_full: bool = False) -> str:
        """
        This interface is used to get the the allowance
        from transfer-from account to transfer-to account in current network.
        :param asset_name:
        :param from_address: a base58 encoded account address.
        :param to_address: a base58 encoded account address.
        :param is_full:
        :return: the information of allowance in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_ALLOWANCE, [asset_name, from_address, to_address])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_storage(self, hex_contract_address: str, hex_key: str, is_full: bool = False) -> str:
        """
        This interface is used to get the corresponding stored value
        based on hexadecimal contract address and stored key.
        :param hex_contract_address: hexadecimal contract address.
        :param hex_key: a hexadecimal stored key.
        :param is_full:
        :return: the information of contract storage.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_STORAGE, [hex_contract_address, hex_key, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_contract_event_by_tx_hash(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.
        :param tx_hash: a hexadecimal hash value.
        :param is_full:
        :return: the information of smart contract event in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [tx_hash, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    def get_contract_event_by_height(self, height: int, is_full: bool = False) -> List[dict]:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.
        :param height: a decimal height value.
        :param is_full:
        :return: the information of smart contract event in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [height, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        event_list = response['result']
        if event_list is None:
            event_list = list()
        return event_list

    def get_contract_event_by_count(self, count: int, is_full: bool = False) -> List[dict]:
        return self.get_contract_event_by_height(count - 1, is_full)

    def get_transaction_by_tx_hash(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding transaction information based on the specified hash value.
        :param tx_hash: str, a hexadecimal hash value.
        :param is_full:
        :return: dict
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_TRANSACTION, [tx_hash, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_contract(self, hex_contract_address: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the information of smart contract based on the specified hexadecimal hash value.
        :param hex_contract_address: str, a hexadecimal hash value.
        :param is_full:
        :return: the information of smart contract in dictionary form.
        """
        if not isinstance(hex_contract_address, str):
            raise SDKException(ErrorCode.param_err('a hexadecimal contract address is required.'))
        if len(hex_contract_address) != 40:
            raise SDKException(ErrorCode.param_err('the length of the contract address should be 40 bytes.'))
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT, [hex_contract_address, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_merkle_proof(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding merkle proof based on the specified hexadecimal hash value.
        :param tx_hash: an hexadecimal transaction hash value.
        :param is_full:
        :return: the merkle proof in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MERKLE_PROOF, [tx_hash, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_memory_pool_tx_count(self, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MEM_POOL_TX_COUNT)
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def get_memory_pool_tx_state(self, tx_hash: str, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MEM_POOL_TX_STATE, [tx_hash])
        response = self.__post(self._url, payload)
        if response.get('result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if is_full:
            return response
        return response['result']['State']

    def send_raw_transaction(self, tx: Transaction, is_full: bool = False) -> str:
        """
        This interface is used to send the transaction into the network.
        :param tx: Transaction object in ontology Python SDK.
        :param is_full:
        :return: a hexadecimal transaction hash value.
        """
        tx_data = tx.serialize(is_hex=True)
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def send_raw_transaction_pre_exec(self, tx: Transaction, is_full: bool = False):
        """
        This interface is used to send the transaction that is prepare to execute.
        :param tx: Transaction object in ontology Python SDK.
        :param is_full: Whether to return all information.
        :return: the execution result of transaction that is prepare to execute.
        """
        tx_data = tx.serialize(is_hex=True)
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data, 1])
        response = self.__post(self._url, payload)
        if is_full:
            return response
        return response['result']

    def send_neo_vm_tx_pre_exec(self, contract_address: str or bytes or bytearray, func: AbiFunction or InvokeFunction,
                                signer: Account = None, is_full: bool = False):
        contract_address = ensure_bytearray_contract_address(contract_address)
        tx = NeoVm.make_invoke_transaction(contract_address, func, b'', 0, 0)
        if signer is not None:
            tx.sign_transaction(signer)
        return self.send_raw_transaction_pre_exec(tx, is_full)

    def send_neo_vm_transaction(self, contract_address: str or bytes or bytearray,
                                signer: Account or None,
                                payer: Account or None,
                                gas_price: int,
                                gas_limit: int,
                                func: AbiFunction or InvokeFunction, is_full: bool = False):
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
        tx = Transaction(0, 0xd1, gas_price, gas_limit, payer.get_address_bytes(), params)
        tx.sign_transaction(payer)
        if isinstance(signer, Account) and signer.get_address_base58() != payer.get_address_base58():
            tx.add_sign_transaction(signer)
        return self.send_raw_transaction(tx, is_full)
