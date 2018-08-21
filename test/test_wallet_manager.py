#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import unittest

from ontology.crypto.signature_scheme import SignatureScheme
from ontology.wallet.wallet_manager import WalletManager
from ontology.exception.exception import SDKException
from ontology.account.account import Account
from ontology.utils import util


class TestWalletManager(unittest.TestCase):
    def test_aa(self):
        wm = WalletManager()
        wm.open_wallet("test9.json")
        wm.create_account("ss", "111111")
        wm.create_identity("ss", "111111")
        wm.write_wallet()

    def test_open_wallet(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet("./test.json")
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

    def test_set_default_identity_by_index(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        size = 3
        for i in range(size):
            private_key = util.get_random_str(64)
            wm.create_identity_from_pri_key("ide", str(i), private_key)
        identities = wm.get_wallet().get_identities()
        self.assertEqual(len(identities), size)
        self.assertRaises(SDKException, wm.get_wallet().set_default_identity_by_index, size)
        for index in range(size):
            wm.get_wallet().set_default_identity_by_index(index)
            default_identity = wm.get_default_identity()
            self.assertEqual(identities[index], default_identity)
        os.remove(path)

    def test_set_default_identity_by_ont_id(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = "password"
        size = 3
        for i in range(size):
            private_key = util.get_random_str(64)
            wm.create_identity_from_pri_key("ide", str(i), private_key)
        identities = wm.get_wallet().get_identities()
        self.assertEqual(len(identities), size)
        self.assertRaises(SDKException, wm.get_wallet().set_default_identity_by_ont_id, '')
        ont_id_list = list()
        for identity in wm.get_wallet().identities:
            ont_id_list.append(identity.ontid)
        for index in range(size * 5):
            rand_ont_id = random.choice(ont_id_list)
            wm.get_wallet().set_default_identity_by_ont_id(rand_ont_id)
            default_identity = wm.get_default_identity()
            self.assertEqual(rand_ont_id, default_identity.ontid)
        os.remove(path)

    def test_set_default_account_by_index(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = "password"
        size = 3
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        self.assertRaises(SDKException, wm.get_wallet().set_default_account_by_index, size)
        for index in range(size):
            wm.get_wallet().set_default_account_by_index(index)
            default_address = wm.get_wallet().get_default_account_address()
            self.assertEqual(accounts[index].address, default_address)
        os.remove(path)

    def test_set_default_account_by_address(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = "password"
        size = 3
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        self.assertRaises(SDKException, wm.get_wallet().set_default_account_by_address, '1')
        for acct in accounts:
            wm.get_wallet().set_default_account_by_address(acct.address)
            default_address = wm.get_wallet().get_default_account_address()
            self.assertEqual(default_address, acct.address)
        os.remove(path)

    def test_get_default_account(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = "password"
        size = 3
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        for acct in accounts:
            wm.get_wallet().set_default_account_by_address(acct.address)
            default_account = wm.get_default_account()
            self.assertEqual(default_account.address, acct.address)
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
