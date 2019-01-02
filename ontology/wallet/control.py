#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Control(object):
    def __init__(self, kid="", address='', enc_alg="aes-256-gcm", key="", algorithm='ECDSA', salt="", param=None,
                 hash_value="sha256", public_key=""):
        if param is None:
            param = {"curve": "P-256"}
        self.address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.hash = hash_value
        self.kid = kid
        self.key = key
        self.parameters = param
        self.salt = salt
        self.__public_key = public_key

    def __iter__(self):
        data = dict()
        data['address'] = self.address
        data['algorithm'] = self.algorithm
        data['enc-alg'] = self.enc_alg
        data['hash'] = self.hash
        data['id'] = self.kid
        data['key'] = self.key
        data['parameters'] = self.parameters
        data['salt'] = self.salt
        data['publicKey'] = self.__public_key
        for key, value in data.items():
            yield (key, value)

    @staticmethod
    def dict2obj(control_data: dict):
        try:
            hash_value = control_data['hash']
        except Exception as e:
            hash_value = "sha256"
        try:
            public_key = control_data['publicKey']
        except Exception as e:
            public_key = ""
        obj = Control(kid=control_data['id'], address=control_data['address'], enc_alg=control_data['enc-alg'],
                      key=control_data['key'], algorithm=control_data['algorithm'], salt=control_data['salt'],
                      param=control_data['parameters'], hash_value=hash_value,
                      public_key=public_key)
        return obj

    @property
    def public_key(self):
        return self.__public_key

    @public_key.setter
    def public_key(self, b64_pub_key: str):
        if not isinstance(b64_pub_key, str):
            raise SDKException(ErrorCode.other_error('Invalid public key.'))
        self.__public_key = b64_pub_key
