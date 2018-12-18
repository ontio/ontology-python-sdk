#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

from sys import maxsize
from Cryptodome.Random.random import randint

from ontology.common.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException


class RpcMethod(object):
    GET_VERSION = "getversion"
    GET_NODE_COUNT = "getconnectioncount"
    GET_GAS_PRICE = "getgasprice"
    GET_NETWORK_ID = "getnetworkid"
    GET_TRANSACTION = "getrawtransaction"
    SEND_TRANSACTION = "sendrawtransaction"
    GET_BLOCK = "getblock"
    GET_BLOCK_COUNT = "getblockcount"
    GET_BLOCK_HASH = "getblockhash"
    GET_CURRENT_BLOCK_HASH = "getbestblockhash"
    GET_BALANCE = "getbalance"
    GET_ALLOWANCE = "getallowance"
    GET_SMART_CONTRACT_EVENT = "getsmartcodeevent"
    GET_STORAGE = "getstorage"
    GET_SMART_CONTRACT = "getcontractstate"
    GET_GENERATE_BLOCK_TIME = "getgenerateblocktime"
    GET_MERKLE_PROOF = "getmerkleproof"
    SEND_EMERGENCY_GOV_REQ = "sendemergencygovreq"
    GET_BLOCK_ROOT_WITH_NEW_TX_ROOT = "getblockrootwithnewtxroot"

    RPC_VERSION = "2.0"


class RpcClient(object):
    def __init__(self, url: str = '', qid: int = 0):
        self.__url = url
        self.__qid = qid
        self.__generate_qid()

    def set_address(self, url: str):
        self.__url = url

    def get_address(self):
        return self.__url

    def __generate_qid(self):
        if self.__qid == 0:
            self.__qid = randint(0, maxsize)
        return self.__qid

    @staticmethod
    def __post(url, payload):
        header = {'Content-type': 'application/json'}
        try:
            response = requests.post(url, json=payload, headers=header, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0]))
        except requests.exceptions.ConnectTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectTimeout: ', url])))
        except requests.exceptions.ConnectionError:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectionError: ', url])))
        if response.status_code != 200:
            raise SDKException(ErrorCode.other_error(response.content.decode('utf-8')))
        response = json.loads(response.content.decode('utf-8'))
        return response

    @staticmethod
    def __get(url, payload):
        header = {'Content-type': 'application/json'}
        try:
            response = requests.get(url, params=json.dumps(payload), headers=header, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0]))
        except requests.exceptions.ConnectTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectTimeout: ', url])))
        except requests.exceptions.ConnectionError:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectionError: ', url])))
        if response.status_code != 200:
            raise SDKException(ErrorCode.other_error(response.content.decode('utf-8')))
        response = json.loads(response.content.decode('utf-8'))
        return response

    def generate_json_rpc_payload(self, method, param=None):
        if param is None:
            param = list()
        json_rpc_payload = dict(jsonrpc=RpcMethod.RPC_VERSION, id=self.__qid, method=method, params=param)
        return json_rpc_payload

    def get_version(self, is_full: bool = False) -> dict or str:
        """
        This interface is used to get the version information of the connected node in current network.

        Return:
            the version information of the connected node.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_VERSION)
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def get_block_count(self, is_full: bool = False) -> int:
        """
        This interface is used to get the decimal block number in current network.

        Return:
            the decimal total number of blocks in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_COUNT)
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def get_balance(self, base58_address: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the account balance of specified base58 encoded address in current network.

        :param base58_address: a base58 encoded account address.
        :param is_full:
        :return: the value of account balance in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BALANCE, [base58_address, 1])
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

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
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def get_storage(self, contract_address: str, key: str, is_full: bool = False) -> str:
        """
        This interface is used to get the corresponding stored value
        based on hexadecimal contract address and stored key.

        :param contract_address: hexadecimal contract address.
        :param key: a hexadecimal stored key.
        :param is_full:
        :return: the information of contract storage.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_STORAGE, [contract_address, key, 1])
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def get_smart_contract_event_by_tx_hash(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.

        :param tx_hash: a hexadecimal hash value.
        :param is_full:
        :return: the information of smart contract event in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [tx_hash, 1])
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def get_smart_contract_event_by_height(self, height: int, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.

        :param height: a decimal height value.
        :param is_full:
        :return: the information of smart contract event in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [height, 1])
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def get_raw_transaction(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding transaction information based on the specified hash value.

        :param tx_hash: str, a hexadecimal hash value.
        :param is_full:
        :return: dict
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_TRANSACTION, [tx_hash, 1])
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def get_smart_contract(self, hex_contract_address: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the information of smart contract based on the specified hexadecimal hash value.

        :param hex_contract_address: str, a hexadecimal hash value.
        :param is_full:
        :return: the information of smart contract in dictionary form.
        """
        if type(hex_contract_address) != str:
            raise SDKException(ErrorCode.param_err('a hexadecimal contract address is required.'))
        if len(hex_contract_address) != 40:
            raise SDKException(ErrorCode.param_err('the length of the contract address should be 40 bytes.'))
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT, [hex_contract_address, 1])
        response = self.__post(self.__url, payload)
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
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']

    def send_raw_transaction(self, tx: Transaction, is_full: bool = False) -> str:
        """
        This interface is used to send the transaction into the network.
        :param tx: Transaction object in ontology Python SDK.
        :param is_full:
        :return: a hexadecimal transaction hash value.
        """
        tx_data = tx.serialize(is_hex=True).decode('ascii')
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data])
        response = self.__post(self.__url, payload)
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
        tx_data = tx.serialize(is_hex=True).decode('ascii')
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data, 1])
        response = self.__post(self.__url, payload)
        if is_full:
            return response
        return response['result']
