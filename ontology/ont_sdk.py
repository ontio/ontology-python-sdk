#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

from ontology.core.sig import Sig
from ontology.rpc.rpc import RpcClient
from ontology.common import define as Common
from ontology.account.account import Account
from ontology.smart_contract.neo_vm import NeoVm
from ontology.core.program import ProgramBuilder
from ontology.common.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.smart_contract.native_vm import NativeVm
from ontology.wallet.wallet_manager import WalletManager
from ontology.crypto.signature_scheme import SignatureScheme


class OntologySdk(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.rpc = RpcClient()
        self.wallet_manager = WalletManager()
        self.__native_vm = None
        self.__neo_vm = None
        self.defaultSignScheme = SignatureScheme.SHA256withECDSA

    def __new__(cls, *args, **kwargs):
        if not hasattr(OntologySdk, "_instance"):
            with OntologySdk._instance_lock:
                if not hasattr(OntologySdk, "_instance"):
                    OntologySdk._instance = object.__new__(cls)
        return OntologySdk._instance

    def native_vm(self):
        if self.__native_vm is None:
            self.__native_vm = NativeVm(OntologySdk._instance)
        return self.__native_vm

    def neo_vm(self):
        if self.__neo_vm is None:
            self.__neo_vm = NeoVm(OntologySdk._instance)
        return self.__neo_vm

    def get_wallet_manager(self):
        if self.wallet_manager is None:
            self.wallet_manager = WalletManager()
        return self.wallet_manager

    def set_rpc(self, rpc_addr: str):
        self.rpc.set_address(rpc_addr)

    def get_rpc(self):
        if self.rpc is None:
            self.rpc = RpcClient()
        return self.rpc

    def set_signature_scheme(self, scheme: SignatureScheme):
        self.defaultSignScheme = scheme
        self.wallet_manager.set_signature_scheme(scheme)

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
        elif len(tx.sigs) >= Common.TX_MAX_SIG_SIZE:
            raise SDKException(ErrorCode.param_err('the number of transaction signatures should not be over 16'))
        tx_hash = tx.hash256_bytes()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        sig = Sig([signer.serialize_public_key()], 1, [sig_data])
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
        pub_keys = ProgramBuilder.sort_publickeys(pub_keys)
        tx_hash = tx.hash256_bytes()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        if tx.sigs is None or len(tx.sigs) == 0:
            tx.sigs = []
        elif len(tx.sigs) >= Common.TX_MAX_SIG_SIZE:
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

    def open_wallet(self, wallet_file):
        return self.wallet_manager.open_wallet(wallet_file)
