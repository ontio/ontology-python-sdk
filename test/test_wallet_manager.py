#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from ontology.crypto.signature_scheme import SignatureScheme
from ontology.wallet.wallet_manager import WalletManager
from ontology.account.account import Account
from ontology.utils import util


class TestWalletManager(unittest.TestCase):
    def test_open_wallet(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        self.assertEqual(wm.__dict__['scheme'], SignatureScheme.SHA256withECDSA)
        os.remove(path)

    def test_get_accounts(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = "password"
        size = 5
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        os.remove(path)

    def test_set_default_account(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = "password"
        size = 3
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        for index in range(size):
            wm.get_wallet().set_default_account(index)
            self.assertEqual(accounts[index].address, wm.get_wallet().get_default_account_address())
        os.remove(path)

    def test_import_identity(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        salt = util.get_random_str(16)
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key)
        enpri = acct.export_gcm_encrypted_private_key("1", salt, 16384)
        wm.import_identity("label2", enpri, "1", salt, acct.get_address_base58())
        os.remove(path)

    def test_create_identity_from_prikey(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        ide = wm.create_identity_from_pri_key("ide", "1", private_key)
        self.assertEqual(ide.label, 'ide')
        self.assertEqual(ide.ont_id, 'did:ont:AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve')
        os.remove(path)

    def test_import_account(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        wm.open_wallet("./test.json")
        wm.import_account("label2", "Yl1e9ugbVADd8a2SbAQ56UfUvr3e9hD2eNXAM9xNjhnefB+YuNXDFvUrIRaYth+L", "1",
                          "AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve", "pwLIUKAf2bAbTseH/WYrfQ==")
        wm.save()
        os.remove(path)

    def test_create_account_from_prikey(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        account = wm.create_account_from_prikey("myaccount", "1", private_key)
        wm.save()
        self.assertEqual(account.address, 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve')
        os.remove(path)


if __name__ == '__main__':
    unittest.main()
