#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from Cryptodome.Random.random import choice

from test import sdk, identity1, password

from ontology.utils import utils
from ontology.crypto.curve import Curve
from ontology.account.account import Account
from ontology.wallet.account import AccountData
from ontology.crypto.signature import Signature
from ontology.exception.exception import SDKException
from ontology.wallet.wallet_manager import WalletManager
from ontology.crypto.signature_scheme import SignatureScheme


class TestWalletManager(unittest.TestCase):
    def test_create_write(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        password = utils.get_random_hex_str(10)
        label = 'label'
        wm.create_account(label, password)
        default_account = wm.get_default_account()
        self.assertEqual(label, default_account.label)
        wm.create_identity(label, password)
        default_identity = wm.get_default_identity()
        self.assertEqual(label, default_identity.label)
        wm.write_wallet()
        os.remove(path)

    def test_open_wallet(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        self.assertEqual(wm.__dict__['scheme'], SignatureScheme.SHA256withECDSA)
        wm.write_wallet()
        os.remove(path)

    def test_open_cyano_wallet(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'cyano_wallet.json')
        wm.open_wallet(path)
        self.assertEqual(wm.__dict__['scheme'], SignatureScheme.SHA256withECDSA)
        account = wm.get_account_by_b58_address('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', '1234567890')
        self.assertTrue(isinstance(account, Account))

    def test_wallet_data(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'wallet.json')
        self.assertRaises(SDKException, wm.create_wallet, path)
        wm.open_wallet(path)
        self.assertTrue(isinstance(wm, WalletManager))
        self.assertEqual(wm.__dict__['scheme'], SignatureScheme.SHA256withECDSA)

        size = 32
        dict_wallet_in_mem = wm.wallet_in_mem.__dict__
        self.assertEqual(dict_wallet_in_mem['name'], 'MyWallet')
        self.assertEqual(dict_wallet_in_mem['version'], '1.1')
        self.assertEqual(len(dict_wallet_in_mem['accounts']), size)

        dict_accounts = dict(wm.wallet_in_mem.accounts[0])
        self.assertEqual(dict_accounts['address'], 'Ad4pjz2bqep4RhQrUAzMuZJkBC3qJ1tZuT')
        self.assertEqual(dict_accounts['algorithm'], 'ECDSA')
        self.assertEqual(dict_accounts['enc-alg'], 'aes-256-gcm')
        self.assertEqual(dict_accounts['isDefault'], True)
        self.assertEqual(dict_accounts['key'], 'O6/Ens58XsV4+TqbKIZ5qgM76pTC0KsufNYV3VKDmHtG6VFvDZUblVWSAM6XBwKk')
        self.assertEqual(dict_accounts['label'], '')
        self.assertEqual(dict_accounts['lock'], False)
        self.assertEqual(dict_accounts['parameters']['curve'], 'P-256')
        self.assertEqual(dict_accounts['salt'], 'OkX96EG0OaCNUFD3hdc50Q==')
        self.assertEqual(dict_accounts['signatureScheme'], 'SHA256withECDSA')

        dict_accounts = dict(wm.wallet_in_mem.accounts[15])
        self.assertEqual(dict_accounts['address'], 'AZy1ApV47jLM4m4a2MSx92hzwpDcMtn96z')
        self.assertEqual(dict_accounts['enc-alg'], 'aes-256-gcm')
        self.assertEqual(dict_accounts['isDefault'], False)
        self.assertEqual(dict_accounts['key'], 'ATqEeReytF1Ma16KJKWlvnSmHeH7p8l5Es3Ngp/62l/1Pp4K4fhAaXOfahZ6g8Wd')
        self.assertEqual(dict_accounts['label'], '4c0638c9')
        self.assertEqual(dict_accounts['lock'], False)
        self.assertEqual(dict_accounts['parameters']['curve'], 'P-256')
        self.assertEqual(dict_accounts['salt'], 'tJHCzvar3e5dPkIyXswx5w==')
        self.assertEqual(dict_accounts['signatureScheme'], 'SHA256withECDSA')

        dict_accounts = dict(wm.wallet_in_mem.accounts[31])
        self.assertEqual(dict_accounts['address'], 'Aa4diLddFtHg5fU7Nf71q3KwBmu21D4ZyM')
        self.assertEqual(dict_accounts['enc-alg'], 'aes-256-gcm')
        self.assertEqual(dict_accounts['isDefault'], False)
        self.assertEqual(dict_accounts['key'], 'epWSyUe9VUI81WIe30ul2B/ahjHhc1sXRg7IJjV2jk39BPzkrMbIa5p9UOOrAZ3e')
        self.assertEqual(dict_accounts['label'], '')
        self.assertEqual(dict_accounts['lock'], False)
        self.assertEqual(dict_accounts['parameters']['curve'], 'P-256')
        self.assertEqual(dict_accounts['salt'], 'DqS/T2FmSmYabWdW1vQYzQ==')
        self.assertEqual(dict_accounts['signatureScheme'], 'SHA256withECDSA')

    def test_get_account(self):
        wallet_manager = WalletManager()
        password = 'password'
        acct0 = wallet_manager.create_account('', password)
        self.assertTrue(isinstance(acct0, AccountData))
        b58_address = wallet_manager.wallet_in_mem.default_account_address
        acct0 = wallet_manager.get_account_by_b58_address(b58_address, password)
        self.assertEqual(acct0.get_address_base58(), b58_address)
        self.assertRaises(SDKException, wallet_manager.get_account_by_b58_address, b58_address, 'wrong_password')

        b58_address = 'AHX1wzvdw9Yipk7E9MuLY4GGX4Ym9tHeDe'
        encrypted_pri_key = '8p2q0vLRqyfKmFHhnjUYVWOm12kPm78JWqzkTOi9rrFMBz624KjhHQJpyPmiSSOa'
        password = '111111'
        label = ''
        base64_salt = 'KbiCUr53CZUfKG1M3Gojjw=='
        acct1 = wallet_manager.import_account(label, encrypted_pri_key, password, b58_address, base64_salt)
        self.assertEqual(b58_address, acct1.b58_address)
        import_acct = wallet_manager.get_account_by_b58_address(b58_address, password)
        self.assertEqual(b58_address, import_acct.get_address_base58())
        self.assertEqual(base64_salt, acct1.salt)

    def test_get_accounts(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
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
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        size = 3
        for i in range(size):
            private_key = utils.get_random_hex_str(64)
            wm.create_identity_from_private_key("ide", str(i), private_key)
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
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        size = 3
        for i in range(size):
            private_key = utils.get_random_hex_str(64)
            wm.create_identity_from_private_key("ide", str(i), private_key)
        identities = wm.get_wallet().get_identities()
        self.assertEqual(len(identities), size)
        self.assertRaises(SDKException, wm.get_wallet().set_default_identity_by_ont_id, '')
        ont_id_list = list()
        for identity in wm.get_wallet().identities:
            ont_id_list.append(identity.ont_id)
        for index in range(size * 5):
            rand_ont_id = choice(ont_id_list)
            wm.get_wallet().set_default_identity_by_ont_id(rand_ont_id)
            default_identity = wm.get_default_identity()
            self.assertEqual(rand_ont_id, default_identity.ont_id)
        wm.write_wallet()
        os.remove(path)

    def test_set_default_account_by_index(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
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
            self.assertEqual(accounts[index].b58_address, default_address)
        wm.write_wallet()
        os.remove(path)

    def test_set_default_account_by_address(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        password = 'password'
        size = 3
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        self.assertRaises(SDKException, wm.get_wallet().set_default_account_by_address, '1')
        for acct in accounts:
            wm.get_wallet().set_default_account_by_address(acct.b58_address)
            default_address = wm.get_wallet().get_default_account_address()
            self.assertEqual(default_address, acct.b58_address)
        wm.write_wallet()
        os.remove(path)

    def test_get_default_account(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        password = 'password'
        size = 3
        for i in range(size):
            wm.create_account('', password)
        accounts = wm.get_wallet().get_accounts()
        self.assertEqual(len(accounts), size)
        for acct in accounts:
            wm.get_wallet().set_default_account_by_address(acct.b58_address)
            default_account = wm.get_default_account()
            self.assertEqual(default_account.b58_address, acct.b58_address)
        wm.write_wallet()
        os.remove(path)

    def test_import_identity(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        private_key = utils.get_random_hex_str(64)
        acct = Account(private_key)
        password = utils.get_random_hex_str(10)
        salt = utils.get_random_hex_str(16)
        scrypt_n = 16384
        encrypted_private_key = acct.export_gcm_encrypted_private_key(password, salt, scrypt_n)
        label = 'label'
        b58_address = acct.get_address_base58()
        wm.import_identity(label, encrypted_private_key, password, salt, b58_address)
        identity = wm.get_default_identity()
        self.assertEqual(label, identity.label)
        wm.write_wallet()
        os.remove(path)

    def test_create_identity_from_pri_key(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        ide = wm.create_identity_from_private_key("ide", "1", private_key)
        self.assertEqual(ide.label, 'ide')
        self.assertEqual(ide.ont_id, 'did:ont:AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve')
        wm.write_wallet()
        os.remove(path)

    def test_import_account(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        label = 'label'
        encrypted_pri_key = 'Yl1e9ugbVADd8a2SbAQ56UfUvr3e9hD2eNXAM9xNjhnefB+YuNXDFvUrIRaYth+L'
        password = '1'
        b58_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        b64_salt = 'pwLIUKAf2bAbTseH/WYrfQ=='
        account = wm.import_account(label, encrypted_pri_key, password, b58_address, b64_salt)
        self.assertTrue(isinstance(account, AccountData))
        wm.save()
        os.remove(path)

    def test_create_account_from_private_key(self):
        wm = WalletManager()
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        self.assertRaises(SDKException, wm.open_wallet, path)
        wm.create_wallet(path)
        wm.open_wallet(path)
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        label = 'hello_account'
        password = 'password'
        account = wm.create_account_from_private_key(label, password, private_key)
        b58_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        wm.save()
        self.assertEqual(b58_address, account.b58_address)
        os.remove(path)

    def test_add_control_by_private_key(self):
        private_key = utils.get_random_bytes(32)
        hex_private_key = private_key.hex()
        public_key = Signature.ec_get_public_key_by_private_key(private_key, Curve.P256)
        hex_public_key = public_key.hex()
        sdk.wallet_manager.add_control_by_private_key(identity1.ont_id, password, hex_private_key)
        ctrl_acct = sdk.wallet_manager.get_control_account_by_index(identity1.ont_id, 1, password)
        acct_private_key = ctrl_acct.get_private_key_hex()
        acct_public_key = ctrl_acct.get_public_key_hex()
        self.assertEqual(hex_public_key, acct_public_key)
        self.assertEqual(hex_private_key, acct_private_key)
        ctrl_len_1 = len(sdk.wallet_manager.wallet_in_mem.identities[0].controls)
        ctrl_len_2 = len(sdk.wallet_manager.wallet_file.identities[0].controls)
        self.assertEqual(ctrl_len_1, ctrl_len_2 + 1)


if __name__ == '__main__':
    unittest.main()
