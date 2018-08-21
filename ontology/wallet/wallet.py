#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from ontology.crypto.scrypt import Scrypt
from ontology.wallet.control import Control
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
        self.identities = list()
        self.accounts = list()
        for index in range(len(identities)):
            dict_identity = identities[index]
            if isinstance(dict_identity, dict):
                list_controls = list()
                try:
                    for control_data in dict_identity['controls']:
                        list_controls.append(Control.dict2obj(control_data))
                    identity = Identity(ont_id=dict_identity['ontid'], label=dict_identity['label'],
                                        lock=dict_identity['lock'], controls=list_controls,
                                        is_default=dict_identity['isDefault'])
                except KeyError:
                    raise SDKException(ErrorCode.param_error)
                self.identities.append(identity)
            else:
                self.identities = identities
                break
        for index in range(len(accounts)):
            dict_account = accounts[index]
            if isinstance(dict_account, dict):
                try:
                    public_key = dict_account['publicKey']
                except KeyError:
                    public_key = ''
                try:
                    acct = AccountData(address=dict_account['address'], enc_alg=dict_account['enc-alg'],
                                       key=dict_account['key'], algorithm=dict_account['algorithm'],
                                       salt=dict_account['salt'], param=dict_account['parameters'],
                                       label=dict_account['label'], public_key=public_key,
                                       sign_scheme=dict_account['signatureScheme'],
                                       is_default=dict_account['isDefault'], lock=dict_account['lock'])
                except KeyError:
                    raise SDKException(ErrorCode.param_error)
                self.accounts.append(acct)
            else:
                self.accounts = accounts
                break

    def __iter__(self):
        data = dict()
        data['name'] = self.name
        data['version'] = self.version
        data['createTime'] = self.create_time
        data['defaultOntid'] = self.default_ont_id
        data['defaultAccountAddress'] = self.default_account_address
        data['scrypt'] = self.scrypt
        data['identities'] = self.identities
        data['accounts'] = self.accounts
        for key, value in data.items():
            yield (key, value)

    def clone(self):
        wallet = WalletData()
        wallet.name = self.name
        wallet.version = self.version
        wallet.create_time = self.create_time
        wallet.default_ont_id = self.default_ont_id
        wallet.default_account_address = self.default_account_address
        wallet.scrypt = self.scrypt
        wallet.accounts = self.accounts
        wallet.set_identities(self.identities)
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
        for i in range(len(self.accounts)):
            self.accounts[i].is_default = False
        self.accounts[index].is_default = True
        self.default_account_address = b58_address

    def get_default_account_address(self):
        return self.default_account_address

    def get_account_by_index(self, index: int):
        if index < 0 or index >= len(self.accounts):
            return ValueError("wrong account index")
        return self.accounts[index]

    def get_account_by_address(self, address: str):
        for index in range(len(self.accounts)):
            if self.accounts[index].address == address:
                return self.accounts[index]
        return None

    def set_identities(self, identities: list):
        if not isinstance(identities, list):
            raise SDKException(ErrorCode.param_error)
        self.identities = identities

    def get_identities(self) -> list:
        return self.identities

    def clear_identities(self):
        self.identities = list()

    def add_identity(self, id: Identity):
        for identity in self.identities:
            if identity.ont_id == id.ont_id:
                raise Exception("ont id is equal.")
        self.identities.append(id)

    def remove_identity(self, ont_id):
        for index in range(len(self.identities)):
            if self.identities[index].ont_id == ont_id:
                del self.identities[index]
                return
        raise SDKException(ErrorCode.param_error)

    def get_identity_by_ont_id(self, ont_id: str) -> Identity or None:
        for identity in self.identities:
            if identity.ont_id == ont_id:
                return identity
        return None

    def set_default_identity_by_index(self, index: int):
        identities_len = len(self.identities)
        if index >= identities_len:
            raise SDKException(ErrorCode.param_error)
        for i in range(identities_len):
            self.identities[i].is_default = False
            if i == index:
                self.identities[index].is_default = True

    def set_default_identity_by_ont_id(self, ont_id: str):
        flag = True
        for identity in self.identities:
            if identity.ont_id == ont_id:
                identity.is_default = True
                flag = False
            else:
                identity.is_default = False
        if flag:
            raise SDKException(ErrorCode.param_error)
