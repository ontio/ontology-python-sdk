#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import json
import requests

from sys import maxsize
from Cryptodome.Random.random import randint

from ontology.common.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.utils.contract_data_parser import ContractDataParser

RPC_GET_VERSION = "getversion"
RPC_GET_NODE_COUNT = "getconnectioncount"
RPC_GET_GAS_PRICE = "getgasprice"
RPC_GET_NETWORK_ID = "getnetworkid"
RPC_GET_TRANSACTION = "getrawtransaction"
RPC_SEND_TRANSACTION = "sendrawtransaction"
RPC_GET_BLOCK = "getblock"
RPC_GET_BLOCK_COUNT = "getblockcount"
RPC_GET_BLOCK_HASH = "getblockhash"
RPC_GET_CURRENT_BLOCK_HASH = "getbestblockhash"
RPC_GET_BALANCE = "getbalance"
RPC_GET_ALLOWANCE = "getallowance"
RPC_GET_SMART_CONTRACT_EVENT = "getsmartcodeevent"
RPC_GET_STORAGE = "getstorage"
RPC_GET_SMART_CONTRACT = "getcontractstate"
RPC_GET_GENERATE_BLOCK_TIME = "getgenerateblocktime"
RPC_GET_MERKLE_PROOF = "getmerkleproof"
SEND_EMERGENCY_GOV_REQ = "sendemergencygovreq"
GET_BLOCK_ROOT_WITH_NEW_TX_ROOT = "getblockrootwithnewtxroot"

JSON_RPC_VERSION = "2.0"


class HttpRequest(object):
    _timeout = 10

    @staticmethod
    def set_timeout(timeout=10):
        HttpRequest._timeout = timeout

    @staticmethod
    def request(method, url, payload):
        header = {'Content-type': 'application/json'}
        try:
            if method == "post":
                res = requests.post(url, json=payload, headers=header, timeout=HttpRequest._timeout)
                return res
            elif method == "get":
                res = requests.get(url, params=json.dumps(payload), timeout=HttpRequest._timeout)
                return res
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0]))


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

    def generate_json_rpc_payload(self, method, param=None):
        if param is None:
            param = list()
        json_rpc_payload = dict(jsonrpc=JSON_RPC_VERSION, id=self.__qid, method=method, params=param)
        return json_rpc_payload

    def __post(self, method: str, msg: list = None) -> dict or str:
        if msg is None:
            msg = list()
        payload = self.generate_json_rpc_payload(method, msg)
        try:
            response = HttpRequest.request("post", self.__url, payload)
        except requests.exceptions.ConnectTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectTimeout: ', self.__url])))
        except requests.exceptions.ConnectionError:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectionError: ', self.__url])))
        response = json.loads(response.content.decode())['result']
        return response

    def get_version(self) -> str:
        """
        This interface is used to get the version information of the connected node in current network.

        Return:
            the version information of the connected node.
        """
        response = self.__post(RPC_GET_VERSION)
        return response

    def get_node_count(self) -> int:
        """
        This interface is used to get the current number of connections for the node in current network.

        Return:
            the number of connections.
        """

        count = self.__post(RPC_GET_NODE_COUNT)
        return count

    def get_gas_price(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the gas price in current network.

        Return:
            the value of gas price.
        """

        price = self.__post(RPC_GET_GAS_PRICE)
        if is_full:
            return price
        return price['gasprice']

    def get_network_id(self) -> int:
        """
        This interface is used to get the network id of current network.

        Return:
            the network id of current network.
        """

        network_id = self.__post(RPC_GET_NETWORK_ID)
        return network_id

    def get_block_by_hash(self, block_hash: str) -> dict:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.

        Args:
         block_hash (str):
            a hexadecimal value of block hash

        Return:
            the block information of the specified block hash.
        """

        dict_block = self.__post(RPC_GET_BLOCK, [block_hash, 1])
        return dict_block

    def get_block_by_height(self, height: int) -> dict:
        """
        This interface is used to get the block information by block height in current network.

        Return:
            the decimal total number of blocks in current network.
        """

        dict_block = self.__post(RPC_GET_BLOCK, [height, 1])
        return dict_block

    def get_block_count(self) -> int:
        """
        This interface is used to get the decimal block number in current network.

        Return:
            the decimal total number of blocks in current network.
        """

        count = self.__post(RPC_GET_BLOCK_COUNT)
        return count

    def get_current_block_hash(self) -> str:
        """
        This interface is used to get the hexadecimal hash value of the highest block in current network.

        Return:
            the hexadecimal hash value of the highest block in current network.
        """

        current_block_hash = self.__post(RPC_GET_CURRENT_BLOCK_HASH)
        return current_block_hash

    def get_block_hash_by_height(self, height: int) -> str:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.

        Args:
         height (int):
            a decimal block height value

        Return:
            the hexadecimal hash value of the specified block height.
        """

        block_hash = self.__post(RPC_GET_BLOCK_HASH, [height, 1])
        return block_hash

    def get_balance(self, base58_address: str) -> dict:
        """
        This interface is used to get the account balance of specified base58 encoded address in current network.

        Args:
         base58_address (str):
            a base58 encoded account address

        Return:
            the value of account balance in dictionary form.
        """

        balance = self.__post(RPC_GET_BALANCE, [base58_address, 1])
        return balance

    def get_allowance(self, asset_name: str, from_address: str, to_address: str) -> str:
        """
        This interface is used to get the the allowance
        from transfer-from account to transfer-to account in current network.

        Args:
         from_address (str):
            a base58 encoded account address

        Return:
            the information of allowance in dictionary form.
        """

        allowance = self.__post(RPC_GET_ALLOWANCE, [asset_name, from_address, to_address])
        return allowance

    def get_storage(self, contract_address: str, key: str) -> str:
        """
        This interface is used to get the corresponding stored value
        based on hexadecimal contract address and stored key.

        Args:
         contract_address (str):
            hexadecimal contract address
         key (str):
            a hexadecimal stored key

        Return:
            the information of contract storage.
        """

        storage_value = self.__post(RPC_GET_STORAGE, [contract_address, key, 1])
        return storage_value

    def get_smart_contract_event_by_tx_hash(self, tx_hash: str) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.

        Args:
         tx_hash (str):
            a hexadecimal hash value

        Return:
            the information of smart contract event in dictionary form.
        """

        event = self.__post(RPC_GET_SMART_CONTRACT_EVENT, [tx_hash, 1])
        return event

    def get_smart_contract_event_by_height(self, height: int) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.

        Args:
         height (int):
            a decimal height value.

        Return:
            the information of smart contract event in dictionary form.
        """

        event = self.__post(RPC_GET_SMART_CONTRACT_EVENT, [height, 1])
        return event

    def get_raw_transaction(self, tx_hash: str) -> dict:
        """
        This interface is used to get the corresponding transaction information based on the specified hash value.

        :param tx_hash: str, a hexadecimal hash value.
        :return: dict
        """
        tx = self.__post(RPC_GET_TRANSACTION, [tx_hash, 1])
        return tx

    def get_smart_contract(self, contract_address: str) -> dict:
        """
        This interface is used to get the information of smart contract based on the specified hexadecimal hash value.

        :param contract_address: str, a hexadecimal hash value.
        :return: the information of smart contract in dictionary form.
        """
        if type(contract_address) != str:
            raise SDKException(ErrorCode.param_err('a hexadecimal contract address is required.'))
        if len(contract_address) != 40:
            raise SDKException(ErrorCode.param_err('the length of the contract address should be 40 bytes.'))
        contract = self.__post(RPC_GET_SMART_CONTRACT, [contract_address, 1])
        return contract

    def get_merkle_proof(self, tx_hash: str) -> dict:
        """
        This interface is used to get the corresponding merkle proof based on the specified hexadecimal hash value.

        Args:
         tx_hash (str):
            an hexadecimal transaction hash value.

        Return:
            the merkle proof in dictionary form.
        """

        proof = self.__post(RPC_GET_MERKLE_PROOF, [tx_hash, 1])
        return proof

    def send_raw_transaction(self, tx: Transaction) -> str:
        """
        This interface is used to send the transaction into the network.

        Args:
         tx (Transaction):
            Transaction object in ontology Python SDK.

        Return:
            a hexadecimal transaction hash value.
        """

        tx_data = tx.serialize(is_hex=True).decode('ascii')
        tx_hash = self.__post(RPC_SEND_TRANSACTION, [tx_data])
        return tx_hash

    def send_raw_transaction_pre_exec(self, tx: Transaction, is_full: bool = False):
        """
        This interface is used to send the transaction that is prepare to execute.

        :param tx: Transaction object in ontology Python SDK.
        :param is_full: Whether to return all information.
        :return: the execution result of transaction that is prepare to execute.
        """
        tx_data = tx.serialize(is_hex=True).decode('ascii')
        response = self.__post(RPC_SEND_TRANSACTION, [tx_data, 1])
        if is_full:
            return response
        return response["Result"]
