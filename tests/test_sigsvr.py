#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import unittest

from os import path

from tests import sdk, password

from ontology.crypto.signature_handler import SignatureHandler


class TestSigSvr(unittest.TestCase):
    def test_create_account(self):
        sdk.service.sig_svr.connect_to_localhost()
        result = sdk.service.sig_svr.create_account(password)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(34, len(result.get('account', '')))

    def test_export_account(self):
        sdk.service.sig_svr.connect_to_localhost()
        export_path = path.dirname(__file__)
        result = sdk.service.sig_svr.export_account(export_path)
        wm = sdk.wallet_manager
        wm.open_wallet(result['wallet_file'])
        try:
            self.assertEqual(result['account_num'], len(wm.get_acct_data_list()))
        finally:
            wm.del_wallet_file()

    def test_sig_data(self):
        sdk.service.sig_svr.connect_to_localhost()
        export_path = path.dirname(__file__)
        result = sdk.service.sig_svr.export_account(export_path)
        wm = sdk.wallet_manager
        wm.open_wallet(result['wallet_file'])
        try:
            self.assertEqual(result['account_num'], len(wm.get_acct_data_list()))
            acct = wm.get_wallet().get_account_by_index(0)
            b58_address = acct.b58_address
            scheme = acct.signature_scheme
            msg = b'Hello, world!'
            result = sdk.service.sig_svr.sig_data(bytes.hex(msg), b58_address, password)
            signature = bytes.fromhex(result.get('signed_data', ''))
            handler = SignatureHandler(scheme)
            is_valid = handler.verify_signature(acct.public_key, msg, signature)
            self.assertTrue(is_valid)
        finally:
            wm.del_wallet_file()
