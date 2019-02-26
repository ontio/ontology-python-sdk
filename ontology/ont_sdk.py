#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

from Cryptodome.Random.random import choice

from ontology.sigsvr.sigsvr import SigSvr
from ontology.service.service import Service
from ontology.smart_contract.neo_vm import NeoVm
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.smart_contract.native_vm import NativeVm
from ontology.network.websocket import WebsocketClient
from ontology.wallet.wallet_manager import WalletManager
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.network.rpc import RpcClient, TEST_RPC_ADDRESS, MAIN_RPC_ADDRESS
from ontology.network.restful import RestfulClient, TEST_RESTFUL_ADDRESS, MAIN_RESTFUL_ADDRESS


class OntologySdk(object):
    _instance_lock = threading.Lock()

    def __init__(self, rpc_address: str = '', restful_address: str = '', ws_address: str = '', sig_svr_address='',
                 default_signature_scheme: SignatureScheme = SignatureScheme.SHA256withECDSA):
        if not isinstance(default_signature_scheme, SignatureScheme):
            raise SDKException(ErrorCode.param_err('SignatureScheme object is required.'))
        self.__rpc = RpcClient(rpc_address)
        self.__restful = RestfulClient(restful_address)
        self.__websocket = WebsocketClient(ws_address)
        self.__native_vm = NativeVm(self._instance)
        self.__neo_vm = NeoVm(self._instance)
        self.__service = Service(self._instance)
        self.__wallet_manager = WalletManager()
        self.__default_signature_scheme = default_signature_scheme

    def __new__(cls, *args, **kwargs):
        if not hasattr(OntologySdk, '_instance'):
            with OntologySdk._instance_lock:
                if not hasattr(OntologySdk, '_instance'):
                    OntologySdk._instance = object.__new__(cls)
        return OntologySdk._instance

    def get_network(self) -> RpcClient or RestfulClient:
        if self.__rpc.get_address() != '':
            return self.__rpc
        elif self.__restful.get_address() != '':
            return self.__restful
        else:
            raise SDKException(ErrorCode.other_error('Invalid network instance.'))

    @property
    def wallet_manager(self):
        if self.__wallet_manager is None:
            self.__wallet_manager = WalletManager()
        return self.__wallet_manager

    @wallet_manager.setter
    def wallet_manager(self, wallet_manager: WalletManager):
        if isinstance(self.wallet_manager, WalletManager):
            self.__wallet_manager = wallet_manager
        else:
            raise SDKException(ErrorCode.other_error('Invalid WalletManager instance'))

    @property
    def default_signature_scheme(self):
        if self.__default_signature_scheme is None:
            self.__default_signature_scheme = SignatureScheme.SHA256withECDSA
        return self.__default_signature_scheme

    @default_signature_scheme.setter
    def default_signature_scheme(self, scheme: SignatureScheme):
        if isinstance(scheme, SignatureScheme):
            self.__default_signature_scheme = scheme
            self.__wallet_manager.set_signature_scheme(scheme)
        else:
            raise SDKException(ErrorCode.other_error('Invalid signature scheme'))

    @property
    def rpc(self) -> RpcClient:
        return self.__rpc

    @rpc.setter
    def rpc(self, rpc_client: RpcClient):
        if isinstance(rpc_client, RpcClient):
            self.__rpc = rpc_client

    @property
    def restful(self) -> RestfulClient:
        return self.__restful

    @restful.setter
    def restful(self, restful_client: RestfulClient):
        if isinstance(restful_client, RestfulClient):
            self.__restful = restful_client

    @property
    def websocket(self) -> WebsocketClient:
        return self.__websocket

    @websocket.setter
    def websocket(self, websocket_client: WebsocketClient):
        if isinstance(websocket_client, WebsocketClient):
            self.__websocket = websocket_client

    @property
    def native_vm(self):
        return self.__native_vm

    @property
    def neo_vm(self):
        return self.__neo_vm

    @property
    def service(self):
        return self.__service

    def set_rpc_address(self, rpc_address: str):
        if isinstance(self.__rpc, RpcClient):
            self.__rpc.set_address(rpc_address)
        else:
            self.__rpc = RpcClient(rpc_address)

    def get_rpc_address(self):
        if self.__rpc is None:
            return ''
        return self.__rpc.get_address()

    @staticmethod
    def get_random_test_rpc_address():
        return choice(TEST_RPC_ADDRESS)

    @staticmethod
    def get_random_main_rpc_address():
        return choice(MAIN_RPC_ADDRESS)

    def set_restful_address(self, restful_address: str):
        if isinstance(self.__restful, RestfulClient):
            self.__restful.set_address(restful_address)
        else:
            self.__restful = RestfulClient(restful_address)

    def get_restful_address(self):
        if not isinstance(self.__restful, RestfulClient):
            return ''
        return self.__restful.get_address()

    @staticmethod
    def get_random_test_restful_address():
        choice(TEST_RESTFUL_ADDRESS)

    @staticmethod
    def get_random_main_restful_address():
        return choice(MAIN_RESTFUL_ADDRESS)

    @staticmethod
    def get_test_net_restful_address_list():
        return TEST_RESTFUL_ADDRESS

    @staticmethod
    def get_main_net_restful_address_list():
        return MAIN_RESTFUL_ADDRESS

    def set_websocket_address(self, websocket_address: str):
        if isinstance(self.__websocket, WebsocketClient):
            self.__websocket.set_address(websocket_address)
        else:
            self.__websocket = WebsocketClient(websocket_address)

    def get_websocket_address(self):
        if not isinstance(self.__websocket, WebsocketClient):
            return ''
        return self.__websocket.get_address()
