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

    def __iter__(self):
        data = dict()
        data['address'] = self.address
        data['algorithm'] = self.algorithm
        data['enc-alg'] = self.enc_alg
        data['hash'] = self.hash
        data['id'] = self.id
        data['key'] = self.key
        data['parameters'] = self.parameters
        data['salt'] = self.salt
        data['publicKey'] = self.publicKey
        for key, value in data.items():
            yield (key, value)

    @staticmethod
    def dict2obj(control_data: dict):
        obj = Control(id=control_data['id'], address=control_data['address'], enc_alg=control_data['enc-alg'],
                      key=control_data['key'], algorithm=control_data['algorithm'], salt=control_data['salt'],
                      param=control_data['parameters'], hash_value=control_data['hash'],
                      public_key=control_data['publicKey'])
        return obj
