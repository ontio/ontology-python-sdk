#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from random import choice

from ontology.core.sig import Sig
from ontology.common import define
from ontology.crypto.key_type import KeyType
from ontology.account.account import Account
from ontology.smart_contract.neo_vm import NeoVm
from ontology.core.program import ProgramBuilder
from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.smart_contract.native_vm import NativeVm
from ontology.network.websocket import WebsocketClient
from ontology.wallet.wallet_manager import WalletManager
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.crypto.signature_handler import SignatureHandler
from ontology.network.rpc import RpcClient, TEST_RPC_ADDRESS, MAIN_RPC_ADDRESS
from ontology.network.restful import RestfulClient, TEST_RESTFUL_ADDRESS, MAIN_RESTFUL_ADDRESS


class OntologySdk(object):
    _instance_lock = threading.Lock()

    def __init__(self, rpc_address: str = '', restful_address: str = '', ws_address: str = '',
                 default_signature_scheme: SignatureScheme = SignatureScheme.SHA256withECDSA):
        self.__rpc = RpcClient(rpc_address)
        self.__restful = RestfulClient(restful_address)
        self.__websocket = WebsocketClient(ws_address)
        self.__wallet_manager = WalletManager()
        self.__native_vm = None
        self.__neo_vm = None
        self.__default_signature_scheme = default_signature_scheme

    def __new__(cls, *args, **kwargs):
        if not hasattr(OntologySdk, '_instance'):
            with OntologySdk._instance_lock:
                if not hasattr(OntologySdk, '_instance'):
                    OntologySdk._instance = object.__new__(cls)
        return OntologySdk._instance

    def get_network(self) -> RpcClient or RestfulClient or WebsocketClient:
        if self.__rpc.get_address() != '':
            return self.__rpc
        elif self.__restful.get_address() != '':
            return self.__restful
        elif self.__websocket.get_address() != '':
            return self.__websocket
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
        if self.__native_vm is None:
            self.__native_vm = NativeVm(self._instance)
        return self.__native_vm

    @property
    def neo_vm(self):
        if self.__neo_vm is None:
            self.__neo_vm = NeoVm(self._instance)
        return self.__neo_vm

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

    @staticmethod
    def get_test_net_rpc_address():
        return TEST_RPC_ADDRESS

    @staticmethod
    def get_main_net_rpc_address():
        return MAIN_RPC_ADDRESS

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

    @staticmethod
    def sign_transaction(tx: Transaction, signer: Account) -> Transaction:
        """
        This interface is used to sign the transaction.

        :param tx: a Transaction object which will be signed.
        :param signer: an Account object which will sign the transaction.
        :return: a Transaction object which has been signed.
        """
        tx_hash = tx.hash256_bytes()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        sig = [Sig([signer.get_public_key_bytes()], 1, [sig_data])]
        tx.sigs = sig
        return tx

    @staticmethod
    def add_sign_transaction(tx: Transaction, signer: Account):
        """
        This interface is used to add signature into the transaction.

        :param tx: a Transaction object which will be signed.
        :param signer: an Account object which will sign the transaction.
        :return: a Transaction object which has been signed.
        """
        if tx.sigs is None or len(tx.sigs) == 0:
            tx.sigs = []
        elif len(tx.sigs) >= define.TX_MAX_SIG_SIZE:
            raise SDKException(ErrorCode.param_err('the number of transaction signatures should not be over 16'))
        tx_hash = tx.hash256_bytes()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        sig = Sig([signer.get_public_key_bytes()], 1, [sig_data])
        tx.sigs.append(sig)
        return tx

    @staticmethod
    def add_multi_sign_transaction(tx: Transaction, m: int, pub_keys: list, signer: Account):
        """
        This interface is used to generate an Transaction object which has multi signature.

        :param tx: a Transaction object which will be signed.
        :param m: the amount of signer.
        :param pub_keys: a list of public keys.
        :param signer: an Account object which will sign the transaction.
        :return: a Transaction object which has been signed.
        """
        pub_keys = ProgramBuilder.sort_public_keys(pub_keys)
        tx_hash = tx.hash256_bytes()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        if tx.sigs is None or len(tx.sigs) == 0:
            tx.sigs = []
        elif len(tx.sigs) >= define.TX_MAX_SIG_SIZE:
            raise SDKException(ErrorCode.param_err('the number of transaction signatures should not be over 16'))
        else:
            for i in range(len(tx.sigs)):
                if tx.sigs[i].public_keys == pub_keys:
                    if len(tx.sigs[i].sig_data) + 1 > len(pub_keys):
                        raise SDKException(ErrorCode.param_err('too more sigData'))
                    if tx.sigs[i].M != m:
                        raise SDKException(ErrorCode.param_err('M error'))
                    tx.sigs[i].sig_data.append(sig_data)
                    return tx
        sig = Sig(pub_keys, m, [sig_data])
        tx.sigs.append(sig)
        return tx

    @staticmethod
    def signature_data(acct: Account, data: bytearray or bytes):
        return acct.generate_signature(data, acct.get_signature_scheme())

    @staticmethod
    def verify_signature(public_key: bytearray, data: bytearray, signature: bytearray):
        if len(public_key) == 33:
            key_type = KeyType.ECDSA
        elif len(public_key) == 35:
            key_type = KeyType.from_label(public_key[0])
        else:
            raise SDKException(ErrorCode.other_error('Unsupported key type'))
        if key_type == KeyType.ECDSA:
            handler = SignatureHandler(key_type, SignatureScheme.SHA256withECDSA)
        elif key_type == KeyType.SM2:
            handler = SignatureHandler(key_type, SignatureScheme.SM3withSM2)
        else:
            raise SDKException(ErrorCode.other_error('Unsupported key type'))
        return handler.verify_signature(public_key, data, signature)
