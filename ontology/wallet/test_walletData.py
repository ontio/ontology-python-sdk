from unittest import TestCase
from ontology.wallet.wallet import WalletData
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity


class TestWalletData(TestCase):

    def test_field(self):
        data = AccountData()
        print(data.algorithm)

    def test_clone(self):
        w = WalletData(default_ontid='hahaha')
        clone = w.clone()
        print(clone.__dict__)

    def test_add_account(self):
        w = WalletData(default_ontid='hahaha')
        acct = AccountData()
        w.add_account(acct)
        print(w.accounts[0])

    def test_remove_account(self):
        w = WalletData(default_ontid='hahaha')
        acct1 = AccountData(address="123")
        acct2 = AccountData(address="456")
        w.add_account(acct1)
        w.add_account(acct2)
        print(len(w.accounts))
        w.remove_account("123")
        print(len(w.accounts))

    def test_get_account_by_index(self):
        w = WalletData(default_ontid='hahaha')
        acct1 = AccountData(address="123")
        acct2 = AccountData(address="456")
        w.add_account(acct1)
        w.add_account(acct2)
        print(len(w.accounts))
        r = w.get_account_by_index(1)
        print(r)
        r = w.get_account_by_index(2)
        print(r)

    def test_get_account_by_address(self):
        w = WalletData(default_ontid='hahaha')
        acct1 = AccountData(address="123")
        acct2 = AccountData(address="456")
        w.add_account(acct1)
        w.add_account(acct2)
        print(len(w.accounts))
        r = w.get_account_by_address("123")
        print(r[0])
        print(r[1])

    def test_add_identity(self):
        w = WalletData(default_ontid='hahaha')
        iden = Identity()
        print(len(w.identities))
        w.add_identity(iden)
        print(len(w.identities))
        print(w.identities[0].__dict__)

    def test_remove_identity(self):
        w = WalletData(default_ontid='hahaha')
        iden = Identity(ontid="123")
        w.add_identity(iden)
        print(len(w.identities))
        w.remove_identity("123")
        print(len(w.identities))
