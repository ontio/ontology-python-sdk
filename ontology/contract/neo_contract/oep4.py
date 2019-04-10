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
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class Oep4(object):
    def __init__(self, contract_address: str = '', sdk=None):
        self.__hex_contract_address = contract_address
        self.__sdk = sdk

    @property
    def hex_contract_address(self):
        return self.__hex_contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address: str):
        if not isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            raise SDKException(ErrorCode.require_str_params)
        self.__hex_contract_address = hex_contract_address

    def __new_token_setting_tx(self, func_name: str) -> InvokeTransaction:
        func = InvokeFunction(func_name)
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, func)
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
        response = self.__sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response.get('Result', ''))

    async def aio_name(self):
        """
        This interface is used to get the name of the token asynchronously. E.g. "DXToken".
        """
        tx = self.new_name_tx()
        response = await self.__sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
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
        response = self.__sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response.get('Result', ''))

    async def aio_symbol(self):
        """
        This interface is used to get the symbol of the token asynchronously. E.g. “DX”.
        """
        tx = self.new_symbol_tx()
        response = await self.__sdk.default_network.send_raw_transaction_pre_exec(tx)
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
        response = self.__sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_int(response.get('Result', ''))

    async def aio_decimals(self):
        """
        This interface is used to the number of decimals the token uses asynchronously.
        E.g. 8, means to divide the token amount by 100000000 to get its user representation.
        """
        tx = self.new_decimals_tx()
        response = await self.__sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        return Data.to_int(response.get('Result', ''))

    def new_total_supply_tx(self) -> InvokeTransaction:
        """
        This interface is used to generate transaction which can get the total token supply.
        """
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, InvokeFunction('totalSupply'))
        return tx

    def total_supply(self) -> int:
        """
        This interface is used to get the total token supply synchronously.
        """
        tx = self.new_total_supply_tx()
        response = self.__sdk.default_network.send_raw_transaction_pre_exec(tx)
        try:
            total_supply = Data.to_int(response['Result'])
        except SDKException:
            total_supply = 0
        return total_supply

    async def aio_total_supply(self) -> int:
        """
        This interface is used to get the total token supply asynchronously.
        """
        tx = self.new_total_supply_tx()
        response = await self.__sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
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
        tx.add_invoke_code(self.__hex_contract_address, InvokeFunction('init'))
        return tx

    def init(self, payer: Account, gas_price: int, gas_limit: int):
        tx = self.new_init_tx(payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(payer)
        tx_hash = self.__sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    async def aio_init(self, payer: Account, gas_price: int, gas_limit: int):
        tx = self.new_init_tx(payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(payer)
        tx_hash = await self.__sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    def new_balance_of_tx(self, owner: Union[str, Address]) -> InvokeTransaction:
        """
        This interface is used to generate transaction which can get the account balance of another account with owner address.
        """
        func = InvokeFunction('balanceOf')
        func.set_params_value(Address.b58decode(owner))
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def balance_of(self, owner: str) -> int:
        """
        This interface is used to get the account balance of another account with owner address synchronously.
        """
        tx = self.new_balance_of_tx(owner)
        result = self.__sdk.default_network.send_raw_transaction_pre_exec(tx)
        try:
            balance = Data.to_int(result['Result'])
        except SDKException:
            balance = 0
        return balance

    async def aio_balance_of(self, owner: Union[str, Address]) -> int:
        """
        This interface is used to get the account balance of another account with owner address asynchronously.
        """
        tx = self.new_balance_of_tx(owner)
        result = await self.__sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
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
        params = InvokeTransaction.generate_invoke_code(self.__hex_contract_address, func)
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
        tx_hash = self.__sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    async def aio_transfer(self, from_acct: Account, to_address: Union[str, Address], amount: int, payer: Account,
                           gas_price: int, gas_limit: int) -> str:
        """
        This interface is used to transfer amount of tokens to to_address synchronously.
        """
        tx = self.new_transfer_tx(from_acct.get_address(), to_address, amount, payer.get_address(), gas_price,
                                  gas_limit)
        tx.sign_transaction(from_acct)
        if from_acct.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = await self.__sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    def new_transfer_multi_tx(self, transfer_list: list, b58_payer_address: str, gas_limit: int,
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

    def transfer_multi(self):
        pass

    def query_transfer_event(self, tx_hash: str):
        event = self.__sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self.__hex_contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify

    async def aio_query_transfer_event(self, tx_hash: str):
        event = await self.__sdk.default_aio_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self.__hex_contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify

    def query_multi_transfer_event(self, tx_hash: str) -> list:
        event = self.__sdk.get_network().get_contract_event_by_tx_hash(tx_hash)
        notify_list = Event.get_notify_by_contract_address(event, self.__hex_contract_address)
        for index, notify in enumerate(notify_list):
            if notify.get('ContractAddress', '') == self.__hex_contract_address:
                notify_list[index]['States'][0] = Data.to_utf8_str(notify['States'][0])
                notify_list[index]['States'][1] = Data.to_b58_address(notify['States'][1])
                notify_list[index]['States'][2] = Data.to_b58_address(notify['States'][2])
                notify_list[index]['States'][3] = Data.to_int(notify['States'][3])
        return notify_list

    def query_approve_event(self, tx_hash: str):
        event = self.__sdk.get_network().get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self.__hex_contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify

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
