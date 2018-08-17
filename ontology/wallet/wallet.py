#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.crypto.scrypt import Scrypt
from ontology.wallet.identity import Identity
from ontology.wallet.account import AccountData
from ontology.common.error_code import ErrorCode
from ontology.exception.exception import SDKException


class WalletData(object):
    def __init__(self, name: str = "MyWallet", version: str = "1.1", create_time: str = "", default_id: str = "",
                 default_address="", scrypt: Scrypt = None, identities: list = None, accounts: list = None):
        if scrypt is None:
            scrypt = Scrypt()
        if identities is None:
            identities = list()
        if accounts is None:
            accounts = list()
        self.name = name
        self.version = version
        self.create_time = create_time
        self.default_ont_id = default_id
        self.default_account_address = default_address
        self.scrypt = scrypt
        self.identities = identities
        self.accounts = accounts

    def clone(self):
        wallet = WalletData()
        wallet.name = self.name
        wallet.version = self.version
        wallet.create_time = self.create_time
        wallet.default_ont_id = self.default_ont_id
        wallet.default_account_address = self.default_account_address
        wallet.scrypt = self.scrypt
        wallet.accounts = self.accounts
        wallet.identities = self.identities
        return wallet

    def add_account(self, acc: AccountData):
        self.accounts.append(acc)

    def remove_account(self, address: str):
        account = self.get_account_by_address(address)
        if account is None:
            raise Exception("no the account")
        return self.accounts.remove(account)

    def get_accounts(self):
        return self.accounts

    def set_default_account_by_index(self, index: int):
        if index >= len(self.accounts):
            raise SDKException(ErrorCode.param_error)
        for acct in self.accounts:
            acct.is_default = False
        self.accounts[index].is_default = True
        self.default_account_address = self.accounts[index].address

    def set_default_account_by_address(self, b58_address: str):
        flag = True
        index = -1
        for acct in self.accounts:
            index += 1
            if acct.address == b58_address:
                flag = False
                break
        if flag:
            raise SDKException(ErrorCode.get_account_by_address_err)
        for acct in self.accounts:
            acct.is_default = False
        self.accounts[index].is_default = True
        self.default_account_address = b58_address

    def get_default_account_address(self):
        return self.default_account_address

    def get_default_account(self):
        for acct in self.accounts:
            if acct.is_default:
                return acct
        raise SDKException(ErrorCode.get_default_account_err)

    def get_account_by_index(self, index: int):
        if index < 0 or index >= len(self.accounts):
            return ValueError("wrong account index")
        return self.accounts[index]

    def get_account_by_address(self, address: str):
        for index in range(len(self.accounts)):
            if self.accounts[index].address == address:
                return self.accounts[index]
        return None

    def add_identity(self, id: Identity):
        for identity in self.identities:
            if identity.ont_id == id.ont_id:
                raise Exception("ont id is equal.")
        self.identities.append(id)

    def remove_identity(self, ont_id):
        for index in range(len(self.identities)):
            if self.identities[index].ont_id == ont_id:
                del self.identities[index]
                break
        raise SDKException(ErrorCode.param_error)

    def get_identity_by_ont_id(self, ont_id: str):
        for identity in self.identities:
            if identity.ont_id == ont_id:
                return identity
        return None
