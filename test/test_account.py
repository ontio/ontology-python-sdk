#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import unittest

from ontology.utils import util
from ontology.account.account import Account
from ontology.wallet.wallet import WalletData
from ontology.wallet.account import AccountData
from ontology.crypto.signature_scheme import SignatureScheme


class TestAccount(unittest.TestCase):
    def test_account_data_constructor(self):
        data = AccountData()
        self.assertEqual(data.algorithm, 'ECDSA')

    def test_wallet_data_clone(self):
        ont_id = 'test_ont_id'
        w = WalletData(default_id=ont_id)
        clone_wallet = w.clone()
        self.assertEqual(clone_wallet.__dict__['default_ont_id'], ont_id)

    def test_export_gcm_encrypted_private_key(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        account = Account(private_key, SignatureScheme.SHA256withECDSA)
        salt = util.get_random_str(16)
        enc_private_key = account.export_gcm_encrypted_private_key("1", salt, 16384)
        import_private_key = account.get_gcm_decoded_private_key(enc_private_key, "1", account.get_address_base58(),
                                                                 salt, 16384, SignatureScheme.SHA256withECDSA)
        self.assertEqual(import_private_key, private_key)

    def test_get_gcm_decoded_private_key(self):
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        salt = base64.b64decode("pwLIUKAf2bAbTseH/WYrfQ==".encode('ascii')).decode('latin-1')
        account = Account(private_key, SignatureScheme.SHA256withECDSA)
        enc_private_key = account.export_gcm_encrypted_private_key("1", salt, 16384)
        self.assertEqual(enc_private_key, 'Yl1e9ugbVADd8a2SbAQ56UfUvr3e9hD2eNXAM9xNjhnefB+YuNXDFvUrIRaYth+L')

    def test_generate_signature(self):
        raw_hex_data = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        account = Account(raw_hex_data, SignatureScheme.SHA256withECDSA)
        data = account.generate_signature(bytes("test".encode()), SignatureScheme.SHA256withECDSA)
        # TODO: add verify signature
        # print(data.hex())

    def test_serialize_private_key(self):
        hex_private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        account = Account(hex_private_key, SignatureScheme.SHA256withECDSA)
        hex_serialize_private_key = account.serialize_private_key().hex()
        self.assertEqual(hex_private_key, hex_serialize_private_key)

    def test_get_address_base58(self):
        base58_address = "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"
        hex_private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        account = Account(hex_private_key, SignatureScheme.SHA256withECDSA)
        self.assertEqual(base58_address, account.get_address_base58())

    def test_get_address_hex(self):
        hex_private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        account = Account(hex_private_key, SignatureScheme.SHA256withECDSA)
        hex_address = '4756c9dd829b2142883adbe1ae4f8689a1f673e9'
        self.assertEqual(hex_address, account.get_address_hex())

    def test_get_address_hex_reverse(self):
        hex_private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        account = Account(hex_private_key, SignatureScheme.SHA256withECDSA)
        hex_reverse_address = 'e973f6a189864faee1db3a8842219b82ddc95647'
        self.assertEqual(hex_reverse_address, account.get_address_hex_reverse())

    def test_get_signature_scheme(self):
        hex_private_key = '523c5fcf74823831752f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        account = Account(hex_private_key, SignatureScheme.SHA256withECDSA)
        signature_scheme = account.get_signature_scheme()
        self.assertEqual(SignatureScheme, type(signature_scheme))

    def test_serialize_public_key(self):
        hex_private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        hex_public_key = "03036c12be3726eb283d078dff481175e96224f0b0c632c7a37e10eb40fe6be889"
        account = Account(hex_private_key, SignatureScheme.SHA256withECDSA)
        self.assertEqual(hex_public_key, account.serialize_public_key().hex())

    def test_export_wif(self):
        private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        account = Account(private_key, SignatureScheme.SHA256withECDSA)
        wif = 'KyyZpJYXRfW8CXxH2B6FRq5AJsyTH7PjPACgBht4xRjstz4mxkeJ'
        self.assertEqual(wif, account.export_wif())

    def test_get_private_key_from_wif(self):
        private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        wif = 'KyyZpJYXRfW8CXxH2B6FRq5AJsyTH7PjPACgBht4xRjstz4mxkeJ'
        self.assertEqual(private_key, Account.get_private_key_from_wif(wif).hex())


if __name__ == '__main__':
    unittest.main()
