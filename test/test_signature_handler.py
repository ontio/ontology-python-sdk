#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from test import sdk, acct1, acct2

from ontology.crypto.signature_scheme import SignatureScheme
from ontology.crypto.signature_handler import SignatureHandler


class TestSignatureHandler(unittest.TestCase):
    def test_tx_signature(self):
        b58_from_address = acct1.get_address_base58()
        b58_to_address = acct2.get_address_base58()
        tx = sdk.native_vm.asset().new_transfer_transaction('ont', b58_from_address, b58_to_address, 10,
                                                            b58_from_address, 20000, 0)
        tx.sign_transaction(acct1)
        self.assertTrue(acct1.verify_signature(tx.hash256_bytes(), tx.sig_list[0].sig_data[0]))
        self.assertFalse(acct2.verify_signature(tx.hash256_bytes(), tx.sig_list[0].sig_data[0]))
        tx.add_sign_transaction(acct2)
        self.assertTrue(acct2.verify_signature(tx.hash256_bytes(), tx.sig_list[1].sig_data[0]))

    def test_generate_signature(self):
        msg = b'Attack!'
        signature = acct1.generate_signature(msg)
        result = acct1.verify_signature(msg, signature)
        self.assertTrue(result)
        result = acct2.verify_signature(msg, signature)
        self.assertFalse(result)

    def test_verify_cyano_signature(self):
        msg = b'123'
        sign = '0b6912568942a1e646b3a532dc904e965eb1085bab877bc34fe06768257f07b3' \
               '079af3fa69fc759b51fa2bf894a7fd748ab5bc326c8663a01f90dcc518184e65'
        pk = '03036c12be3726eb283d078dff481175e96224f0b0c632c7a37e10eb40fe6be889'
        handler = SignatureHandler(SignatureScheme.SHA256withECDSA)
        result = handler.verify_signature(bytes.fromhex(pk), msg, bytes.fromhex(sign))
        self.assertTrue(result)
        sign = '010b6912568942a1e646b3a532dc904e965eb1085bab877bc34fe06768257f07b' \
               '3079af3fa69fc759b51fa2bf894a7fd748ab5bc326c8663a01f90dcc518184e65'
        handler = SignatureHandler(SignatureScheme.SHA256withECDSA)
        result = handler.verify_signature(bytes.fromhex(pk), msg, bytes.fromhex(sign))
        self.assertTrue(result)
