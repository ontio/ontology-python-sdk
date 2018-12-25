#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class AccountData(object):
    def __init__(self, address: str = '', enc_alg: str = "aes-256-gcm", key: str = "", algorithm="ECDSA", salt="",
                 param: dict = None, label: str = "", public_key: str = "", sign_scheme: str = "SHA256withECDSA",
                 is_default: bool = True, lock: bool = False):
        if param is None:
            param = {"curve": "P-256"}
        self.__b58_address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.is_default = is_default
        self.__key = key
        self.__label = label
        self.lock = lock
        self.parameters = param
        self.salt = salt
        self.__public_key = public_key
        self.signature_scheme = sign_scheme

    def __iter__(self):
        data = dict()
        data['address'] = self.__b58_address
        data['algorithm'] = self.algorithm
        data['enc-alg'] = self.enc_alg
        data['isDefault'] = self.is_default
        data['key'] = self.__key
        data['label'] = self.__label
        data['lock'] = self.lock
        data['parameters'] = self.parameters
        data['salt'] = self.salt
        data['publicKey'] = self.__public_key
        data['signatureScheme'] = self.signature_scheme
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
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def public_key(self):
        return self.__public_key

    @public_key.setter
    def public_key(self, pub_key):
        self.__public_key = pub_key

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, label: str):
        if not isinstance(label, str):
            raise SDKException(ErrorCode.other_error('Invalid label.'))
        self.__label = label




    def get_public_key_bytes(self):
        return self.public_key

    def get_key(self):
        return self.key
