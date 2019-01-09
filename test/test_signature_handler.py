#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from test import sdk, acct1, acct2


class TestSignatureHandler(unittest.TestCase):
    def test_tx_signature(self):
        b58_from_address = acct1.get_address_base58()
        b58_to_address = acct2.get_address_base58()
        tx = sdk.native_vm.asset().new_transfer_transaction('ont', b58_from_address, b58_to_address, 10,
                                                            b58_from_address, 20000, 0)
        tx.sign_transaction(acct1)
        self.assertTrue(acct1.verify_signature(tx.hash256_bytes(), tx.sigs[0].sig_data[0]))
        self.assertFalse(acct2.verify_signature(tx.hash256_bytes(), tx.sigs[0].sig_data[0]))
        tx.add_sign_transaction(acct2)
        self.assertTrue(acct2.verify_signature(tx.hash256_bytes(), tx.sigs[1].sig_data[0]))

    def test_generate_signature(self):
        msg = b'Attack!'
        signature = acct1.generate_signature(msg)
        result = acct1.verify_signature(msg, signature)
        self.assertTrue(result)
        result = acct2.verify_signature(msg, signature)
        self.assertFalse(result)
