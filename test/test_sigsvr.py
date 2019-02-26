#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from os import path

from test import sdk, password

from ontology.crypto.signature_handler import SignatureHandler


class TestSigSvr(unittest.TestCase):
    def test_create_account(self):
        result = sdk.service.sig_svr().create_account(password)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(34, len(result.get('account', '')))

    def test_export_account(self):
        export_path = path.dirname(__file__)
        result = sdk.service.sig_svr().export_account(export_path)
        wm =sdk.wallet_manager
        wm.open_wallet(result['wallet_file'])
        try:
            self.assertEqual(result['account_num'], len(wm.get_acct_data_list()))
        finally:
            wm.del_wallet_file()

    def test_sig_data(self):
        export_path = path.dirname(__file__)
        result = sdk.service.sig_svr().export_account(export_path)
        wm = sdk.wallet_manager
        wm.open_wallet(result['wallet_file'])
        try:
            self.assertEqual(result['account_num'], len(wm.get_acct_data_list()))
            acct = wm.get_wallet().get_account_by_index(0)
            b58_address = acct.b58_address
            scheme = acct.signature_scheme
            msg = b'Hello, world!'
            result = sdk.service.sig_svr().sig_data(bytes.hex(msg), b58_address, password)
            signature = bytes.fromhex(result.get('signed_data', ''))
            handler = SignatureHandler(scheme)
            is_valid = handler.verify_signature(acct.public_key, msg, signature)
            self.assertTrue(is_valid)
        finally:
            wm.del_wallet_file()
