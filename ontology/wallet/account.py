#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AccountData(object):
    def __init__(self, address: str = '', enc_alg: str = "aes-256-gcm", key: str = "", algorithm="ECDSA", salt="",
                 param: dict = None, label: str = "", public_key: str = "", sign_scheme: str = "SHA256withECDSA",
                 is_default: bool = True, lock: bool = False):
        if param is None:
            param = {"curve": "P-256"}
        self.address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.isDefault = is_default
        self.key = key
        self.label = label
        self.lock = lock
        self.parameters = param
        self.salt = salt
        self.publicKey = public_key
        self.signatureScheme = sign_scheme

    def __iter__(self):
        data = dict()
        data['address'] = self.address
        data['algorithm'] = self.algorithm
        data['enc-alg'] = self.enc_alg
        data['isDefault'] = self.isDefault
        data['key'] = self.key
        data['label'] = self.label
        data['lock'] = self.lock
        data['parameters'] = self.parameters
        data['salt'] = self.salt
        data['publicKey'] = self.publicKey
        data['signatureScheme'] = self.signatureScheme
        for key, value in data.items():
            yield (key, value)

    def set_label(self, label: str):
        self.label = label

    def set_address(self, address):
        self.address = address

    def set_public_key(self, public_key):
        self.publicKey = public_key

    def set_key(self, key):
        self.key = key

    def get_label(self):
        return self.label

    def get_address(self):
        return self.address

    def get_public_key(self):
        return self.publicKey

    def get_key(self):
        return self.key
