#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from ontology.crypto.SignatureScheme import SignatureScheme


class SignatureHandler(object):
    def __init__(self, key_type, scheme):
        self.__type = key_type
        self.__scheme = scheme

    def generateSignature(self, pri_key, msg):
        if self.__scheme == SignatureScheme.SHA224withECDSA:
            private_key = ec.derive_private_key(int(pri_key, 16), ec.SECP224R1(), default_backend())
            signature = private_key.sign(
                msg,
                ec.ECDSA(hashes.SHA224())
            )
        elif self.__scheme == SignatureScheme.SHA256withECDSA:
            private_key = ec.derive_private_key(int(pri_key, 16), ec.SECP256R1(), default_backend())
            signature = private_key.sign(
                msg,
                ec.ECDSA(hashes.SHA256())
            )
        elif self.__scheme == SignatureScheme.SHA384withECDSA:
            private_key = ec.derive_private_key(int(pri_key, 16), ec.SECP384R1(), default_backend())
            signature = private_key.sign(
                msg,
                ec.ECDSA(hashes.SHA384())
            )
        sign = SignatureHandler.dsa_der_to_plain(signature)
        return sign

    @staticmethod
    def dsa_der_to_plain(signature):
        r, s = utils.decode_dss_signature(signature)
        r = hex(r)[2:]
        s = hex(s)[2:]
        return r + s
