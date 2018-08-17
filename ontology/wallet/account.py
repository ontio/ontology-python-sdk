#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AccountData(object):
    def __init__(self, address: str = '', enc_alg: str = "aes-256-gcm", key: str = "", algorithm="ECDSA", salt="",
                 param: dict = None, label: str = "", public_key: str = "", sign_scheme: str = "SHA256withECDSA",
                 isDefault: bool = True, lock: bool = False, hash_value: str = "sha256"):
        if param is None:
            param = {"curve": "P-256"}
        self.address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.hash = hash_value
        self.isDefault = isDefault
        self.key = key
        self.label = label
        self.lock = lock
        self.parameters = param
        self.salt = salt
        self.publicKey = public_key
        self.signatureScheme = sign_scheme

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
