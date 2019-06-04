"""
Copyright (C) 2018-2019 The ontology Authors
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

import unittest

from Cryptodome import Random
from Cryptodome.Cipher import AES

from ontology.crypto.aes_handler import AESHandler


class TestAesHandler(unittest.TestCase):
    def test_aes_cbc(self):
        key = b'Sixteen byte key'
        plain_text = b'Attack at dawn'
        iv, cipher_text = AESHandler.aes_cbc_encrypt(plain_text, key)
        decrypt_out = AESHandler.aes_cbc_decrypt(cipher_text, iv, key)
        self.assertEqual(plain_text, decrypt_out)

    def test_aes_gcm(self):
        key = b'Sixteen byte key'
        plain_text = b'Attack at dawn'
        hdr = b'To your eyes only'
        nonce, mac, cipher_text = AESHandler.aes_gcm_encrypt(plain_text, hdr, key)
        decrypt_out = AESHandler.aes_gcm_decrypt(cipher_text, hdr, nonce, mac, key)
        self.assertEqual(plain_text, decrypt_out)

    def test_aes_gcm_with_iv(self):
        key = b'Sixteen byte key'
        plain_text = b'Attack at dawn'
        hdr = b'To your eyes only'
        iv = Random.new().read(AES.block_size)
        mac, cipher_text = AESHandler.aes_gcm_encrypt_with_iv(plain_text, hdr, key, iv)
        decrypt_out = AESHandler.aes_gcm_decrypt_with_iv(cipher_text, hdr, mac, key, iv)
        self.assertEqual(plain_text, decrypt_out)

    def test_aes_gcm_with_iv_wrong_iv(self):
        key = b'Sixteen byte key'
        plain_text = b'Attack at dawn'
        hdr = b'To your eyes only'
        iv = Random.new().read(AES.block_size)
        mac, cipher_text = AESHandler.aes_gcm_encrypt_with_iv(plain_text, hdr, key, iv)
        iv = Random.new().read(AES.block_size)
        decrypt_out = AESHandler.aes_gcm_decrypt_with_iv(cipher_text, hdr, mac, key, iv)
        self.assertNotEqual(plain_text, decrypt_out)

    def test_aes_ctr(self):
        key = b'Sixteen byte key'
        plain_text = b'Attack at dawn'
        nonce, cipher_text = AESHandler.aes_ctr_encrypt(plain_text, key)
        decrypt_out = AESHandler.aes_ctr_decrypt(cipher_text, nonce, key)
        self.assertEqual(plain_text, decrypt_out)


if __name__ == '__main__':
    unittest.main()
