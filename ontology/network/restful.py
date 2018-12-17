#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

from typing import List
from urllib.parse import urljoin

from ontology.common.error_code import ErrorCode
from ontology.exception.exception import SDKException


class RestfulMethod(object):
    GET_VERSION = '/api/v1/version'
    GET_CONNECTION_COUNT = '/api/v1/node/connectioncount'
    GET_GAS_PRICE = '/api/v1/gasprice'

    SEND_TRANSACTION = '/api/v1/transaction'
    GET_TRANSACTION = '/api/v1/transaction/'
    GET_GENERATE_BLOCK_TIME = '/api/v1/node/generateblocktime'
    GET_BLOCK_HEIGHT = '/api/v1/block/height'
    GET_BLOCK_BY_HEIGHT = '/api/v1/block/details/height/'
    GET_BLOCK_BY_HASH = '/api/v1/block/details/hash/'
    GET_ACCOUNT_BALANCE = '/api/v1/balance/'
    GET_CONTRACT_STATE = '/api/v1/contract/'
    GET_SMART_CODE_EVENT_TXS_BY_HEIGHT = '/api/v1/smartcode/event/transactions/'
    GET_SMART_CODE_EVENT_BY_TXHASH = '/api/v1/smartcode/event/txhash/'
    GET_BLOCK_HEIGHT_BY_TXHASH = '/api/v1/block/height/txhash/'
    GET_STORAGE = '/api/v1/storage/'
    GET_MERKLE_PROOF = '/api/v1/merkleproof/'
    GET_MEM_POOL_TX_COUNT = '/api/v1/mempool/txcount'
    GET_MEM_POOL_TX_STATE = '/api/v1/mempool/txstate/'
    GET_ALLOWANCE = '/api/v1/allowance/'
    GET_GRANT_ONG = '/api/v1/grantong'
    GET_NETWORK_ID = '/api/v1/networkid'


class RestfulClient(object):
    def __init__(self, url: str = ''):
        self.__url = url

    def set_address(self, url: str):
        self.__url = url

    def get_address(self):
        return self.__url

    def __generate_get_url(self, method: str, *param):
        url = urljoin(self.__url, method)
        for p in param:
            url = urljoin(url, p)
        return url

    def __get(self, url: str):
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0]))
        except requests.exceptions.ConnectTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectTimeout: ', self.__url])))
        except requests.exceptions.ConnectionError:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectionError: ', self.__url])))
        if response.status_code != 200:
            raise SDKException(ErrorCode.other_error(response.content.decode('utf-8')))
        try:
            response = json.loads(response.content.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        if response['Error'] != 0:
            raise SDKException(ErrorCode.other_error(response['Result']))
        return response

    def get_version(self, is_full: bool = False):
        url = self.__generate_get_url(RestfulMethod.GET_VERSION)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_connection_count(self, is_full: bool = False) -> int:
        url = self.__generate_get_url(RestfulMethod.GET_CONNECTION_COUNT)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_gas_price(self, is_full: bool = False) -> int or dict:
        url = self.__generate_get_url(RestfulMethod.GET_GAS_PRICE)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']['gasprice']

    def get_network_id(self, is_full: bool = False) -> int or dict:
        url = self.__generate_get_url(RestfulMethod.GET_NETWORK_ID)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_block_by_hash(self, block_hash: str, is_full: bool = False) -> int or dict:
        url = self.__generate_get_url(RestfulMethod.GET_BLOCK_BY_HASH, block_hash)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_block_by_height(self, height: int, is_full: bool = False):
        url = self.__generate_get_url(RestfulMethod.GET_BLOCK_BY_HEIGHT, height)
        response = self.__get(url)
        print(response)
        if is_full:
            return response
        return response['Result']
