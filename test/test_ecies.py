#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import unittest

from ontology.crypto.ecies import ECIES
from ontology.exception.exception import SDKException


class EciesTest(unittest.TestCase):
    def test_get_public_key_by_private_key(self):
        for _ in range(10):
            private_key_bytes = ECIES.generate_private_key()
            self.assertEqual(32, len(private_key_bytes))
            public_key_bytes = ECIES.get_public_key_by_bytes_private_key(private_key_bytes)
            self.assertEqual(33, len(public_key_bytes))
            self.assertRaises(SDKException, ECIES.get_public_key_by_bytes_private_key, '')
            self.assertRaises(SDKException, ECIES.get_public_key_by_bytes_private_key, b'')

    def test_compatibility(self):
        hex_private_key = '9a31d585431ce0aa0aab1f0a432142e98a92afccb7bcbcaff53f758df82acdb3'
        hex_public_key = ECIES.get_public_key_by_hex_private_key(hex_private_key)
        self.assertEqual('021401156f187ec23ce631a489c3fa17f292171009c6c3162ef642406d3d09c74d', hex_public_key)
        bytes_private_key = binascii.a2b_hex(hex_private_key)
        public_key_bytes = ECIES.get_public_key_by_bytes_private_key(bytes_private_key)
        msg = b'Attack!'
        aes_iv, encode_g_tilde, cipher_text = ECIES.encrypt_with_cbc_mode(msg, public_key_bytes)
        decrypt_msg = ECIES.decrypt_with_cbc_mode(cipher_text, bytes_private_key, aes_iv, encode_g_tilde)
        self.assertEqual(msg, decrypt_msg)
        nonce, mac_tag, encode_g_tilde, cipher_text = ECIES.encrypt_with_gcm_mode(msg, b'', public_key_bytes)
        self.assertRaises(SDKException, ECIES.encrypt_with_gcm_mode, msg, b'', '')
        self.assertRaises(SDKException, ECIES.encrypt_with_gcm_mode, msg, b'', b'')
        decrypt_msg = ECIES.decrypt_with_gcm_mode(nonce, mac_tag, cipher_text, bytes_private_key, b'', encode_g_tilde)
        self.assertEqual(msg, decrypt_msg)

    def test_encrypt_with_cbc_mode(self):
        for _ in range(10):
            private_key_bytes = ECIES.generate_private_key()
            self.assertEqual(32, len(private_key_bytes))
            public_key_bytes = ECIES.get_public_key_by_bytes_private_key(private_key_bytes)
            self.assertEqual(33, len(public_key_bytes))
            msg = b'Attack!'
            aes_iv, encode_g_tilde, cipher_text = ECIES.encrypt_with_cbc_mode(msg, public_key_bytes)
            self.assertRaises(SDKException, ECIES.encrypt_with_cbc_mode, msg, '')
            self.assertRaises(SDKException, ECIES.encrypt_with_cbc_mode, msg, b'')
            decrypt_msg = ECIES.decrypt_with_cbc_mode(cipher_text, private_key_bytes, aes_iv, encode_g_tilde)
            self.assertRaises(SDKException, ECIES.decrypt_with_cbc_mode, cipher_text, b'', aes_iv, encode_g_tilde)
            self.assertRaises(SDKException, ECIES.decrypt_with_cbc_mode, cipher_text, '', aes_iv, encode_g_tilde)
            self.assertEqual(msg, decrypt_msg)
            cipher_text = b'\x00' * len(cipher_text)
            self.assertRaises(SDKException, ECIES.decrypt_with_cbc_mode, cipher_text, private_key_bytes, aes_iv,
                              encode_g_tilde)

    def test_encrypt_with_gcm_mode(self):
        for _ in range(10):
            private_key_bytes = ECIES.generate_private_key()
            self.assertEqual(32, len(private_key_bytes))
            public_key_bytes = ECIES.get_public_key_by_bytes_private_key(private_key_bytes)
            self.assertEqual(33, len(public_key_bytes))
            msg = b'Attack!'
            nonce, mac_tag, encode_g_tilde, cipher_text = ECIES.encrypt_with_gcm_mode(msg, b'', public_key_bytes)
            self.assertRaises(SDKException, ECIES.encrypt_with_gcm_mode, msg, b'', '')
            self.assertRaises(SDKException, ECIES.encrypt_with_gcm_mode, msg, b'', b'')
            decrypt_msg = ECIES.decrypt_with_gcm_mode(nonce, mac_tag, cipher_text, private_key_bytes, b'',
                                                      encode_g_tilde)
            self.assertEqual(msg, decrypt_msg)
            cipher_text = b'\x00' * len(cipher_text)
            decrypt_msg = ECIES.decrypt_with_gcm_mode(nonce, mac_tag, cipher_text, private_key_bytes, b'',
                                                      encode_g_tilde)
            self.assertRaises(SDKException, ECIES.decrypt_with_gcm_mode, nonce, mac_tag, cipher_text, '', b'',
                              encode_g_tilde)
            self.assertRaises(SDKException, ECIES.decrypt_with_gcm_mode, nonce, mac_tag, cipher_text, b'', b'',
                              encode_g_tilde)
            self.assertEqual(b'', decrypt_msg)


if __name__ == '__main__':
    unittest.main()
