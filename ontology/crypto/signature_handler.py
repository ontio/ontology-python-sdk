"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

from ecdsa import (
    util,
    keys,
    NIST256p,
    VerifyingKey,
    ellipticcurve,
    numbertheory
)

from hashlib import sha256

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme


class SignatureHandler(object):
    def __init__(self, scheme: SignatureScheme):
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
    def verify_signature(public_key: bytes or str, msg: bytes, signature: bytes):
        if isinstance(public_key, str):
            public_key = bytes.fromhex(public_key)
        if public_key.startswith(b'\x02') or public_key.startswith(b'\x03'):
            public_key = SignatureHandler.uncompress_public_key(public_key)
        elif public_key.startswith(b'\x04'):
            pass
        else:
            raise SDKException(ErrorCode.unknown_asymmetric_key_type)
        if len(signature) == 65:
            signature = signature[1:]
        vk = VerifyingKey.from_string(public_key, curve=NIST256p)
        try:
            return vk.verify(signature, msg, hashfunc=sha256)
        except (AssertionError, keys.BadSignatureError, keys.BadDigestError):
            return False

    @staticmethod
    def dsa_der_to_plain(signature):
        r, s = utils.decode_dss_signature(signature)
        r = hex(r)[2:]
        if len(r) < 64:
            r = '0' * (64 - len(r)) + r
        s = hex(s)[2:]
        if len(s) < 64:
            s = '0' * (64 - len(s)) + s
        return r + s

    @staticmethod
    def uncompress_public_key(public_key: bytes) -> bytes:
        """
        Uncompress the compressed public key.
        :param public_key: compressed public key
        :return: uncompressed public key
        """
        is_even = public_key.startswith(b'\x02')
        x = util.string_to_number(public_key[1:])
        curve = NIST256p.curve
        order = NIST256p.order
        p = curve.p()
        alpha = (pow(x, 3, p) + (curve.a() * x) + curve.b()) % p
        beta = numbertheory.square_root_mod_prime(alpha, p)
        if is_even == bool(beta & 1):
            y = p - beta
        else:
            y = beta
        point = ellipticcurve.Point(curve, x, y, order)
        return b''.join([util.number_to_string(point.x(), order), util.number_to_string(point.y(), order)])
