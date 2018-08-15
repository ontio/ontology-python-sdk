#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import unittest

from ontology.wallet.wallet import WalletData
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity


class TestWalletData(unittest.TestCase):
    def test_add_account(self):
        test_id = "test_ont_id"
        w = WalletData(default_id=test_id)
        acct = AccountData()
        w.add_account(acct)
        acct = w.accounts[0]
        self.assertTrue(isinstance(acct, AccountData))

    def test_remove_account(self):
        test_id = "test_ont_id"
        w = WalletData(default_id=test_id)
        size = 10
        address_list = list()
        for i in range(size):
            address = random.randint(0, 1000000000)
            acct = AccountData(address=address)
            w.add_account(acct)
            address_list.append(address)
            self.assertEqual(len(w.accounts), i + 1)

        for i in range(size):
            rand_address = random.choice(address_list)
            w.remove_account(rand_address)
            address_list.remove(rand_address)
            self.assertEqual(len(w.accounts), size - i - 1)

    def test_get_account_by_index(self):
        test_id = "test_ont_id"
        w = WalletData(default_id=test_id)
        size = 10
        address_list = list()
        for i in range(size):
            address = random.randint(0, 1000000000)
            acct = AccountData(address=address)
            w.add_account(acct)
            address_list.append(address)
            self.assertEqual(len(w.accounts), i + 1)

        for i in range(size * 2):
            index = random.choice(range(size))
            acct = w.get_account_by_index(index)
            self.assertEqual(address_list[index], acct.address)

    def test_get_account_by_address(self):
        test_id = "test_ont_id"
        w = WalletData(default_id=test_id)
        size = 10
        address_list = list()
        for i in range(size):
            address = random.randint(0, 1000000000)
            acct = AccountData(address=address)
            w.add_account(acct)
            address_list.append(address)
            self.assertEqual(len(w.accounts), i + 1)

        for i in range(size * 2):
            rand_address = random.choice(address_list)
            acct = w.get_account_by_address(rand_address)
            self.assertEqual(rand_address, acct.address)

    def test_add_identity(self):
        test_id = "test_ont_id"
        w = WalletData(default_id=test_id)
        size = 10
        for i in range(size):
            rand_id = random.randint(0, 1000000000)
            identity = Identity(ont_id=rand_id)
            w.add_identity(identity)
            self.assertEqual(len(w.identities), i + 1)

    def test_remove_identity(self):
        test_id = "test_ont_id"
        w = WalletData(default_id=test_id)
        size = 10
        id_list = list()
        for i in range(size):
            rand_id = random.randint(0, 1000000000)
            identity = Identity(ont_id=rand_id)
            w.add_identity(identity)
            id_list.append(rand_id)
            self.assertEqual(len(w.identities), i + 1)

        for i in range(size):
            rand_id = random.choice(id_list)
            w.remove_identity(rand_id)
            id_list.remove(rand_id)
            self.assertEqual(len(w.identities), size - i - 1)


if __name__ == '__main__':
    unittest.main()
