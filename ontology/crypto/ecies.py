#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ecdsa.curves import NIST256p
from ecdsa.ellipticcurve import Point
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
from ontology.crypto.aes_handler import AESHandler
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class ECIES:
    @staticmethod
    def generate_private_key():
        private_key = SigningKey.generate(NIST256p)
        return private_key.to_string()

    @staticmethod
    def ec_get_public_key_by_private_key(private_key: bytes):
        if not isinstance(private_key, bytes):
            raise SDKException(ErrorCode.other_error('the length of private key should be 32 bytes.'))
        if len(private_key) != 32:
            raise SDKException(ErrorCode.other_error('the length of private key should be 32 bytes.'))
        private_key = SigningKey.from_string(string=private_key, curve=NIST256p)
        public_key = private_key.get_verifying_key().to_string()
        return public_key

    @staticmethod
    def encrypt_with_cbc_mode(plain_text: bytes, public_key: bytes) -> (bytes, bytes, bytes):
        if not isinstance(public_key, bytes):
            raise SDKException(ErrorCode.other_error('the length of public key should be 64 bytes.'))
        if len(public_key) != 64:
            raise SDKException(ErrorCode.other_error('the length of public key should be 64 bytes.'))
        r = randint(1, NIST256p.order)
        g_tilde = r * NIST256p.generator
        h_tilde = r * VerifyingKey.from_string(string=public_key, curve=NIST256p).pubkey.point
        str_g_tilde_x = number_to_string(g_tilde.x(), NIST256p.order)
        str_g_tilde_y = number_to_string(g_tilde.y(), NIST256p.order)
        encode_g_tilde = b''.join([b'\x04', str_g_tilde_x, str_g_tilde_y])
        str_h_tilde_x = number_to_string(h_tilde.x(), NIST256p.order)
        seed = b''.join([encode_g_tilde, str_h_tilde_x])
        aes_key = pbkdf2(seed, 32)
        aes_iv, cipher_text = AESHandler.aes_cbc_encrypt(plain_text, aes_key)
        return aes_iv, encode_g_tilde, cipher_text

    @staticmethod
    def decrypt_with_cbc_mode(cipher_text: bytes, private_key: bytes, iv: bytes, encode_g_tilde: bytes):
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
        plain_text = AESHandler.aes_cbc_decrypt(cipher_text, iv, aes_key)
        return plain_text

    @staticmethod
    def encrypt_with_gcm_mode(plain_text: bytes, hdr: bytes, public_key: bytes):
        if not isinstance(public_key, bytes):
            raise SDKException(ErrorCode.other_error('the length of public key should be 64 bytes.'))
        if len(public_key) != 64:
            raise SDKException(ErrorCode.other_error('the length of public key should be 64 bytes.'))
        r = randint(1, NIST256p.order)
        g_tilde = r * NIST256p.generator
        h_tilde = r * VerifyingKey.from_string(string=public_key, curve=NIST256p).pubkey.point
        str_g_tilde_x = number_to_string(g_tilde.x(), NIST256p.order)
        str_g_tilde_y = number_to_string(g_tilde.y(), NIST256p.order)
        encode_g_tilde = b''.join([b'\x04', str_g_tilde_x, str_g_tilde_y])
        str_h_tilde_x = number_to_string(h_tilde.x(), NIST256p.order)
        seed = b''.join([encode_g_tilde, str_h_tilde_x])
        aes_key = pbkdf2(seed, 32)
        nonce, mac_tag, cipher_text = AESHandler.aes_gcm_encrypt(plain_text, hdr, aes_key)
        return nonce, mac_tag, encode_g_tilde, cipher_text

    @staticmethod
    def decrypt_with_gcm_mode(nonce: bytes, mac_tag: bytes, cipher_text: bytes, private_key: bytes, hdr: bytes,
                              encode_g_tilde: bytes):
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
        plain_text = AESHandler.aes_gcm_decrypt(cipher_text, hdr, nonce, mac_tag, aes_key)
        return plain_text
