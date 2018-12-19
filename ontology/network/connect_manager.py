#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
from enum import Enum, unique

from ontology.core.transaction import Transaction
from ontology.network.restful import RestfulClient
from ontology.network.rpc import RpcClient
from ontology.common.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.network.websocket import WebsocketClient

TEST_RPC_ADDRESS = ['http://polaris1.ont.io:20336', 'http://polaris2.ont.io:20336', 'http://polaris3.ont.io:20336']
TEST_WS_ADDRESS = ['ws://polaris1.ont.io:20335', 'ws://polaris2.ont.io:20335', 'ws://polaris3.ont.io:20335']
TEST_RESTFUL_ADDRESS = ['http://polaris1.ont.io:20334', 'http://polaris2.ont.io:20334', 'http://polaris3.ont.io:20334']

MAIN_RPC_ADDRESS = ['http://dappnode1.ont.io:20336', 'http://dappnode2.ont.io:20336']
MAIN_WS_ADDRESS = ['ws://dappnode1.ont.io:20335', 'ws://dappnode2.ont.io:20335']


@unique
class ConnectType(Enum):
    RPC = 0
    Restful = 1
    Websocket = 2


class ConnectMgr(object):
    def __init__(self, url: str = '', connect_type: ConnectType = ConnectType.RPC):
        if connect_type == ConnectType.RPC:
            self.__connector = RpcClient(url=url)
        elif connect_type == ConnectType.Restful:
            self.__connector = RestfulClient(url=url)
        elif connect_type == ConnectType.Websocket:
            self.__connector = WebsocketClient(url=url)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def is_rpc(self):
        if isinstance(self.__connector, RpcClient):
            return True
        return False

    def is_restful(self):
        if isinstance(self.__connector, RestfulClient):
            return True
        return False

    def is_websocket(self):
        if isinstance(self.__connector, WebsocketClient):
            return True
        return False

    def set_address(self, url: str):
        if isinstance(self.__connector, RpcClient) or isinstance(self.__connector, WebsocketClient):
            self.__connector.set_address(url)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_address(self) -> str:
        if isinstance(self.__connector, RpcClient) or isinstance(self.__connector, WebsocketClient):
            return self.__connector.get_address()
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def set_connect_test_net(self):
        if isinstance(self.__connector, RpcClient):
            rpc_address = choice(TEST_RPC_ADDRESS)
            self.__connector.set_address(rpc_address)
        elif isinstance(self.__connector, WebsocketClient):
            ws_address = choice(TEST_WS_ADDRESS)
            self.__connector.set_address(ws_address)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def set_connect_main_net(self):
        if isinstance(self.__connector, RpcClient):
            rpc_address = choice(MAIN_RPC_ADDRESS)
            self.__connector.set_address(rpc_address)
        elif isinstance(self.__connector, WebsocketClient):
            ws_address = choice(MAIN_WS_ADDRESS)
            self.__connector.set_address(ws_address)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_version(self, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_version(is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_connection_count(self, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_connection_count(is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_gas_price(self, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_gas_price(is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_network_id(self, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_network_id(is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_block_by_hash(self, block_hash: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_block_by_hash(block_hash, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_block_by_height(self, height: int, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_block_by_height(height, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_block_height(self, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_block_height(is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_block_height_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_block_height_by_tx_hash(tx_hash, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_block_count_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_block_count_by_tx_hash(tx_hash, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_current_block_hash(self, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_current_block_hash(is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_block_hash_by_height(self, height: int, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_block_hash_by_height(height, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_balance(self, b58_address: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_balance(b58_address, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_grant_ong(self, b58_address: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_grant_ong(b58_address, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_allowance(self, asset_name: str, from_address: str, to_address: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_allowance(asset_name, from_address, to_address, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_storage(self, hex_contract_address: str, hex_key: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_storage(hex_contract_address, hex_key, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_smart_contract_event_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_smart_contract_event_by_tx_hash(tx_hash, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_smart_contract_event_by_height(self, height: int, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_smart_contract_event_by_height(height, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_transaction_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_transaction_by_tx_hash(tx_hash, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_smart_contract_event_by_count(self, count: int, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_smart_contract_event_by_count(count, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_smart_contract(self, hex_contract_address: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_smart_contract(hex_contract_address, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_merkle_proof(self, tx_hash: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_merkle_proof(tx_hash, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def send_raw_transaction(self, tx: Transaction, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.send_raw_transaction(tx, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def send_raw_transaction_pre_exec(self, tx: Transaction, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.send_raw_transaction_pre_exec(tx, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_memory_pool_tx_count(self, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_memory_pool_tx_count(is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))

    def get_memory_pool_tx_state(self, tx_hash: str, is_full: bool = False):
        if self.is_rpc() or self.is_restful():
            return self.__connector.get_memory_pool_tx_state(tx_hash, is_full)
        else:
            raise SDKException(ErrorCode.other_error('Invalid connect type'))
