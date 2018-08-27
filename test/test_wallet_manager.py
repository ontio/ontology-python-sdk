#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import unittest

from ontology.utils import util
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.wallet.wallet_manager import WalletManager
from ontology.crypto.signature_scheme import SignatureScheme


class TestWalletManager(unittest.TestCase):
    def test_create_write(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = 'password'
        label = 'label'
        wm.create_account(label, password)
        wm.create_identity(label, password)
        wm.write_wallet()
        os.remove(path)

    def test_open_wallet(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        self.assertEqual(wm.__dict__['scheme'], SignatureScheme.SHA256withECDSA)
        wm.write_wallet()
        os.remove(path)

    def test_wallet_data(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'wallet.dat')
        wm.open_wallet(path)
        self.assertTrue(isinstance(wm, WalletManager))
        self.assertEqual(wm.__dict__['scheme'], SignatureScheme.SHA256withECDSA)

        size = 32
        dict_wallet_in_mem = wm.wallet_in_mem.__dict__
        self.assertEqual(dict_wallet_in_mem['name'], 'MyWallet')
        self.assertEqual(dict_wallet_in_mem['version'], '1.1')
        self.assertEqual(len(dict_wallet_in_mem['accounts']), size)

        dict_accounts = wm.wallet_in_mem.accounts[0].__dict__
        self.assertEqual(dict_accounts['address'], 'Ad4pjz2bqep4RhQrUAzMuZJkBC3qJ1tZuT')
        self.assertEqual(dict_accounts['algorithm'], 'ECDSA')
        self.assertEqual(dict_accounts['enc_alg'], 'aes-256-gcm')
        self.assertEqual(dict_accounts['is_default'], True)
        self.assertEqual(dict_accounts['key'], 'O6/Ens58XsV4+TqbKIZ5qgM76pTC0KsufNYV3VKDmHtG6VFvDZUblVWSAM6XBwKk')
        self.assertEqual(dict_accounts['label'], '')
        self.assertEqual(dict_accounts['lock'], False)
        self.assertEqual(dict_accounts['parameters']['curve'], 'P-256')
        self.assertEqual(dict_accounts['salt'], 'OkX96EG0OaCNUFD3hdc50Q==')
        self.assertEqual(dict_accounts['signature_scheme'], 'SHA256withECDSA')

        dict_accounts = wm.wallet_in_mem.accounts[15].__dict__
        self.assertEqual(dict_accounts['address'], 'AZy1ApV47jLM4m4a2MSx92hzwpDcMtn96z')
        self.assertEqual(dict_accounts['enc_alg'], 'aes-256-gcm')
        self.assertEqual(dict_accounts['is_default'], False)
        self.assertEqual(dict_accounts['key'], 'ATqEeReytF1Ma16KJKWlvnSmHeH7p8l5Es3Ngp/62l/1Pp4K4fhAaXOfahZ6g8Wd')
        self.assertEqual(dict_accounts['label'], '4c0638c9')
        self.assertEqual(dict_accounts['lock'], False)
        self.assertEqual(dict_accounts['parameters']['curve'], 'P-256')
        self.assertEqual(dict_accounts['salt'], 'tJHCzvar3e5dPkIyXswx5w==')
        self.assertEqual(dict_accounts['signature_scheme'], 'SHA256withECDSA')

        dict_accounts = wm.wallet_in_mem.accounts[31].__dict__
        self.assertEqual(dict_accounts['address'], 'Aa4diLddFtHg5fU7Nf71q3KwBmu21D4ZyM')
        self.assertEqual(dict_accounts['enc_alg'], 'aes-256-gcm')
        self.assertEqual(dict_accounts['is_default'], False)
        self.assertEqual(dict_accounts['key'], 'epWSyUe9VUI81WIe30ul2B/ahjHhc1sXRg7IJjV2jk39BPzkrMbIa5p9UOOrAZ3e')
        self.assertEqual(dict_accounts['label'], '')
        self.assertEqual(dict_accounts['lock'], False)
        self.assertEqual(dict_accounts['parameters']['curve'], 'P-256')
        self.assertEqual(dict_accounts['salt'], 'DqS/T2FmSmYabWdW1vQYzQ==')
        self.assertEqual(dict_accounts['signature_scheme'], 'SHA256withECDSA')

    def test_get_accounts(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = 'password'
        size = 5
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        wm.write_wallet()
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
        wm.write_wallet()
        os.remove(path)

    def test_set_default_identity_by_ont_id(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        size = 3
        for i in range(size):
            private_key = util.get_random_str(64)
            wm.create_identity_from_pri_key("ide", str(i), private_key)
        identities = wm.get_wallet().get_identities()
        self.assertEqual(len(identities), size)
        self.assertRaises(SDKException, wm.get_wallet().set_default_identity_by_ont_id, '')
        ont_id_list = list()
        for identity in wm.get_wallet().identities:
            ont_id_list.append(identity.ont_id)
        for index in range(size * 5):
            rand_ont_id = random.choice(ont_id_list)
            wm.get_wallet().set_default_identity_by_ont_id(rand_ont_id)
            default_identity = wm.get_default_identity()
            self.assertEqual(rand_ont_id, default_identity.ont_id)
        wm.write_wallet()
        os.remove(path)

    def test_set_default_account_by_index(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = 'password'
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
        wm.write_wallet()
        os.remove(path)

    def test_set_default_account_by_address(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = 'password'
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
        wm.write_wallet()
        os.remove(path)

    def test_get_default_account(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        password = 'password'
        size = 3
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        for acct in accounts:
            wm.get_wallet().set_default_account_by_address(acct.address)
            default_account = wm.get_default_account()
            self.assertEqual(default_account.address, acct.address)
        wm.write_wallet()
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
        wm.write_wallet()
        os.remove(path)

    def test_create_identity_from_prikey(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        ide = wm.create_identity_from_pri_key("ide", "1", private_key)
        self.assertEqual(ide.label, 'ide')
        self.assertEqual(ide.ont_id, 'did:ont:AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve')
        wm.write_wallet()
        os.remove(path)

    def test_import_account(self):
        wm = WalletManager()
        path = os.path.join(os.getcwd(), 'test.json')
        wm.open_wallet(path)
        label = 'label'
        encrypted_pri_key = 'Yl1e9ugbVADd8a2SbAQ56UfUvr3e9hD2eNXAM9xNjhnefB+YuNXDFvUrIRaYth+L'
        password = '1'
        b58_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        b64_salt = 'pwLIUKAf2bAbTseH/WYrfQ=='
        wm.import_account(label, encrypted_pri_key, password, b58_address, b64_salt)
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
