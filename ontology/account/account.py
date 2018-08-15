#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import base58
from binascii import b2a_hex, a2b_hex

from ontology.crypto.curve import Curve
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.crypto.signature_handler import SignatureHandler
from ontology.crypto.signature import Signature
from ontology.common.address import Address
from ontology.crypto.key_type import KeyType
from ontology.crypto.aes_handler import AESHandler
from ontology.crypto.scrypt import Scrypt
from ontology.crypto.digest import Digest


class Account(object):
    def __init__(self, private_key: str, scheme=SignatureScheme.SHA256withECDSA):
        self.__signature_scheme = scheme
        if scheme == SignatureScheme.SHA256withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_384withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_384withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA512withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_224withECDSA:
            self.__keyType = KeyType.ECDSA
        else:
            raise TypeError
        self.__private_key = a2b_hex(private_key.encode())  # 32 bytes
        self.__curve_name = Curve.P256
        self.__publicKey = Signature.ec_get_pubkey_by_prikey(self.__private_key, self.__curve_name)  # 33 bytes
        self.__address = Address.address_from_bytes_pubkey(self.__publicKey)  # address is a class type

    def generate_signature(self, msg: bytes, signature_scheme: SignatureScheme):
        if signature_scheme == SignatureScheme.SHA256withECDSA:
            handler = SignatureHandler(self.__keyType, signature_scheme)
            signature_value = handler.generateSignature(b2a_hex(self.__private_key), msg)
            byte_signature = Signature(signature_scheme, signature_value).to_byte()
        else:
            raise TypeError
        return byte_signature

    def get_address(self):
        return self.__address  # __address is a class not a string or bytes

    def get_address_base58(self):
        return self.__address.to_base58()

    def get_address_hex(self):
        return self.__address.to_reverse_hex_str()

    def get_public_key(self):
        return self.__publicKey

    def get_signature_scheme(self):
        return self.__signature_scheme

    def export_gcm_encrypted_private_key(self, password: str, salt: str, n: int):
        r = 8
        p = 8
        dk_len = 64
        scrypt = Scrypt(n, r, p, dk_len)
        derivedkey = scrypt.generate_kd(password, salt)
        iv = derivedkey[0:12]
        derivedhalf2 = derivedkey[32:64]
        mac_tag, cipher_text = AESHandler.aes_gcm_encrypt_with_iv(self.__private_key,
                                                                  self.__address.to_base58().encode(),
                                                                  derivedhalf2,
                                                                  iv)
        encrypted_key = b2a_hex(cipher_text) + b2a_hex(mac_tag)
        encrypted_key_str = base64.b64encode(a2b_hex(encrypted_key))
        return encrypted_key_str.decode()

    @staticmethod
    def get_gcm_decoded_private_key(encrypted_key_str: str, password: str, address: str, salt: str, n: int,
                                    scheme: SignatureScheme) -> str:
        r = 8
        p = 8
        dk_len = 64
        scrypt = Scrypt(n, r, p, dk_len)
        derivedkey = scrypt.generate_kd(password, salt)
        iv = derivedkey[0:12]
        derivedhalf2 = derivedkey[32:64]
        encrypted_key = base64.b64decode(encrypted_key_str).hex()
        mac_tag = a2b_hex(encrypted_key[64:96])
        cipher_text = a2b_hex(encrypted_key[0:64])
        pri_key = AESHandler.aes_gcm_decrypt_with_iv(cipher_text, address.encode(), mac_tag, derivedhalf2, iv)
        pri_key = b2a_hex(pri_key).decode('ascii')
        acct = Account(pri_key, scheme)
        if acct.get_address().to_base58() != address:
            raise RuntimeError
        return pri_key

    def serialize_private_key(self):
        return self.__private_key

    def serialize_public_key(self):
        return self.__publicKey

    def export_wif(self):
        data = b'\x80'
        data = data + self.serialize_private_key()
        data += b'\01'
        checksum = Digest.hash256(data[0:34])
        data += checksum[0:4]
        return base58.b58encode(data)

    def get_privatekey_from_wif(self, wif: str):
        if wif is None or wif is "":
            raise Exception("none wif")
        data = base58.b58decode(wif)
        if len(data) != 38 or data[0] != 0x80 or data[33] != 0x01:
            raise Exception("wif wrong")
        checksum = Digest.hash256(data[0:34])
        for i in range(4):
            if data[len(data) - 4 + i] != checksum[i]:
                raise Exception("wif wrong")
        return data[1:33]
