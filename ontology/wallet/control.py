#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Control(object):
    def __init__(self, id="", address='', enc_alg="aes-256-gcm", key="", algorithm='ECDSA', salt="", param=None,
                 hash_value="sha256", public_key=""):
        if param is None:
            param = {"curve": "P-256"}
        self.address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.hash = hash_value
        self.id = id
        self.key = key
        self.parameters = param
        self.salt = salt
        self.publicKey = public_key
