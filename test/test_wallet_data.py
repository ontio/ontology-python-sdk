#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import unittest

from Cryptodome.Random.random import randint, choice

from ontology.common.define import DID_ONT
from ontology.wallet.wallet import WalletData
from ontology.wallet.identity import Identity
from ontology.wallet.account import AccountData
from ontology.exception.exception import SDKException


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

    def create_wallet_data(self, default_id, size):
        wallet = WalletData(default_id=default_id)
        address_list = list()
        for i in range(size):
            address = randint(0, 1000000000)
            acct = AccountData(b58_address=address)
            wallet.add_account(acct)
            address_list.append(address)
            self.assertEqual(len(wallet.accounts), i + 1)
        return wallet, address_list

    def test_remove_account(self):
        test_id = "test_ont_id"
        size = 10
        wallet, address_list = self.create_wallet_data(test_id, size)
        for i in range(size):
            rand_address = choice(address_list)
            wallet.remove_account(rand_address)
            address_list.remove(rand_address)
            self.assertEqual(len(wallet.accounts), size - i - 1)

    def test_get_account_by_index(self):
        test_id = "test_ont_id"
        size = 10
        wallet, address_list = self.create_wallet_data(test_id, size)
        for _ in range(size * 2):
            index = choice(range(size))
            acct = wallet.get_account_by_index(index)
            self.assertEqual(address_list[index], acct.b58_address)

    def test_get_account_by_address(self):
        test_id = "test_ont_id"
        size = 10
        wallet, address_list = self.create_wallet_data(test_id, size)
        for i in range(size * 2):
            rand_address = choice(address_list)
            acct = wallet.get_account_by_b58_address(rand_address)
            self.assertEqual(rand_address, acct.b58_address)

    def test_add_identity(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        for i in range(size):
            rand_id = DID_ONT + str(randint(0, 1000000000))
            identity = Identity(ont_id=rand_id)
            wallet.add_identity(identity)
            self.assertEqual(len(wallet.get_identities()), i + 1)

    def test_remove_identity(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        id_list = list()
        for i in range(size):
            try:
                rand_id = str(randint(0, 1000000000))
                Identity(ont_id=rand_id)
            except SDKException as e:
                self.assertTrue(isinstance(e, SDKException))
            rand_id = DID_ONT + str(randint(0, 1000000000))
            identity = Identity(ont_id=rand_id)
            wallet.add_identity(identity)
            id_list.append(rand_id)
            self.assertEqual(len(wallet.get_identities()), i + 1)

        for i in range(size):
            rand_id = choice(id_list)
            wallet.remove_identity(rand_id)
            id_list.remove(rand_id)
            self.assertEqual(len(wallet.get_identities()), size - i - 1)

    def test_get_identities(self):
        test_id = "test_ont_id"
        wallet = WalletData(default_id=test_id)
        size = 10
        id_list = list()
        for i in range(size):
            rand_id = DID_ONT + str(randint(0, 1000000000))
            identity = Identity(ont_id=rand_id)
            wallet.add_identity(identity)
            id_list.append(rand_id)
            self.assertEqual(len(wallet.get_identities()), i + 1)
        identities = wallet.get_identities()
        self.assertEqual(len(identities), size)

    def test_deep_copy(self):
        wallet_1 = WalletData()
        size = 10
        id_list = list()
        for i in range(size):
            rand_id = DID_ONT + str(randint(0, 1000000000))
            identity = Identity(ont_id=rand_id)
            wallet_1.add_identity(identity)
            id_list.append(rand_id)
            self.assertEqual(len(wallet_1.get_identities()), i + 1)
        wallet_2 = copy.deepcopy(wallet_1)
        self.assertNotEqual(id(wallet_1), id(wallet_2))
        self.assertEqual(wallet_1.name, wallet_2.name)
        wallet_2.name = 'newWallet'
        self.assertNotEqual(id(wallet_1.name), id(wallet_2.name))
        for i in range(size):
            self.assertEqual(wallet_1.identities[i].ont_id, wallet_2.identities[i].ont_id)
            rand_id = DID_ONT + str(randint(0, 1000000000))
            wallet_1.identities[i].ont_id = rand_id
            try:
                wallet_1.identities[i].ont_id = str(randint(0, 1000000000))
            except SDKException as e:
                self.assertTrue(isinstance(e, SDKException))
            self.assertNotEqual(wallet_1.identities[i].ont_id, wallet_2.identities[i].ont_id)
            self.assertNotEqual(id(wallet_1.identities[i]), id(wallet_2.identities[i]))


if __name__ == '__main__':
    unittest.main()
