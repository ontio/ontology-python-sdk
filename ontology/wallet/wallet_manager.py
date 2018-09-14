#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import uuid
import base64
from datetime import datetime

from ontology.common.define import DID_ONT
from ontology.crypto.scrypt import Scrypt
from ontology.wallet.control import Control
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.utils.util import is_file_exist
from ontology.wallet.wallet import WalletData
from ontology.utils.util import get_random_str
from ontology.wallet.account import AccountData
from ontology.common.error_code import ErrorCode
from ontology.wallet.account_info import AccountInfo
from ontology.exception.exception import SDKException
from ontology.wallet.identity import Identity, did_ont
from ontology.wallet.identity_info import IdentityInfo
from ontology.crypto.signature_scheme import SignatureScheme


class WalletManager(object):
    def __init__(self, scheme=SignatureScheme.SHA256withECDSA):
        self.scheme = scheme
        self.wallet_file = WalletData()
        self.wallet_in_mem = WalletData()
        self.wallet_path = ""

    def open_wallet(self, wallet_path: str):
        self.wallet_path = wallet_path
        if is_file_exist(wallet_path) is False:
            # create a new wallet file
            self.wallet_in_mem.create_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.save()
        # wallet file exists now
        self.wallet_file = self.load()
        self.wallet_in_mem = self.wallet_file
        return self.wallet_file

    def load(self):
        with open(self.wallet_path, "r") as f:
            obj = json.load(f)
            try:
                create_time = obj['createTime']
            except KeyError:
                create_time = ''
            try:
                default_id = obj['defaultOntid']
            except KeyError:
                default_id = ''
            try:
                default_address = obj['defaultAccountAddress']
            except KeyError:
                default_address = ''
            try:
                identities = obj['identities']
            except KeyError:
                identities = list()
            try:
                wallet = WalletData(obj['name'], obj['version'], create_time, default_id, default_address,
                                    obj['scrypt'], identities, obj['accounts'])
            except KeyError as e:
                raise SDKException(ErrorCode.param_err('wallet file format error: %s.' % e))
        return wallet

    def save(self):
        with open(self.wallet_path, "w") as f:
            json.dump(self.wallet_in_mem, f, default=lambda obj: dict(obj), indent=4)

    def get_wallet(self):
        return self.wallet_in_mem

    def write_wallet(self):
        self.save()
        self.wallet_file = self.wallet_in_mem
        return self.wallet_file

    def reset_wallet(self):
        self.wallet_in_mem = self.wallet_file.clone()
        return self.wallet_in_mem

    def get_signature_scheme(self):
        return self.scheme

    def set_signature_scheme(self, scheme):
        self.scheme = scheme

    def import_identity(self, label: str, encrypted_pri_key: str, pwd: str, salt: str,
                        b58_address: str) -> Identity or None:
        """
        This interface is used to import identity by providing encrypted private key, password, salt and
        base58 encode address which should be correspond to the encrypted private key provided.

        :param label: a label for identity.
        :param encrypted_pri_key: an encrypted private key in base64 encoding from.
        :param pwd: a password which is used to encrypt and decrypt the private key.
        :param salt: a salt value which will be used in the process of encrypt private key.
        :param b58_address: a base58 encode address which correspond with the encrypted private key provided.
        :return: if succeed, an Identity object will be returned.
        """
        scrypt_n = Scrypt().get_n()
        pri_key = Account.get_gcm_decoded_private_key(encrypted_pri_key, pwd, b58_address, salt, scrypt_n, self.scheme)
        info = self.__create_identity(label, pwd, salt, pri_key)
        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ont_id == info.ont_id:
                return self.wallet_in_mem.identities[index]
        return None

    def create_identity(self, label: str, pwd: str) -> Identity:
        """

        :param label: a label for identity.
        :param pwd: a password which will be used to encrypt and decrypt the private key.
        :return: if succeed, an Identity object will be returned.
        """
        pri_key = get_random_str(64)
        salt = get_random_str(16)
        return self.__create_identity(label, pwd, salt, pri_key)

    def __create_identity(self, label: str, pwd: str, salt: str, private_key: str):
        acct = self.__create_account(label, pwd, salt, private_key, False)
        info = IdentityInfo()
        info.ont_id = did_ont + acct.get_address_base58()
        info.pubic_key = acct.serialize_public_key().hex()
        info.private_key = acct.serialize_private_key().hex()
        info.pri_key_wif = acct.export_wif()
        info.encrypted_pri_key = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        return self.wallet_in_mem.get_identity_by_ont_id(info.ont_id)

    def create_identity_from_pri_key(self, label: str, pwd: str, private_key: str) -> Identity:
        """
        This interface is used to create identity based on given label, password and private key.

        :param label: a label for identity.
        :param pwd: a password which will be used to encrypt and decrypt the private key.
        :param private_key: a private key in the form of string.
        :return: if succeed, an Identity object will be returned.
        """
        salt = get_random_str(16)
        identity = self.__create_identity(label, pwd, salt, private_key)
        return identity

    def create_account(self, label: str, pwd: str) -> AccountData:
        """
        This interface is used to create account based on given password and label.

        :param label: a label for account.
        :param pwd: a password which will be used to encrypt and decrypt the private key
        :return: if succeed, return an data structure which contain the information of a wallet account.
        """
        pri_key = get_random_str(64)
        salt = get_random_str(16)
        account = self.__create_account(label, pwd, salt, pri_key, True)
        return self.wallet_in_mem.get_account_by_address(account.get_address_base58())

    def __create_account(self, label: str, pwd: str, salt: str, private_key: str, account_flag: bool):
        account = Account(private_key, self.scheme)
        # initialization
        if self.scheme == SignatureScheme.SHA256withECDSA:
            acct = AccountData()
        else:
            raise ValueError("scheme type is error")
        # set key
        if pwd is not None:
            acct.key = account.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        else:
            acct.key = account.serialize_private_key().hex()

        acct.address = account.get_address_base58()
        # set label
        if label is None or label == "":
            label = str(uuid.uuid4())[0:8]
        if account_flag:
            for index in range(len(self.wallet_in_mem.accounts)):
                if acct.address == self.wallet_in_mem.accounts[index].address:
                    raise ValueError("wallet account exists")

            if len(self.wallet_in_mem.accounts) == 0:
                acct.is_default = True
                self.wallet_in_mem.default_account_address = acct.address
            acct.label = label
            acct.salt = base64.b64encode(salt.encode()).decode('ascii')
            acct.public_key = account.serialize_public_key().hex()
            self.wallet_in_mem.accounts.append(acct)
        else:
            for index in range(len(self.wallet_in_mem.identities)):
                if self.wallet_in_mem.identities[index].ont_id == did_ont + acct.address:
                    raise ValueError("wallet identity exists")
            idt = Identity()
            idt.ont_id = did_ont + acct.address
            idt.label = label
            if len(self.wallet_in_mem.identities) == 0:
                idt.is_default = True
                self.wallet_in_mem.default_ont_id = idt.ont_id
            ctl = Control(id="keys-1", key=acct.key, salt=base64.b64encode(salt.encode()).decode('ascii'),
                          address=acct.address,
                          public_key=account.serialize_public_key().hex())
            idt.controls.append(ctl)
            self.wallet_in_mem.identities.append(idt)
        return account

    def import_account(self, label: str, encrypted_pri_key: str, pwd: str, base58_address: str,
                       base64_salt: str) -> AccountData or None:
        """
        This interface is used to import account by providing account data.

        :param label: str, wallet label
        :param encrypted_pri_key: str, an encrypted private key in base64 encoding from
        :param pwd: str, a password which is used to encrypt and decrypt the private key
        :param base58_address: str, a base58 encode  wallet address value
        :param base64_salt: str, a base64 encode salt value which is used in the encryption of private key
        :return:
            if succeed, return an data structure which contain the information of a wallet account.
            if failed, return a None object.
        """
        salt = base64.b64decode(base64_salt.encode('ascii')).decode('latin-1')
        private_key = Account.get_gcm_decoded_private_key(encrypted_pri_key, pwd, base58_address, salt,
                                                          Scrypt().get_n(),
                                                          self.scheme)
        info = self.create_account_info(label, pwd, salt, private_key)
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].address:
                return self.wallet_in_mem.accounts[index]
        return None

    def create_account_info(self, label: str, pwd: str, salt: str, private_key: str) -> AccountInfo:
        acct = self.__create_account(label, pwd, salt, private_key, True)
        info = AccountInfo()
        info.address_base58 = Address.address_from_bytes_pubkey(acct.serialize_public_key()).b58encode()
        info.public_key = acct.serialize_public_key().hex()
        info.encrypted_pri_key = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        info.salt = salt
        return info

    def create_account_from_private_key(self, label: str, password: str, private_key: str) -> AccountData or None:
        """
        This interface is used to create account by providing an encrypted private key and it's decrypt password.

        :param label: a label for account.
        :param password: a password which is used to decrypt the encrypted private key.
        :param private_key: a private key in the form of string.
        :return: if succeed, return an AccountData object.
                  if failed, return a None object.
        """
        salt = get_random_str(16)
        info = self.create_account_info(label, password, salt, private_key)
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].address:
                return self.wallet_in_mem.accounts[index]
        return None


    def get_account(self, b58_address_or_ontid: str, pwd: str) -> Account or None:
      """
        :param b58_address_or_ontid: a base58 encode address or ontid
        :param password: a password which is used to decrypt the encrypted private key.
        :return:
        """
        if address_or_ontid.startswith(DID_ONT):
            for index in range(len(self.wallet_in_mem.identities)):
                if self.wallet_in_mem.identities[index].ont_id == address_or_ontid:
                    addr = self.wallet_in_mem.identities[index].ont_id.replace(did_ont, "")
                    key = self.wallet_in_mem.identities[index].controls[0].key
                    salt = base64.b64decode(self.wallet_in_mem.identities[index].controls[0].salt)
                    private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(),
                                                                      self.scheme)
                    return Account(private_key, self.scheme)
        else:
            for index in range(len(self.wallet_in_mem.accounts)):
                if self.wallet_in_mem.accounts[index].address == address_or_ontid:
                    key = self.wallet_in_mem.accounts[index].key
                    addr = self.wallet_in_mem.accounts[index].address
                    salt = base64.b64decode(self.wallet_in_mem.accounts[index].salt)
                    private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.scheme)
                    return Account(private_key, self.scheme)
        return None

    def get_default_identity(self) -> Identity:
        for identity in self.wallet_in_mem.identities:
            if identity.is_default:
                return identity
        raise SDKException(ErrorCode.param_error)

    def get_default_account(self) -> AccountData:
        """
        This interface is used to get the default account in WalletManager.

        :return: an AccountData object that contain all the information of a default account.
        """
        for acct in self.wallet_in_mem.accounts:
            if acct.is_default:
                return acct
        raise SDKException(ErrorCode.get_default_account_err)
