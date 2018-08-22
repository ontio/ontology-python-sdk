#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

from ontology.rpc.define import *
from ontology.common.address import Address
from ontology.common.error_code import ErrorCode
from ontology.utils.util import get_asset_address
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException


class HttpRequest(object):
    _timeout = 10

    @staticmethod
    def set_timeout(timeout=10):
        HttpRequest._timeout = timeout

    @staticmethod
    def request(method, url, payload):
        header = {'Content-type': 'application/json'}
        if method == "post":
            res = requests.post(url, json=payload, headers=header, timeout=HttpRequest._timeout)
            return res
        elif method == "get":
            res = requests.get(url, params=json.dumps(payload), timeout=HttpRequest._timeout)
            return res


class RpcClient(object):
    def __init__(self, qid=0, addr=None):
        self.qid = qid
        self.addr = addr

    def set_address(self, addr):
        self.addr = addr

    @staticmethod
    def set_json_rpc_version(method, param=None):
        JsonRpcRequest["jsonrpc"] = JSON_RPC_VERSION
        JsonRpcRequest["id"] = "1"
        JsonRpcRequest["method"] = method
        if param is None:
            JsonRpcRequest["params"] = list()
        else:
            JsonRpcRequest["params"] = param
        return JsonRpcRequest

    def get_version(self) -> str:
        """
        This interface is used to get the version information of the connected node in current network.

        Return:
            the version information of the connected node.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_VERSION, [])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        version = json.loads(r.content.decode())["result"]
        return version

    def get_node_count(self) -> int:
        """
        This interface is used to get the current number of connections for the node in current network.

        Return:
            the number of connections.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_NODE_COUNT, [])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        count = json.loads(r.content.decode())["result"]
        return count

    def get_gas_price(self) -> int:
        """
        This interface is used to get the gas price in current network.

        Return:
            the value of gas price.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_GAS_PRICE, [])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        price = json.loads(r.content.decode())["result"]['gasprice']
        return price

    def get_network_id(self) -> int:
        """
        This interface is used to get the network id of current network.

        Return:
            the network id of current network.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_NETWORK_ID, [])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        id = json.loads(r.content.decode())["result"]
        return id

    def get_block_by_hash(self, block_hash: str) -> dict:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.

        Args:
         block_hash (str):
            a hexadecimal value of block hash

        Return:
            the block information of the specified block hash.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_BLOCK, [block_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        dict_block = json.loads(r.content.decode())["result"]
        return dict_block

    def get_block_by_height(self, height: int) -> dict:
        """
        This interface is used to get the block information by block height in current network.

        Return:
            the decimal total number of blocks in current network.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_BLOCK, [height, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        block = json.loads(r.content.decode())["result"]
        return block

    def get_block_count(self) -> int:
        """
        This interface is used to get the decimal block number in current network.

        Return:
            the decimal total number of blocks in current network.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_BLOCK_COUNT)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        count = json.loads(r.content.decode())["result"]
        return count

    def get_current_block_hash(self) -> str:
        """
        This interface is used to get the hexadecimal hash value of the highest block in current network.

        Return:
            the hexadecimal hash value of the highest block in current network.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_CURRENT_BLOCK_HASH)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_block_hash_by_height(self, height: int) -> str:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.

        Args:
         height (int):
            a decimal block height value

        Return:
            the hexadecimal hash value of the specified block height.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_BLOCK_HASH, [height, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        block_hash = json.loads(r.content.decode())["result"]
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

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_BALANCE, [base58_address, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        balance = json.loads(r.content.decode())["result"]
        return balance

    def get_allowance(self, base58_address: str) -> str:
        """
        This interface is used to get the the allowance
        from transfer-from account to transfer-to account in current network.

        Args:
         base58_address (str):
            a base58 encoded account address

        Return:
            the information of smart contract event in dictionary form.
        """

        contract_address = get_asset_address("ont")
        b58_contract_address = Address(contract_address).b58encode()
        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_ALLOWANCE, ["ong", b58_contract_address, base58_address])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        allowance = json.loads(r.content.decode())["result"]
        return allowance

    def get_storage(self, contract_address: str, key: str) -> int:
        """
        This interface is used to get the corresponding stored value
        based on hexadecimal contract address and stored key.

        Args:
         contract_address (str):
            hexadecimal contract address
         key (str):
            a hexadecimal stored key

        Return:
            the information of smart contract event in dictionary form.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_STORAGE, [contract_address, key, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        s = json.loads(r.content.decode())["result"]
        s = bytearray.fromhex(s)
        value = (s[0]) | (s[1]) << 8 | (s[2]) << 16 | (s[3]) << 24 | (s[4]) << 32 | (s[5]) << 40 | (s[6]) << 48 | (
            s[7]) << 56
        return value

    def get_smart_contract_event_by_tx_hash(self, tx_hash: str) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.

        Args:
         tx_hash (str):
            a hexadecimal hash value

        Return:
            the information of smart contract event in dictionary form.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_SMART_CONTRACT_EVENT, [tx_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        event = json.loads(r.content.decode())["result"]
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

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_SMART_CONTRACT_EVENT, [height, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        event = json.loads(r.content.decode())["result"]
        return event

    def get_raw_transaction(self, tx_hash: str) -> dict:
        """
        This interface is used to get the corresponding transaction information based on the specified hash value.

        Args:
         tx_hash (str):
            a hexadecimal hash value.

        Return:
            the information of transaction in dictionary form.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_TRANSACTION, [tx_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        tx = json.loads(r.content.decode())["result"]
        return tx

    def get_smart_contract(self, contract_address) -> dict:
        """
        This interface is used to get the information of smart contract based on the specified hexadecimal hash value.

        Args:
         contract_address (str):
            a hexadecimal hash value.

        Return:
            the information of smart contract in dictionary form.
        """

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_SMART_CONTRACT, [contract_address, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        contract = json.loads(r.content.decode())["result"]
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

        rpc_struct = RpcClient.set_json_rpc_version(RPC_GET_MERKLE_PROOF, [tx_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        proof = json.loads(r.content.decode())["result"]
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

        buf = tx.serialize()
        tx_data = buf.hex()
        rpc_struct = RpcClient.set_json_rpc_version(RPC_SEND_TRANSACTION, [tx_data])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        data = json.loads(r.content.decode())
        res = data["result"]
        if data["error"] != 0:
            raise SDKException(ErrorCode.other_error(res))
        return res

    def send_raw_transaction_pre_exec(self, tx: Transaction):
        """
        This interface is used to send the transaction that is prepare to execute.

        Args:
         tx (Transaction):
            Transaction object in ontology Python SDK.

        Return:
            the execution result of transaction that is prepare to execute.
        """

        buf = tx.serialize()
        tx_data = buf.hex()
        rpc_struct = RpcClient.set_json_rpc_version(RPC_SEND_TRANSACTION, [tx_data, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())
        err = res["error"]
        if err > 0:
            raise RuntimeError("error > 0")
        if res["result"]["State"] == 0:
            raise RuntimeError("State = 0")
        return res["result"]["Result"]
