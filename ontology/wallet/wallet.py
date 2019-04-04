"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import List

from ontology.crypto.scrypt import Scrypt
from ontology.common.define import DID_ONT
from ontology.wallet.control import Control
from ontology.wallet.identity import Identity
from ontology.wallet.account import AccountData
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class WalletData(object):
    def __init__(self, name: str = 'MyWallet', version: str = '1.1', create_time: str = '', default_id: str = '',
                 default_address='', scrypt: Scrypt = Scrypt(), identities: List[Identity] = None,
                 accounts: List[AccountData] = None):
        if not isinstance(scrypt, Scrypt):
            raise SDKException(ErrorCode.other_error('Wallet Data init failed'))
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
        for dict_identity in identities:
            if isinstance(dict_identity, dict):
                list_controls = list()
                is_default = dict_identity.get('isDefault', False)
                for ctrl_data in dict_identity['controls']:
                    hash_value = ctrl_data.get('hash', 'sha256')
                    public_key = ctrl_data.get('publicKey', '')
                    try:
                        ctrl = Control(kid=ctrl_data['id'], address=ctrl_data['address'], enc_alg=ctrl_data['enc-alg'],
                                       key=ctrl_data['key'], algorithm=ctrl_data['algorithm'], salt=ctrl_data['salt'],
                                       param=ctrl_data['parameters'], hash_value=hash_value, public_key=public_key)
                    except KeyError:
                        raise SDKException(ErrorCode.other_error('invalid parameters.'))
                    list_controls.append(ctrl)
                try:
                    identity = Identity(ont_id=dict_identity['ontid'], label=dict_identity['label'],
                                        lock=dict_identity['lock'], controls=list_controls, is_default=is_default)
                except KeyError:
                    raise SDKException(ErrorCode.other_error('invalid parameters.'))
                self.identities.append(identity)
            else:
                self.identities = identities
                break
        for dict_account in accounts:
            if isinstance(dict_account, dict):
                try:
                    public_key = dict_account['publicKey']
                except KeyError:
                    public_key = ''
                try:
                    acct = AccountData(b58_address=dict_account['address'], enc_alg=dict_account['enc-alg'],
                                       key=dict_account['key'], algorithm=dict_account['algorithm'],
                                       salt=dict_account['salt'], param=dict_account['parameters'],
                                       label=dict_account['label'], public_key=public_key,
                                       sig_scheme=dict_account['signatureScheme'],
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
        data['scrypt'] = dict(self.scrypt)
        data['identities'] = list()
        for identity in self.identities:
            data['identities'].append(dict(identity))
        data['accounts'] = list()
        for acct in self.accounts:
            data['accounts'].append(dict(acct))
        for key, value in data.items():
            yield (key, value)

    def add_account(self, acct: AccountData):
        """
        This interface is used to add account into WalletData.

        :param acct: an AccountData object.
        """
        self.accounts.append(acct)

    def remove_account(self, address: str):
        """
        This interface is used to remove account from WalletData.

        :param address: a string address.
        """
        account = self.get_account_by_b58_address(address)
        if account is None:
            raise SDKException(ErrorCode.get_account_by_address_err)
        self.accounts.remove(account)

    def get_accounts(self) -> List[AccountData]:
        """
        This interface is used to get all the account information in WalletManager.

        :return: an AccountData list which contain all the account information in WalletManager
        """
        return self.accounts

    def set_default_account_by_index(self, index: int):
        """
        This interface is used to set default account by given index.

        :param index: an int value that indicate the account object in account list.
        """
        if index >= len(self.accounts):
            raise SDKException(ErrorCode.param_error)
        for acct in self.accounts:
            acct.is_default = False
        self.accounts[index].is_default = True
        self.default_account_address = self.accounts[index].b58_address

    def set_default_account_by_address(self, b58_address: str):
        """
        This interface is used to set default account by given base58 encode address.

        :param b58_address: a base58 encode address.
        """
        flag = True
        index = -1
        for acct in self.accounts:
            index += 1
            if acct.b58_address == b58_address:
                flag = False
                break
        if flag:
            raise SDKException(ErrorCode.get_account_by_address_err)
        for i in range(len(self.accounts)):
            self.accounts[i].is_default = False
        self.accounts[index].is_default = True
        self.default_account_address = b58_address

    def get_default_account_address(self) -> str:
        """
        This interface is used to get the default account's base58 encode address in WalletManager.

        :return:
        """
        return self.default_account_address

    def get_account_by_index(self, index: int):
        if index < 0 or index >= len(self.accounts):
            raise SDKException(ErrorCode.get_account_by_index_err)
        return self.accounts[index]

    def get_account_by_b58_address(self, b58_address: str) -> AccountData:
        for acct in self.accounts:
            if acct.b58_address == b58_address:
                return acct
        raise SDKException(ErrorCode.other_error('Get account failed.'))

    def set_identities(self, identities: list):
        if not isinstance(identities, list):
            raise SDKException(ErrorCode.param_error)
        self.identities = identities

    def get_identities(self) -> list:
        return self.identities

    def clear_identities(self):
        self.identities = list()

    def add_identity(self, identity: Identity):
        for item in self.identities:
            if item.ont_id == identity.ont_id:
                raise SDKException(ErrorCode.other_error('add identity failed, OntId conflict.'))
        self.identities.append(identity)

    def __create_identity(self, ont_id: str):
        for item in self.identities:
            if item.ont_id == ont_id:
                return item
        identity = Identity(ont_id=ont_id)
        self.identities.append(identity)
        return identity

    def add_controller(self, ont_id: str, key: str, kid: int, pub_key: str):
        if not isinstance(ont_id, str):
            raise SDKException(ErrorCode.require_str_params)
        if not ont_id.startswith(DID_ONT):
            raise SDKException(ErrorCode.invalid_ont_id_format(ont_id))
        if not isinstance(kid, int):
            raise SDKException(ErrorCode.require_int_params)
        if not isinstance(pub_key, str):
            raise SDKException(ErrorCode.require_str_params)
        try:
            identity = self.get_identity_by_ont_id(ont_id)
        except SDKException:
            identity = self.__create_identity(ont_id)
        for ctrl in identity.controls:
            if ctrl.key == key:
                return identity
        ctrl = Control(key=key, kid=f'keys-{kid}', public_key=pub_key)
        identity.add_control(ctrl)
        return identity

    def remove_identity(self, ont_id):
        for identity in self.identities:
            if identity.ont_id == ont_id:
                self.identities.remove(identity)
                return
        raise SDKException(ErrorCode.param_error)

    def get_identity_by_ont_id(self, ont_id: str) -> Identity:
        for identity in self.identities:
            if identity.ont_id == ont_id:
                return identity
        raise SDKException(ErrorCode.other_error('Get identity failed.'))

    def set_default_identity_by_index(self, index: int):
        """
        This interface is used to set default account by given an index value.

        :param index: an int value that indicate the position of an account object in account list.
        """
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
