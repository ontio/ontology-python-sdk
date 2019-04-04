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

from ecdsa.curves import NIST256p
from ecdsa.ellipticcurve import Point
from ecdsa.numbertheory import square_root_mod_prime

from Cryptodome.Random.random import randint

from ecdsa.util import (
    string_to_number,
    number_to_string
)

from ecdsa.keys import (
    SigningKey,
    VerifyingKey,
)

from ontology.crypto.kdf import pbkdf2
from ontology.utils.arguments import type_assert
from ontology.crypto.aes_handler import AESHandler
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class ECIES:
    @staticmethod
    def generate_private_key() -> bytes:
        private_key = SigningKey.generate(NIST256p)
        return private_key.to_string()

    @staticmethod
    def get_public_key_by_hex_private_key(private_key: str):
        if not isinstance(private_key, str):
            raise SDKException(ErrorCode.other_error('The type of private key should be hexadecimal str.'))
        if len(private_key) != 64:
            raise SDKException(ErrorCode.other_error('The length of private key should be 64 bytes.'))
        private_key = bytes.fromhex(private_key)
        point_str = ECIES.get_public_key_by_bytes_private_key(private_key)
        return point_str.hex()

    @staticmethod
    @type_assert(bytes)
    def get_public_key_by_bytes_private_key(private_key: bytes):
        if not isinstance(private_key, bytes):
            raise SDKException(ErrorCode.other_error('The type of private key should be bytes.'))
        if len(private_key) != 32:
            raise SDKException(ErrorCode.other_error('The length of private key should be 32 bytes.'))
        private_key = SigningKey.from_string(string=private_key, curve=NIST256p)
        public_key = private_key.get_verifying_key()
        order = public_key.pubkey.order
        x_int = public_key.pubkey.point.x()
        y_int = public_key.pubkey.point.y()
        x_str = number_to_string(x_int, order)
        if y_int % 2 == 0:
            point_str = b''.join([b'\x02', x_str])
        else:
            point_str = b''.join([b'\x03', x_str])
        return point_str

    @staticmethod
    @type_assert(bytes)
    def __uncompress_public_key(public_key: bytes) -> bytes:
        """
        Uncompress the compressed public key.
        :param public_key: compressed public key
        :return: uncompressed public key
        """
        is_even = public_key.startswith(b'\x02')
        x = string_to_number(public_key[1:])

        curve = NIST256p.curve
        order = NIST256p.order
        p = curve.p()
        alpha = (pow(x, 3, p) + (curve.a() * x) + curve.b()) % p
        beta = square_root_mod_prime(alpha, p)
        if is_even == bool(beta & 1):
            y = p - beta
        else:
            y = beta
        point = Point(curve, x, y, order)
        return b''.join([number_to_string(point.x(), order), number_to_string(point.y(), order)])

    @staticmethod
    def generate_encrypt_aes_key(public_key: bytes):
        if not isinstance(public_key, bytes):
            raise SDKException(ErrorCode.other_error('the type of public key should be bytes.'))
        if len(public_key) != 33:
            raise SDKException(ErrorCode.other_error('the length of public key should be 33 bytes.'))
        if not (public_key.startswith(b'\x02') or public_key.startswith(b'\x03')):
            raise SDKException(ErrorCode.other_error('Invalid public key.'))
        public_key = ECIES.__uncompress_public_key(public_key)
        r = randint(1, NIST256p.order)
        g_tilde = r * NIST256p.generator
        h_tilde = r * VerifyingKey.from_string(string=public_key, curve=NIST256p).pubkey.point
        str_g_tilde_x = number_to_string(g_tilde.x(), NIST256p.order)
        str_g_tilde_y = number_to_string(g_tilde.y(), NIST256p.order)
        encode_g_tilde = b''.join([b'\x04', str_g_tilde_x, str_g_tilde_y])
        str_h_tilde_x = number_to_string(h_tilde.x(), NIST256p.order)
        seed = b''.join([encode_g_tilde, str_h_tilde_x])
        aes_key = pbkdf2(seed, 32)
        return aes_key, encode_g_tilde

    @staticmethod
    def generate_decrypt_aes_key(private_key: bytes, encode_g_tilde: bytes):
        if not isinstance(private_key, bytes):
            raise SDKException(ErrorCode.other_error('the length of private key should be 32 bytes.'))
        if len(private_key) != 32:
            raise SDKException(ErrorCode.other_error('the length of private key should be 32 bytes.'))
        str_g_tilde_x = encode_g_tilde[1:33]
        str_g_tilde_y = encode_g_tilde[33:65]
        g_tilde_x = string_to_number(str_g_tilde_x)
        g_tilde_y = string_to_number(str_g_tilde_y)
        g_tilde = Point(NIST256p.curve, g_tilde_x, g_tilde_y, NIST256p.order)
        h_tilde = g_tilde * SigningKey.from_string(string=private_key, curve=NIST256p).privkey.secret_multiplier
        seed = b''.join([encode_g_tilde, number_to_string(h_tilde.x(), NIST256p.order)])
        aes_key = pbkdf2(seed, 32)
        return aes_key

    @staticmethod
    @type_assert(bytes, bytes, bytes)
    def encrypt_with_cbc_mode(plain_text: bytes, public_key: bytes, iv: bytes = b'') -> (bytes, bytes, bytes):
        aes_key, encode_g_tilde = ECIES.generate_encrypt_aes_key(public_key)
        aes_iv, cipher_text = AESHandler.aes_cbc_encrypt(plain_text, aes_key, iv)
        return aes_iv, encode_g_tilde, cipher_text

    @staticmethod
    @type_assert(bytes, bytes, bytes, bytes)
    def decrypt_with_cbc_mode(cipher_text: bytes, private_key: bytes, iv: bytes, encode_g_tilde: bytes) -> bytes:
        aes_key = ECIES.generate_decrypt_aes_key(private_key, encode_g_tilde)
        try:
            plain_text = AESHandler.aes_cbc_decrypt(cipher_text, iv, aes_key)
        except ValueError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        return plain_text

    @staticmethod
    @type_assert(bytes, bytes, bytes)
    def encrypt_with_gcm_mode(plain_text: bytes, hdr: bytes, public_key: bytes):
        aes_key, encode_g_tilde = ECIES.generate_encrypt_aes_key(public_key)
        nonce, mac_tag, cipher_text = AESHandler.aes_gcm_encrypt(plain_text, hdr, aes_key)
        return nonce, mac_tag, encode_g_tilde, cipher_text

    @staticmethod
    @type_assert(bytes, bytes, bytes, bytes, bytes, bytes)
    def decrypt_with_gcm_mode(nonce: bytes, mac_tag: bytes, cipher_text: bytes, private_key: bytes, hdr: bytes,
                              encode_g_tilde: bytes):
        aes_key = ECIES.generate_decrypt_aes_key(private_key, encode_g_tilde)
        plain_text = AESHandler.aes_gcm_decrypt(cipher_text, hdr, nonce, mac_tag, aes_key)
        return plain_text
