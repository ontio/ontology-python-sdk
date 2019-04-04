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

from ontology.common.address import Address
from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser
from ontology.utils.contract_event import ContractEventParser
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class Oep4(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__hex_contract_address = ''

    @property
    def hex_contract_address(self):
        return self.__hex_contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address: str):
        if not isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            raise SDKException(ErrorCode.require_str_params)
        self.__hex_contract_address = hex_contract_address

    def __token_setting(self, func_name: str) -> InvokeTransaction:
        func = InvokeFunction(func_name)
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def name(self) -> InvokeTransaction:
        """
        This interface is used to call the Name method in ope4
        that return the name of an oep4 token.

        :return: the string name of the oep4 token.
        """
        return self.__token_setting('name')

    def symbol(self) -> InvokeTransaction:
        """
        This interface is used to call the Symbol method in ope4
        that return the symbol of an oep4 token.

        :return: a short string symbol of the oep4 token
        """
        return self.__token_setting('symbol')

    def decimal(self) -> InvokeTransaction:
        """
        This interface is used to call the Decimal method in ope4
        that return the number of decimals used by the oep4 token.

        :return: the number of decimals used by the oep4 token.
        """
        return self.__token_setting('decimals')

    def init(self, b58_payer_address: str, gas_limit: int, gas_price: int) -> InvokeTransaction:
        """
        This interface is used to call the TotalSupply method in ope4
        that initialize smart contract parameter.
        """
        func = InvokeFunction('init')
        payer = Address.b58decode(b58_payer_address).to_bytes()
        tx = InvokeTransaction(payer, gas_price, gas_limit)
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def total_supply(self) -> InvokeTransaction:
        """
        This interface is used to call the TotalSupply method in ope4
        that return the total supply of the oep4 token.

        :return: the total supply of the oep4 token.
        """
        func = InvokeFunction('totalSupply')
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def balance_of(self, b58_address: str) -> InvokeTransaction:
        """
        This interface is used to call the BalanceOf method in ope4
        that query the ope4 token balance of the given base58 encode address.
        """
        func = InvokeFunction('balanceOf')
        address = Address.b58decode(b58_address).to_bytes()
        func.set_params_value(address)
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def transfer(self, from_acct: str or bytes or Account, b58_to_address: str, value: int, b58_payer_address: str,
                 gas_limit: int,
                 gas_price: int) -> InvokeTransaction:
        """
        This interface is used to call the Transfer method in ope4
        that transfer an amount of tokens from one account to another account.
        """
        func = InvokeFunction('transfer')
        if not isinstance(value, int):
            raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
        if value < 0:
            raise SDKException(ErrorCode.param_err('the value should be equal or great than 0.'))
        from_address = self.get_bytes_address(from_acct)
        to_address = self.get_bytes_address(b58_to_address)
        payer = Address.b58decode(b58_payer_address).to_bytes()
        func.set_params_value(from_address, to_address, value)
        params = InvokeTransaction.generate_invoke_code(self.__hex_contract_address, func)
        tx = InvokeTransaction(payer, gas_price, gas_limit, params)
        return tx

    def query_transfer_event(self, tx_hash: str):
        event = self.__sdk.get_network().get_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        notify = ContractDataParser.parse_addr_addr_int_notify(notify)
        return notify

    def query_multi_transfer_event(self, tx_hash: str) -> list:
        event = self.__sdk.get_network().get_contract_event_by_tx_hash(tx_hash)
        notify_list = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        for index, notify in enumerate(notify_list):
            if notify.get('ContractAddress', '') == self.__hex_contract_address:
                notify_list[index]['States'][0] = ContractDataParser.to_utf8_str(notify['States'][0])
                notify_list[index]['States'][1] = ContractDataParser.to_b58_address(notify['States'][1])
                notify_list[index]['States'][2] = ContractDataParser.to_b58_address(notify['States'][2])
                notify_list[index]['States'][3] = ContractDataParser.to_int(notify['States'][3])
        return notify_list

    def query_approve_event(self, tx_hash: str):
        event = self.__sdk.get_network().get_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        notify = ContractDataParser.parse_addr_addr_int_notify(notify)
        return notify

    def transfer_multi(self, transfer_list: list, b58_payer_address: str, gas_limit: int,
                       gas_price: int) -> InvokeTransaction:
        """
        This interface is used to call the TransferMulti method in ope4
        that allow transfer amount of token from multiple from-account to multiple to-account multiple times.
        """
        func = InvokeFunction('transferMulti')
        for index, item in enumerate(transfer_list):
            if not isinstance(item[2], int):
                raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
            if item[2] < 0:
                raise SDKException(ErrorCode.param_err('the value should be equal or great than 0.'))
            from_address_array = Address.b58decode(item[0]).to_bytes()
            to_address_array = Address.b58decode(item[1]).to_bytes()
            transfer_list[index] = [from_address_array, to_address_array, item[2]]
        for item in transfer_list:
            func.add_params_value(item)
        payer = Address.b58decode(b58_payer_address).to_bytes()
        params = InvokeTransaction.generate_invoke_code(self.__hex_contract_address, func)
        tx = InvokeTransaction(payer, gas_price, gas_limit, params)
        return tx

    def approve(self, owner: str or bytes or Account, b58_spender_address: str, amount: int,
                payer: str or bytes or Account, gas_limit: int, gas_price: int) -> InvokeTransaction:
        """
        This interface is used to call the Approve method in ope4
        that allows spender to withdraw a certain amount of oep4 token from owner account multiple times.

        If this function is called again, it will overwrite the current allowance with new value.
        """
        if not isinstance(amount, int):
            raise SDKException(ErrorCode.param_err('the data type of amount should be int.'))
        if amount < 0:
            raise SDKException(ErrorCode.param_err('the amount should be equal or great than 0.'))
        owner_address, spender_address, payer_address = self.get_bytes_address(owner, b58_spender_address, payer)
        func = InvokeFunction('approve')
        func.set_params_value(owner_address, spender_address, amount)
        params = InvokeTransaction.generate_invoke_code(self.__hex_contract_address, func)
        tx = InvokeTransaction(payer_address, gas_price, gas_limit, params)
        if isinstance(owner, Account):
            tx.sign_transaction(owner)
        if isinstance(payer, Account):
            tx.add_sign_transaction(payer)
        return tx

    def allowance(self, b58_owner_address: str, b58_spender_address: str) -> InvokeTransaction:
        """
        This interface is used to call the Allowance method in ope4
        that query the amount of spender still allowed to withdraw from owner account.
        """
        owner = self.get_bytes_address(b58_owner_address)
        spender = self.get_bytes_address(b58_spender_address)
        func = InvokeFunction('allowance')
        func.set_params_value(owner, spender)
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def transfer_from(self, b58_spender_address: str, b58_from_address: str, b58_to_address: str, value: int,
                      b58_payer_address: str, gas_limit: int, gas_price: int):
        """
        This interface is used to call the Allowance method in ope4
        that allow spender to withdraw amount of oep4 token from from-account to to-account.
        """
        func = InvokeFunction('transferFrom')
        spender = Address.b58decode(b58_spender_address).to_bytes()
        from_address = Address.b58decode(b58_from_address).to_bytes()
        to_address = Address.b58decode(b58_to_address).to_bytes()
        payer = Address.b58decode(b58_payer_address).to_bytes()
        if not isinstance(value, int):
            raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
        func.set_params_value(spender, from_address, to_address, value)
        tx = InvokeTransaction(payer, gas_price, gas_limit)
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx
