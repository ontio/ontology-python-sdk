#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.crypto.ecies import ECIES


class EciesTest(unittest.TestCase):
    def test_ec_get_public_key_by_private_key(self):
        private_key_bytes = ECIES.generate_private_key()
        self.assertEqual(32, len(private_key_bytes))
        public_key_bytes = ECIES.ec_get_public_key_by_private_key(private_key_bytes)
        self.assertEqual(64, len(public_key_bytes))

    def test_encrypt_with_cbc_mode(self):
        private_key_bytes = ECIES.generate_private_key()
        self.assertEqual(32, len(private_key_bytes))
        public_key_bytes = ECIES.ec_get_public_key_by_private_key(private_key_bytes)
        self.assertEqual(64, len(public_key_bytes))
        msg = b'Attack!'
        aes_iv, encode_g_tilde, cipher_text = ECIES.encrypt_with_cbc_mode(msg, public_key_bytes)
        decrypt_msg = ECIES.decrypt_with_cbc_mode(cipher_text, private_key_bytes, aes_iv, encode_g_tilde)
        self.assertEqual(msg, decrypt_msg)

    def test_encrypt_with_gcm_mode(self):
        private_key_bytes = ECIES.generate_private_key()
        self.assertEqual(32, len(private_key_bytes))
        public_key_bytes = ECIES.ec_get_public_key_by_private_key(private_key_bytes)
        self.assertEqual(64, len(public_key_bytes))
        msg = b'Attack!'
        nonce, mac_tag, encode_g_tilde, cipher_text = ECIES.encrypt_with_gcm_mode(msg, b'', public_key_bytes)
        decrypt_msg = ECIES.decrypt_with_gcm_mode(nonce, mac_tag, cipher_text, private_key_bytes, b'', encode_g_tilde)
        self.assertEqual(msg, decrypt_msg)


if __name__ == '__main__':
    unittest.main()
