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

from typing import Union

from ontology.utils.contract import Data
from ontology.utils.contract import Event
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.contract.neo.invoke_function import InvokeFunction


class Oep4(object):
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

    def new_decimals_tx(self) -> InvokeTransaction:
        """
        This interface is used to generate transaction which can get the number of decimals the token uses.
        """
        return self.__new_token_setting_tx('decimals')

    def decimals(self):
        """
        This interface is used to the number of decimals the token uses synchronously.
        E.g. 8, means to divide the token amount by 100000000 to get its user representation.
        """
        tx = self.new_decimals_tx()
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_int(response.get('Result', ''))

    def new_total_supply_tx(self) -> InvokeTransaction:
        """
        This interface is used to generate transaction which can get the total token supply.
        """
        tx = InvokeTransaction()
        tx.add_invoke_code(self._contract_address, InvokeFunction('totalSupply'))
        return tx

    def total_supply(self) -> int:
        """
        This interface is used to get the total token supply synchronously.
        """
        tx = self.new_total_supply_tx()
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        try:
            total_supply = Data.to_int(response['Result'])
        except SDKException:
            total_supply = 0
        return total_supply

    def new_init_tx(self, payer: Union[str, bytes, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to call the TotalSupply method in ope4
        that initialize smart contract parameter.
        """
        tx = InvokeTransaction(payer, gas_price, gas_limit)
        tx.add_invoke_code(self._contract_address, InvokeFunction('init'))
        return tx

    def init(self, founder: Account, payer: Account, gas_price: int, gas_limit: int):
        tx = self.new_init_tx(payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(founder)
        if founder.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

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

    def new_transfer_tx(self, from_address: Union[str, Address], to_address: Union[str, Address], amount: int,
                        payer: Union[str, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a transaction which can transfer amount of tokens to to_address.
        """
        func = InvokeFunction('transfer')
        func.set_params_value(Address.b58decode(from_address), Address.b58decode(to_address), amount)
        params = InvokeTransaction.generate_invoke_code(self._contract_address, func)
        tx = InvokeTransaction(payer, gas_price, gas_limit, params)
        return tx

    def transfer(self, from_acct: Account, to_address: Union[str, Address], amount: int, payer: Account, gas_price: int,
                 gas_limit: int) -> str:
        """
        This interface is used to transfer amount of tokens to to_address synchronously.
        """
        tx = self.new_transfer_tx(from_acct.get_address(), to_address, amount, payer.get_address(), gas_price,
                                  gas_limit)
        tx.sign_transaction(from_acct)
        if from_acct.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    def new_transfer_multi_tx(self, transfer_list: list, payer: Union[str, bytes, Address], gas_price: int,
                              gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a transaction which can
        transfer amount of token from from-account to to-account multiple times.
        """
        func = InvokeFunction('transferMulti')
        for index, item in enumerate(transfer_list):
            if not isinstance(item[2], int):
                raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
            if item[2] < 0:
                raise SDKException(ErrorCode.param_err('the value should be equal or great than 0.'))
            transfer_list[index] = [Address.b58decode(item[0]), Address.b58decode(item[1]), item[2]]
        for item in transfer_list:
            func.add_params_value(item)
        params = InvokeTransaction.generate_invoke_code(self._contract_address, func)
        tx = InvokeTransaction(payer, gas_price, gas_limit, params)
        return tx

    def transfer_multi(self, transfer_list: list, signers: list, payer_acct: Account, gas_price: int,
                       gas_limit: int) -> str:
        """
        This interface is used to transfer amount of token from from-account to to-account multiple times synchronously.
        """
        tx = self.new_transfer_multi_tx(transfer_list, payer_acct.get_address(), gas_price, gas_limit)
        tx.sign_transaction(payer_acct)
        for signer in signers:
            tx.add_sign_transaction(signer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    def new_approve_tx(self, owner: Union[str, bytes, Address], spender: Union[str, bytes, Address], amount: int,
                       payer: Union[str, bytes, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a transaction which allows spender to
        withdraw from owner account multiple times, up to the _value amount.
        If this function is called again it overwrites the current allowance with amount value.
        """
        if not isinstance(amount, int):
            raise SDKException(ErrorCode.param_err('the data type of amount should be int.'))
        if amount < 0:
            raise SDKException(ErrorCode.param_err('the amount should be equal or great than 0.'))
        func = InvokeFunction('approve')
        func.set_params_value(Address.b58decode(owner), Address.b58decode(spender), amount)
        params = InvokeTransaction.generate_invoke_code(self._contract_address, func)
        tx = InvokeTransaction(payer, gas_price, gas_limit, params)
        return tx

    def approve(self, owner: Account, spender: Union[str, bytes, Address], amount: int, payer: Account, gas_price: int,
                gas_limit: int) -> str:
        """
        This interface is used to allow spender to withdraw from owner account multiple times, up to the _value amount.
        If this function is called again it overwrites the current allowance with amount value.
        """
        tx = self.new_approve_tx(owner.get_address(), spender, amount, payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(owner)
        if owner.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    def query_transfer_event(self, tx_hash: str):
        event = self._sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self._contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify

    def _parse_multi_transfer_event(self, event: dict):
        notify_list = Event.get_notify_by_contract_address(event, self._contract_address)
        for index, notify in enumerate(notify_list):
            if notify.get('ContractAddress', '') == self._contract_address:
                notify_list[index] = Data.parse_addr_addr_int_notify(notify_list[index])
        return notify_list

    def query_multi_transfer_event(self, tx_hash: str) -> list:
        event = self._sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        return self._parse_multi_transfer_event(event)

    def query_approve_event(self, tx_hash: str):
        event = self._sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self._contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify

    def new_allowance_tx(self, owner: Union[str, bytes, Address],
                         spender: Union[str, bytes, Address]) -> InvokeTransaction:
        func = InvokeFunction('allowance')
        func.set_params_value(Address.b58decode(owner), Address.b58decode(spender))
        tx = InvokeTransaction()
        tx.add_invoke_code(self._contract_address, func)
        return tx

    def allowance(self, owner: Union[str, bytes, Address], spender: Union[str, bytes, Address]) -> int:
        tx = self.new_allowance_tx(owner, spender)
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        result = response.get('Result')
        if len(result) == 0:
            return 0
        return int(result, base=16)

    def new_transfer_from_tx(self, spender: Union[str, bytes, Address], owner: Union[str, bytes, Address],
                             to_address: Union[str, bytes, Address], value: int, payer: Union[str, bytes, Address],
                             gas_price: int, gas_limit: int) -> InvokeTransaction:
        func = InvokeFunction('transferFrom')
        if not isinstance(value, int):
            raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
        func.set_params_value(Address.b58decode(spender), Address.b58decode(owner), Address.b58decode(to_address),
                              value)
        tx = InvokeTransaction(payer, gas_price, gas_limit)
        tx.add_invoke_code(self._contract_address, func)
        return tx

    def transfer_from(self, spender: Account, owner: Union[str, bytes, Address], to_address: Union[str, bytes, Address],
                      value: int, payer: Account, gas_price: int, gas_limit: int) -> str:
        tx = self.new_transfer_from_tx(spender.get_address(), owner, to_address, value, payer.get_address(), gas_price,
                                       gas_limit)
        tx.sign_transaction(spender)
        if spender.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    def query_transfer_from_event(self, tx_hash: str):
        event = self._sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self._contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify
