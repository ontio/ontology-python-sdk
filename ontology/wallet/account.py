#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class AccountData(object):
    def __init__(self, b58_address: str = '', enc_alg: str = "aes-256-gcm", key: str = "", algorithm: str = 'ECDSA',
                 salt="", param: dict = None, label: str = "", public_key: str = "",
                 sig_scheme: str = 'SHA256withECDSA', is_default: bool = True, lock: bool = False):
        if param is None:
            param = dict(curve='P-256')
        self.__b58_address = b58_address
        self.__algorithm = algorithm
        self.__enc_alg = enc_alg
        self.__is_default = is_default
        self.__key = key
        self.__label = label
        self.__lock = lock
        self.parameters = param
        self.__salt = salt
        self.__public_key = public_key
        self.__signature_scheme = sig_scheme

    def __iter__(self):
        data = dict()
        data['address'] = self.__b58_address
        data['algorithm'] = self.__algorithm
        data['enc-alg'] = self.__enc_alg
        data['isDefault'] = self.__is_default
        data['key'] = self.__key
        data['label'] = self.__label
        data['lock'] = self.__lock
        data['parameters'] = self.parameters
        data['salt'] = self.__salt
        data['publicKey'] = self.__public_key
        data['signatureScheme'] = self.__signature_scheme
        for key, value in data.items():
            yield (key, value)

    # TODO: add check point

    @property
    def b58_address(self):
        return self.__b58_address

    @b58_address.setter
    def b58_address(self, b58_address):
        self.__b58_address = b58_address

    @property
    def algorithm(self):
        return self.__algorithm

    @algorithm.setter
    def algorithm(self, alg):
        self.__algorithm = alg

    @property
    def enc_alg(self):
        return self.__enc_alg

    @enc_alg.setter
    def enc_alg(self, enc_alg: str):
        if not isinstance(enc_alg, str):
            raise SDKException(ErrorCode.other_error('Invalid encryption algorithm.'))
        self.__enc_alg = enc_alg

    @property
    def is_default(self):
        return self.__is_default

    @is_default.setter
    def is_default(self, is_default: bool):
        if not isinstance(is_default, bool):
            raise SDKException(ErrorCode.other_error('Invalid default account state.'))
        self.__is_default = is_default

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, label: str):
        if not isinstance(label, str):
            raise SDKException(ErrorCode.other_error('Invalid label.'))
        self.__label = label

    @property
    def lock(self):
        return self.__lock

    @lock.setter
    def lock(self, lock: bool):
        if not isinstance(lock, bool):
            raise SDKException(ErrorCode.other_error('Invalid lock state.'))
        self.__lock = lock

    @property
    def salt(self):
        return self.__salt

    @salt.setter
    def salt(self, salt):
        self.__salt = salt

    @property
    def public_key(self):
        return self.__public_key

    @public_key.setter
    def public_key(self, pub_key):
        self.__public_key = pub_key

    @property
    def signature_scheme(self):
        return self.__signature_scheme

    @signature_scheme.setter
    def signature_scheme(self, sig_scheme: str):
        if not isinstance(sig_scheme, str):
            raise SDKException(ErrorCode.other_error('Invalid signature scheme.'))
        self.__signature_scheme = sig_scheme
