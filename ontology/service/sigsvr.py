#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import threading
from sys import maxsize

import requests
from Cryptodome.Random.random import randint

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class SigSvr(object):
    _instance_lock = threading.Lock()

    def __init__(self, url: str = ''):
        self.__url = url

    def __new__(cls, *args, **kwargs):
        if not hasattr(SigSvr, '_instance'):
            with SigSvr._instance_lock:
                if not hasattr(SigSvr, '_instance'):
                    SigSvr._instance = object.__new__(cls)
        return SigSvr._instance

    def set_address(self, url: str):
        self.__url = url

    def get_address(self):
        return self.__url

    def connect_to_localhost(self):
        self.set_address('http://localhost:20000/cli')

    def __post(self, method, pwd, params):
        header = {'Content-type': 'application/json'}
        payload = dict(qid=randint(0, maxsize), method=method, pwd=pwd, params=params)
        try:
            response = requests.post(self.__url, json=payload, headers=header, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0])) from None
        except requests.exceptions.ConnectTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectTimeout: ', url]))) from None
        except requests.exceptions.ConnectionError:
            raise SDKException(ErrorCode.other_error(''.join(['ConnectionError: ', url]))) from None
        except requests.exceptions.ReadTimeout:
            raise SDKException(ErrorCode.other_error(''.join(['ReadTimeout: ', url]))) from None
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

    def create_account(self, pwd: str, is_full: bool = False) -> dict or str:
        response = self.__post('createaccount', pwd, dict())
        if is_full:
            return response
        return response['result']
