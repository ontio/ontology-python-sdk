#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ecdsa import util, NIST256p, SigningKey

from ontology.crypto.curve import Curve
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme


class Signature(object):
    def __init__(self, signature_scheme, signature_value):
        self.__scheme = signature_scheme
        self.__value = signature_value

    @staticmethod
    def ec_get_pubkey_by_prikey(privateKey: bytes, curve_name):
        if curve_name == Curve.P256:
            private_key = SigningKey.from_string(string=(privateKey), curve=NIST256p)
            # public_key = private_key.get_verifying_key().to_string()
            verifying_key = private_key.get_verifying_key()
            order = verifying_key.pubkey.order
            x_str = util.number_to_string(verifying_key.pubkey.point.x(), order)
            # TODO: add verify
            # y_str = util.number_to_string(verifying_key.pubkey.point.y(), order)
            # point_str = util.b("\x04") + x_str + y_str
            if verifying_key.pubkey.point.y() % 2 == 0:
                point_str = util.b("\x02") + x_str
            else:
                point_str = util.b("\x03") + x_str
        elif curve_name == Curve.P224:
            raise SDKException(ErrorCode.unsupported_key_type)
        elif curve_name == Curve.P384:
            raise SDKException(ErrorCode.unsupported_key_type)
        elif curve_name == Curve.P521:
            raise SDKException(ErrorCode.unsupported_key_type)
        else:
            raise SDKException(ErrorCode.unknown_key_type)
        return point_str

    def to_byte(self):
        if self.__scheme == SignatureScheme.SM3withSM2:
            raise TypeError
        bs = bytearray()
        bs.append(self.__scheme.value)
        bs += bytearray.fromhex(self.__value)
        return bs
