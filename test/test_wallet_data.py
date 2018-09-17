#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import unittest

from ontology.wallet.wallet import WalletData
from ontology.wallet.identity import Identity
from ontology.wallet.account import AccountData


class TestWalletData(unittest.TestCase):
    def test_init(self):
        wallet = WalletData()
        self.assertTrue(isinstance(wallet, WalletData))

    def test_add_account(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        b58_address = 'AKck7c1ySGr63UinVcMcyuoZD4nXbMk7Sw'
        acct = AccountData(b58_address)
        wallet.add_account(acct)
        acct = wallet.accounts[0]
        self.assertTrue(isinstance(acct, AccountData))

    def test_remove_account(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        address_list = list()
        for i in range(size):
            address = random.randint(0, 1000000000)
            acct = AccountData(address=address)
            wallet.add_account(acct)
            address_list.append(address)
            self.assertEqual(len(wallet.accounts), i + 1)

        for i in range(size):
            rand_address = random.choice(address_list)
            wallet.remove_account(rand_address)
            address_list.remove(rand_address)
            self.assertEqual(len(wallet.accounts), size - i - 1)

    def test_get_account_by_index(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        address_list = list()
        for i in range(size):
            address = random.randint(0, 1000000000)
            acct = AccountData(address=address)
            wallet.add_account(acct)
            address_list.append(address)
            self.assertEqual(len(wallet.accounts), i + 1)

        for i in range(size * 2):
            index = random.choice(range(size))
            acct = wallet.get_account_by_index(index)
            self.assertEqual(address_list[index], acct.address)

    def test_get_account_by_address(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        address_list = list()
        for i in range(size):
            address = random.randint(0, 1000000000)
            acct = AccountData(address=address)
            wallet.add_account(acct)
            address_list.append(address)
            self.assertEqual(len(wallet.accounts), i + 1)

        for i in range(size * 2):
            rand_address = random.choice(address_list)
            acct = wallet.get_account_by_address(rand_address)
            self.assertEqual(rand_address, acct.address)

    def test_add_identity(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        for i in range(size):
            rand_id = random.randint(0, 1000000000)
            identity = Identity(ont_id=rand_id)
            wallet.add_identity(identity)
            self.assertEqual(len(wallet.get_identities()), i + 1)

    def test_remove_identity(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        id_list = list()
        for i in range(size):
            rand_id = random.randint(0, 1000000000)
            identity = Identity(ont_id=rand_id)
            wallet.add_identity(identity)
            id_list.append(rand_id)
            self.assertEqual(len(wallet.get_identities()), i + 1)

        for i in range(size):
            rand_id = random.choice(id_list)
            wallet.remove_identity(rand_id)
            id_list.remove(rand_id)
            self.assertEqual(len(wallet.get_identities()), size - i - 1)

    def test_get_identities(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        id_list = list()
        for i in range(size):
            rand_id = random.randint(0, 1000000000)
            identity = Identity(ont_id=rand_id)
            wallet.add_identity(identity)
            id_list.append(rand_id)
            self.assertEqual(len(wallet.get_identities()), i + 1)
        identities = wallet.get_identities()
        self.assertEqual(len(identities), size)


if __name__ == '__main__':
    unittest.main()
