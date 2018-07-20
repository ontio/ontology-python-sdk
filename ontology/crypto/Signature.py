#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
from ecdsa import SECP256k1, ecdsa, util, NIST256p, SigningKey
from ontology.crypto.Curve import Curve
from ontology.crypto.SignatureScheme import SignatureScheme


class Signature(object):
    def __init__(self, signature_scheme, signature_value):
        self.__scheme = signature_scheme
        self.__value = signature_value

    @staticmethod
    def ec_get_pubkey_by_prikey(privateKey, curveName):
        if curveName == Curve.P256:
            private_key = SigningKey.from_string(string=binascii.a2b_hex(privateKey), curve=NIST256p)
            # public_key = private_key.get_verifying_key().to_string()
            verifying_key = private_key.get_verifying_key()
            order = verifying_key.pubkey.order
            x_str = util.number_to_string(verifying_key.pubkey.point.x(), order)
            y_str = util.number_to_string(verifying_key.pubkey.point.y(), order)
            point_str = util.b("\x04") + x_str + y_str
            if verifying_key.pubkey.point.y() % 2 == 0:
                point_str = util.b("\x02") + x_str
            else:
                point_str = util.b("\x03") + x_str
        else:
            raise TypeError
        return point_str

    def to_byte(self):
        if self.__scheme == SignatureScheme.SM3withSM2:
            raise TypeError
        bs = bytearray()
        bs.append(self.__scheme.value)
        bs += bytearray.fromhex(self.__value)
        return bs

