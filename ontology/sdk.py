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
import asyncio
import inspect

from typing import Union

from Cryptodome.Random.random import choice

from ontology.network.aiorpc import AioRpc
from ontology.contract.neo.vm import NeoVm
from ontology.service.service import Service
from ontology.contract.native.vm import NativeVm
from ontology.network.websocket import Websocket
from ontology.network.aiorestful import AioRestful
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.wallet.wallet_manager import WalletManager
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.network.rpc import Rpc, TEST_RPC_ADDRESS, MAIN_RPC_ADDRESS
from ontology.network.restful import Restful, TEST_RESTFUL_ADDRESS, MAIN_RESTFUL_ADDRESS


class _Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance


class AioRunner(object):

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


class Ontology(AioRunner, metaclass=_Singleton):
    def __init__(self, rpc_address: str = '', restful_address: str = '', ws_address: str = '',
                 default_signature_scheme: SignatureScheme = SignatureScheme.SHA256withECDSA):
        if not isinstance(default_signature_scheme, SignatureScheme):
            raise SDKException(ErrorCode.param_err('SignatureScheme object is required.'))
        self.__rpc = Rpc(rpc_address)
        self.__aio_rpc = AioRpc(rpc_address)
        self.__restful = Restful(restful_address)
        self.__aio_restful = AioRestful(restful_address)
        self.__websocket = Websocket(ws_address)
        self.__default_network = self.__rpc
        self.__default_aio_network = self.__aio_rpc
        self.__native_vm = NativeVm(self)
        self.__neo_vm = NeoVm(self)
        self.__service = Service(self)
        self.__wallet_manager = WalletManager()
        self.__default_signature_scheme = default_signature_scheme

    @property
    def default_network(self):
        return self.__default_network

    @default_network.setter
    def default_network(self, network: Union[Rpc, Restful]):
        self.__default_network = network

    @property
    def default_aio_network(self):
        return self.__default_aio_network

    @default_aio_network.setter
    def default_aio_network(self, network: Union[AioRpc, AioRestful, Websocket]):
        self.__default_aio_network = network

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
    def rpc(self) -> Rpc:
        return self.__rpc

    @rpc.setter
    def rpc(self, rpc_client: Rpc):
        if isinstance(rpc_client, Rpc):
            self.__rpc = rpc_client

    @property
    def aio_rpc(self) -> AioRpc:
        return self.__aio_rpc

    @aio_rpc.setter
    def aio_rpc(self, aio_rpc: AioRpc):
        if isinstance(aio_rpc, AioRpc):
            self.__rpc = aio_rpc

    @property
    def restful(self) -> Restful:
        return self.__restful

    @restful.setter
    def restful(self, restful_client: Restful):
        if isinstance(restful_client, Restful):
            self.__restful = restful_client

    @property
    def aio_restful(self) -> AioRestful:
        return self.__aio_restful

    @restful.setter
    def restful(self, aio_restful: AioRestful):
        if isinstance(aio_restful, AioRestful):
            self.__aio_restful = aio_restful

    @property
    def websocket(self) -> Websocket:
        return self.__websocket

    @websocket.setter
    def websocket(self, websocket_client: Websocket):
        if isinstance(websocket_client, Websocket):
            self.__websocket = websocket_client

    @property
    def rpc_address(self):
        if self.__rpc is None:
            return ''
        return self.__rpc.get_address()

    @rpc_address.setter
    def rpc_address(self, rpc_address: str):
        if isinstance(self.__rpc, Rpc):
            self.__rpc.set_address(rpc_address)
        else:
            self.__rpc = Rpc(rpc_address)

    @property
    def restful_address(self):
        if not isinstance(self.__restful, Restful):
            return ''
        return self.__restful.get_address()

    @restful_address.setter
    def restful_address(self, restful_address: str):
        if isinstance(self.__restful, Restful):
            self.__restful.set_address(restful_address)
        else:
            self.__restful = Restful(restful_address)

    @property
    def websocket_address(self) -> str:
        if not isinstance(self.__websocket, Websocket):
            return ''
        return self.__websocket.get_address()

    @websocket_address.setter
    def websocket_address(self, websocket_address: str):
        if isinstance(self.__websocket, Websocket):
            self.__websocket.set_address(websocket_address)
        else:
            self.__websocket = Websocket(websocket_address)

    @property
    def native_vm(self):
        return self.__native_vm

    @property
    def neo_vm(self):
        return self.__neo_vm

    @property
    def service(self):
        return self.__service

    @staticmethod
    def get_random_test_rpc_address():
        return choice(TEST_RPC_ADDRESS)

    @staticmethod
    def get_random_main_rpc_address():
        return choice(MAIN_RPC_ADDRESS)

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
