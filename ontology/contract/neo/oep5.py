"""
Copyright (C) 2018-2019 The ontology Authors
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
from typing import Union

from ontology.utils.contract import Data
from ontology.common.address import Address
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.contract.neo.invoke_function import InvokeFunction


class Oep5(object):
    def __init__(self, hex_contract_address: str = '', sdk=None):
        self._contract_address = hex_contract_address
        self._sdk = sdk

    @property
    def hex_contract_address(self):
        return self._contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address: str):
        if not isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            raise SDKException(ErrorCode.require_str_params)
        hex_contract_address.replace(' ', '')
        self._contract_address = hex_contract_address

    def __new_token_setting_tx(self, func_name: str) -> InvokeTransaction:
        func = InvokeFunction(func_name)
        tx = InvokeTransaction()
        tx.add_invoke_code(self._contract_address, func)
        return tx

    def new_name_tx(self) -> InvokeTransaction:
        """
        This interface is used to generate transaction which can get the name of the token.
        """
        return self.__new_token_setting_tx('name')

    def name(self):
        """
        This interface is used to get the name of the token synchronously. E.g. "DXToken".
        """
        tx = self.new_name_tx()
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response.get('Result', ''))

    def new_symbol_tx(self) -> InvokeTransaction:
        """
        This interface is used to generate transaction which can get the symbol of the token.
        """
        return self.__new_token_setting_tx('symbol')

    def symbol(self):
        """
        This interface is used to get the symbol of the token synchronously. E.g. “DX”.
        """
        tx = self.new_symbol_tx()
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response.get('Result', ''))

    def new_balance_of_tx(self, owner: Union[str, bytes, Address]) -> InvokeTransaction:
        """
        This interface is used to generate transaction which can get the account balance of another account with owner address.
        """
        func = InvokeFunction('balanceOf')
        func.set_params_value(Address.b58decode(owner))
        tx = InvokeTransaction()
        tx.add_invoke_code(self._contract_address, func)
        return tx

    def balance_of(self, owner: str) -> int:
        """
        This interface is used to get the account balance of another account with owner address synchronously.
        """
        tx = self.new_balance_of_tx(owner)
        result = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        try:
            balance = Data.to_int(result['Result'])
        except SDKException:
            balance = 0
        return balance
