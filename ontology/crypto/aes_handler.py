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

from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


class AESHandler(object):
    @staticmethod
    def generate_iv() -> bytes:
        return Random.new().read(AES.block_size)

    @staticmethod
    def generate_key():
        key = Random.get_random_bytes(32)
        return key

    @staticmethod
    def aes_gcm_encrypt_with_iv(plain_text: bytes, hdr: bytes, key: bytes, iv: bytes):
        cipher = AES.new(key=key, mode=AES.MODE_GCM, nonce=iv)
        cipher.update(hdr)
        cipher_text, mac_tag = cipher.encrypt_and_digest(plain_text)
        return mac_tag, cipher_text

    @staticmethod
    def aes_gcm_decrypt_with_iv(cipher_text: bytes, hdr: bytes, mac_tag: bytes, key: bytes, iv: bytes) -> bytes:
        cipher = AES.new(key=key, mode=AES.MODE_GCM, nonce=iv)
        cipher.update(hdr)
        try:
            plain_text = cipher.decrypt_and_verify(cipher_text, mac_tag)
        except ValueError:
            plain_text = b""
        except KeyError:
            plain_text = b""
        return plain_text

    @staticmethod
    def aes_gcm_encrypt(plain_text: bytes, hdr: bytes, key: bytes):
        cipher = AES.new(key=key, mode=AES.MODE_GCM)
        cipher.update(hdr)
        cipher_text, mac_tag = cipher.encrypt_and_digest(plain_text)
        nonce = cipher.nonce
        return nonce, mac_tag, cipher_text

    @staticmethod
    def aes_gcm_decrypt(cipher_text: bytes, hdr: bytes, nonce: bytes, mac_tag: bytes, key: bytes):
        cipher = AES.new(key=key, mode=AES.MODE_GCM, nonce=nonce)
        cipher.update(hdr)
        try:
            plain_text = cipher.decrypt_and_verify(cipher_text, mac_tag)
        except ValueError:
            plain_text = b""
        except KeyError:
            plain_text = b""
        return plain_text

    @staticmethod
    def aes_ctr_encrypt(plain_text: bytes, key: bytes):
        cipher = AES.new(key=key, mode=AES.MODE_CTR)
        cipher_text = cipher.encrypt(plain_text)
        nonce = cipher.nonce
        return nonce, cipher_text

    @staticmethod
    def aes_ctr_decrypt(cipher_text: bytes, nonce: bytes, key: bytes):
        cipher = AES.new(key=key, mode=AES.MODE_CTR, nonce=nonce)
        plain_text = cipher.decrypt(cipher_text)
        return plain_text

    @staticmethod
    def aes_cbc_encrypt(plain_text: bytes, key: bytes, iv: bytes = b''):
        if len(iv) == 0:
            iv = AESHandler.generate_iv()
        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        return cipher.IV, cipher.encrypt(pad(plain_text, AES.block_size))

    @staticmethod
    def aes_cbc_decrypt(cipher_text: bytes, iv: bytes, key: bytes):
        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        return unpad(cipher.decrypt(cipher_text), AES.block_size, style='pkcs7')
