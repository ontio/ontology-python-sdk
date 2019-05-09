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

import base64
import base58

from ontology.crypto.curve import Curve
from ontology.crypto.digest import Digest
from ontology.crypto.scrypt import Scrypt
from ontology.common.define import DID_ONT
from ontology.common.address import Address
from ontology.crypto.key_type import KeyType
from ontology.crypto.signature import Signature
from ontology.crypto.aes_handler import AESHandler
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.crypto.signature_handler import SignatureHandler


class Account(object):
    def __init__(self, private_key: str or bytes, scheme=SignatureScheme.SHA256withECDSA):
        self.__signature_scheme = scheme
        if scheme == SignatureScheme.SHA256withECDSA:
            self.__key_type = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_384withECDSA:
            self.__key_type = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_384withECDSA:
            self.__key_type = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA512withECDSA:
            self.__key_type = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_224withECDSA:
            self.__key_type = KeyType.ECDSA
        else:
            raise TypeError
        if isinstance(private_key, bytes) and len(private_key) == 32:
            self.__private_key = private_key
        elif isinstance(private_key, str) and len(private_key) == 64:
            self.__private_key = bytes.fromhex(private_key)
        else:
            raise SDKException(ErrorCode.invalid_private_key)
        self.__curve_name = Curve.P256
        self.__public_key = Signature.ec_get_public_key_by_private_key(self.__private_key, self.__curve_name)
        self.__address = Address.from_public_key(self.__public_key)

    def generate_signature(self, msg: bytes):
        handler = SignatureHandler(self.__signature_scheme)
        signature_value = handler.generate_signature(bytes.hex(self.__private_key), msg)
        bytes_signature = Signature(self.__signature_scheme, signature_value).to_bytes()
        result = handler.verify_signature(self.__public_key, msg, bytes_signature)
        if not result:
            raise SDKException(ErrorCode.invalid_signature_data)
        return bytes_signature

    def verify_signature(self, msg: bytes, signature: bytes):
        if msg is None or signature is None:
            raise Exception(ErrorCode.param_err("param should not be None"))
        handler = SignatureHandler(self.__signature_scheme)
        return handler.verify_signature(self.get_public_key_bytes(), msg, signature)

    def get_ont_id(self):
        return DID_ONT + self.get_address_base58()

    def get_address(self):
        """

        :return:
        """
        return self.__address  # __address is a class not a string or bytes

    def get_address_bytes(self):
        return self.__address.to_bytes()

    def get_address_base58(self) -> str:
        """
        This interface is used to get the base58 encode account address.

        :return:
        """
        return self.__address.b58encode()

    def get_address_hex(self, little_endian: bool = True):
        """
        This interface is used to get the little-endian hexadecimal account address.

        :return: little-endian hexadecimal account address.
        """
        return self.__address.hex(little_endian)

    def get_signature_scheme(self) -> SignatureScheme:
        """
        This interface allow to get he signature scheme used in account

        :return: he signature scheme used in account.
        """
        return self.__signature_scheme

    def export_gcm_encrypted_private_key(self, password: str, salt: str, n: int = 16384) -> str:
        """
        This interface is used to export an AES algorithm encrypted private key with the mode of GCM.

        :param password: the secret pass phrase to generate the keys from.
        :param salt: A string to use for better protection from dictionary attacks.
                      This value does not need to be kept secret, but it should be randomly chosen for each derivation.
                      It is recommended to be at least 8 bytes long.
        :param n: CPU/memory cost parameter. It must be a power of 2 and less than 2**32
        :return: an gcm encrypted private key in the form of string.
        """
        r = 8
        p = 8
        dk_len = 64
        scrypt = Scrypt(n, r, p, dk_len)
        derived_key = scrypt.generate_kd(password, salt)
        iv = derived_key[0:12]
        key = derived_key[32:64]
        hdr = self.__address.b58encode().encode()
        mac_tag, cipher_text = AESHandler.aes_gcm_encrypt_with_iv(self.__private_key, hdr, key, iv)
        encrypted_key = bytes.hex(cipher_text) + bytes.hex(mac_tag)
        encrypted_key_str = base64.b64encode(bytes.fromhex(encrypted_key))
        return encrypted_key_str.decode('utf-8')

    @staticmethod
    def get_gcm_decoded_private_key(encrypted_key_str: str, password: str, b58_address: str, salt: str, n: int,
                                    scheme: SignatureScheme) -> str:
        """
        This interface is used to decrypt an private key which has been encrypted.

        :param encrypted_key_str: an gcm encrypted private key in the form of string.
        :param password: the secret pass phrase to generate the keys from.
        :param b58_address: a base58 encode address which should be correspond with the private key.
        :param salt: a string to use for better protection from dictionary attacks.
        :param n: CPU/memory cost parameter.
        :param scheme: the signature scheme.
        :return: a private key in the form of string.
        """
        r = 8
        p = 8
        dk_len = 64
        scrypt = Scrypt(n, r, p, dk_len)
        derived_key = scrypt.generate_kd(password, salt)
        iv = derived_key[0:12]
        key = derived_key[32:64]
        encrypted_key = base64.b64decode(encrypted_key_str).hex()
        mac_tag = bytes.fromhex(encrypted_key[64:96])
        cipher_text = bytes.fromhex(encrypted_key[0:64])
        private_key = AESHandler.aes_gcm_decrypt_with_iv(cipher_text, b58_address.encode(), mac_tag, key, iv)
        if len(private_key) == 0:
            raise SDKException(ErrorCode.decrypt_encrypted_private_key_error)
        acct = Account(private_key, scheme)
        if acct.get_address().b58encode() != b58_address:
            raise SDKException(ErrorCode.other_error('Address error.'))
        return private_key.hex()

    def get_public_key_serialize(self):
        stream = StreamManager.get_stream()
        writer = BinaryWriter(stream)
        if self.__key_type == KeyType.ECDSA:
            writer.write_var_bytes(self.__public_key)
        else:
            raise SDKException(ErrorCode.unknown_asymmetric_key_type)
        stream.flush()
        bytes_stream = stream.hexlify()
        StreamManager.release_stream(stream)
        return bytes_stream

    def get_private_key_bytes(self) -> bytes:
        """
        This interface is used to get the private key in the form of bytes.

        :return: the private key in the form of bytes.
        """
        return self.__private_key

    def get_private_key_hex(self) -> str:
        """
        This interface is used to get the account's hexadecimal public key in the form of string.

        :return: the hexadecimal public key in the form of string.
        """
        return bytes.hex(self.__private_key)

    def get_public_key_bytes(self) -> bytes:
        """
        This interface is used to get the public key in the form of bytes.

        :return: the public key in the form of bytes.
        """
        return self.__public_key

    def get_public_key_bytearray(self) -> bytearray:
        """
        This interface is used to get the public key in the form of bytearray.

        :return: the public key in the form of bytearray.
        """
        return bytearray(self.__public_key)

    def get_public_key_hex(self) -> str:
        """
        This interface is used to get the account's hexadecimal public key in the form of string.

        :return: the hexadecimal public key in the form of string.
        """
        return bytes.hex(self.__public_key)

    def export_wif(self) -> str:
        """
        This interface is used to get export ECDSA private key in the form of WIF which
        is a way to encoding an ECDSA private key and make it easier to copy.

        :return: a WIF encode private key.
        """
        data = b''.join([b'\x80', self.__private_key, b'\01'])
        checksum = Digest.hash256(data[0:34])
        wif = base58.b58encode(b''.join([data, checksum[0:4]]))
        return wif.decode('ascii')

    @staticmethod
    def get_private_key_from_wif(wif: str) -> bytes:
        """
        This interface is used to decode a WIF encode ECDSA private key.

        :param wif: a WIF encode private key.
        :return: a ECDSA private key in the form of bytes.
        """
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
