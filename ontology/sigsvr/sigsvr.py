#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import platform

import requests

from sys import maxsize

from Cryptodome.Random.random import randint

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class SigSvr(object):
    def __init__(self, url: str = ''):
        self.__url = url

    def set_address(self, url: str):
        self.__url = url

    def get_address(self):
        return self.__url

    def connect_to_localhost(self):
        self.set_address('http://localhost:20000/cli')

    def __post(self, method, b58_address: str or None, pwd: str or None, params):
        header = {'Content-type': 'application/json'}
        payload = dict(qid=str(randint(0, maxsize)), method=method, params=params)
        if isinstance(b58_address, str):
            payload['account'] = b58_address
        if isinstance(pwd, str):
            payload['pwd'] = pwd
        try:
            response = requests.post(self.__url, json=payload, headers=header, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0])) from None
        except requests.exceptions.ConnectTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectTimeout: ', self.__url]))) from None
        except requests.exceptions.ConnectionError:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectionError: ', self.__url]))) from None
        except requests.exceptions.ReadTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ReadTimeout: ', self.__url]))) from None
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
        if content['error_code'] != 0:
            if content['error_info'] != '':
                raise SDKException(ErrorCode.other_error(content['error_info']))
            else:
                raise SDKException(ErrorCode.other_error(content['result']))
        return content

    def create_account(self, pwd: str, is_full: bool = False) -> dict or str:
        response = self.__post('createaccount', None, pwd, dict())
        if is_full:
            return response
        return response['result']

    def export_account(self, wallet_path: str = '', is_full: bool = False) -> dict or str:
        params = dict()
        if len(wallet_path) != 0:
            params['wallet_path'] = wallet_path
        response = self.__post('exportaccount', None, None, params)
        if 'Windows' in platform.platform():
            response['result']['wallet_file'] = response['result']['wallet_file'].replace('/', '\\')
        if is_full:
            return response
        return response['result']

    def sig_data(self, hex_data: str, b58_address: str, pwd: str, is_full: bool = False) -> dict or str:
        params = dict(raw_data=hex_data)
        response = self.__post('sigdata', b58_address, pwd, params)
        if is_full:
            return response
        return response['result']
