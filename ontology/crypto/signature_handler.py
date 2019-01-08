# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils

import ecdsa
from hashlib import sha256
from ecdsa import ellipticcurve, VerifyingKey
from ecdsa.numbertheory import square_root_mod_prime
from ecdsa.util import string_to_number, number_to_string

from ontology.crypto.key_type import KeyType
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class SignatureHandler(object):
    def __init__(self, key_type: KeyType, scheme: SignatureScheme):
        self.__type = key_type
        self.__scheme = scheme

    def generate_signature(self, pri_key: str, msg: bytes) -> str:
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
        else:
            raise SDKException(ErrorCode.other_error('Invalid signature scheme.'))
        sign = SignatureHandler.dsa_der_to_plain(signature)
        return sign

    @staticmethod
    def verify_signature(public_key: bytes, msg: bytes, signature: bytes):
        if public_key.startswith(b'\x02') or public_key.startswith(b'\x03'):
            public_key = SignatureHandler.uncompress_public_key(public_key)
        elif public_key.startswith(b'\x04'):
            pass
        else:
            raise ValueError('Invalid public key format')
        vk = ecdsa.VerifyingKey.from_string(public_key, curve=ecdsa.NIST256p)
        try:
            return vk.verify(signature[1:], msg, hashfunc=sha256)
        except Exception:
            return False

    @staticmethod
    def dsa_der_to_plain(signature):
        r, s = utils.decode_dss_signature(signature)
        r = hex(r)[2:]
        if len(r) < 64:
            r = "".join(['0' for i in range(64 - len(r))]) + r
        s = hex(s)[2:]
        if len(s) < 64:
            s = "".join(['0' for i in range(64 - len(s))]) + s
        return r + s

    @staticmethod
    def uncompress_public_key(public_key: bytes)->bytes:
        """
        Uncompress the compressed public key.
        :param public_key: compressed public key
        :return: uncompressed public key
        """
        is_even = public_key.startswith(b'\x02')
        x = string_to_number(public_key[1:])
        curve = ecdsa.NIST256p.curve
        order = ecdsa.NIST256p.order
        p = curve.p()
        alpha = (pow(x, 3, p) + (curve.a() * x) + curve.b()) % p
        beta = square_root_mod_prime(alpha, p)
        if is_even == bool(beta & 1):
            y = p - beta
        else:
            y = beta
        point = ellipticcurve.Point(curve, x, y, order)
        return b''.join([number_to_string(point.x(), order), number_to_string(point.y(), order)])
