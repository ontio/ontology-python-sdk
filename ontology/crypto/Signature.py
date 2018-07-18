#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import binascii

from ecdsa import SECP256k1, SigningKey

from crypto.Curve import Curve
from crypto.SignatureScheme import SignatureScheme


class Signature(object):
    def __init__(self, signature_scheme, signature_value):
        self.__scheme = signature_scheme
        self.__value = signature_value

    @staticmethod
    def ec_get_pubkey_by_prikey(privateKey, curveName):
        if curveName == Curve.P256:
            private_key = SigningKey.from_string(string=binascii.a2b_hex(privateKey), curve=SECP256k1)
            public_key = private_key.get_verifying_key().to_string()
        else:
            raise TypeError
        return public_key

    def to_byte(self):
        if self.__scheme == SignatureScheme.SM3withSM2:
            raise TypeError
        bs = bytearray()
        bs.append(self.__scheme.value)
        bs.append(self.__value)
        return bs
