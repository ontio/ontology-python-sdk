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

from ontology.common.address import Address
from ontology.utils.contract import Data
from ontology.account.account import Account
from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.vm.build_vm import build_native_invoke_code
from ontology.core.invoke_transaction import InvokeTransaction


class Asset(object):
    def __init__(self, sdk):
        self._sdk = sdk
        self._version = b'\x00'
        self._contract_address = b''
        self._invoke_address = b''

    @property
    def contract_address(self) -> Address:
        return Address(self._contract_address)

    def _new_token_setting_tx(self, func_name: str) -> InvokeTransaction:
        invoke_code = build_native_invoke_code(self._invoke_address, self._version, func_name, bytearray())
        return InvokeTransaction(payload=invoke_code)

    def new_name_tx(self) -> InvokeTransaction:
        return self._new_token_setting_tx('name')

    def new_symbol_tx(self) -> InvokeTransaction:
        return self._new_token_setting_tx('symbol')

    def new_decimals_tx(self) -> InvokeTransaction:
        return self._new_token_setting_tx('decimals')

    def new_balance_of_tx(self, owner: Union[str, Address]) -> InvokeTransaction:
        owner = Address.b58decode(owner)
        invoke_code = build_native_invoke_code(self._invoke_address, self._version, 'balanceOf', owner)
        return InvokeTransaction(payload=invoke_code)

    def new_allowance_tx(self, from_address: Union[str, Address], to_address: Union[str, Address]) -> InvokeTransaction:
        args = dict(from_address=Address.b58decode(from_address), to_address=Address.b58decode(to_address))
        invoke_code = build_native_invoke_code(self._invoke_address, self._version, 'allowance', args)
        return InvokeTransaction(payload=invoke_code)

    def new_transfer_tx(self, from_address: Union[str, Address], to_address: Union[str, Address], amount: int,
                        payer: Union[str, Address], gas_price: int, gas_limit: int) -> Transaction:
        """
        This interface is used to generate a Transaction object for transfer.
        """
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        state = [{'from': Address.b58decode(from_address), 'to': Address.b58decode(to_address), 'amount': amount}]
        invoke_code = build_native_invoke_code(self._invoke_address, self._version, 'transfer', state)
        return InvokeTransaction(Address.b58decode(payer), gas_price, gas_limit, invoke_code)

    def new_approve_tx(self, approver: Union[str, Address], spender: Union[str, Address], amount: int,
                       payer: Union[str, Address], gas_price: int, gas_limit: int) -> Transaction:
        """
        This interface is used to generate a Transaction object for approve.
        """
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        args = dict(sender=Address.b58decode(approver), receiver=Address.b58decode(spender), amount=amount)
        invoke_code = build_native_invoke_code(self._invoke_address, self._version, 'approve', args)
        return InvokeTransaction(Address.b58decode(payer), gas_price, gas_limit, invoke_code)

    def new_transfer_from_tx(self, spender: Union[str, Address], from_address: Union[str, Address],
                             receiver: Union[str, Address], amount: int, payer: Union[str, Address], gas_price: int,
                             gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a Transaction object that allow one account to transfer
        a amount of ONT or ONG Asset to another account, in the condition of the first account had been approved.
        """
        args = dict(spender=Address.b58decode(spender), from_address=Address.b58decode(from_address),
                    to_address=Address.b58decode(receiver), amount=amount)
        invoke_code = build_native_invoke_code(self._invoke_address, self._version, 'transferFrom', args)
        return InvokeTransaction(Address.b58decode(payer), gas_price, gas_limit, invoke_code)

    def name(self) -> str:
        """
        This interface is used to query the asset's name of ONT or ONG.
        """
        tx = self.new_name_tx()
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response['Result'])

    def symbol(self) -> str:
        """
        This interface is used to query the asset's symbol of ONT or ONG.
        """
        tx = self.new_symbol_tx()
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response['Result'])

    def decimals(self) -> int:
        """
        This interface is used to query the asset's decimals of ONT or ONG.
        """
        tx = self.new_decimals_tx()
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        try:
            decimal = Data.to_int(response['Result'])
            return decimal
        except SDKException:
            return 0

    def balance_of(self, owner: Union[str, Address]) -> int:
        """
        This interface is used to query the account's ONT or ONG balance.
        """
        tx = self.new_balance_of_tx(owner)
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        try:
            balance = Data.to_int(response['Result'])
            return balance
        except SDKException:
            return 0

    def allowance(self, from_address: Union[str, Address], to_address: Union[str, Address]) -> int:
        tx = self.new_allowance_tx(from_address, to_address)
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        try:
            allowance = Data.to_int(response['Result'])
            return allowance
        except SDKException:
            return 0

    def transfer(self, from_acct: Account, to_address: Union[str, Address], amount: int, payer: Account, gas_price: int,
                 gas_limit: int):
        """
        This interface is used to send a transfer transaction that only for ONT or ONG.
        """
        tx = self.new_transfer_tx(from_acct.get_address(), to_address, amount, payer.get_address(), gas_price,
                                  gas_limit)
        tx.sign_transaction(from_acct)
        if from_acct.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        return self._sdk.default_network.send_raw_transaction(tx)

    def approve(self, approver: Account, spender: Union[str, Address], amount: int, payer: Account, gas_price: int,
                gas_limit: int) -> str:
        """
        This is an interface used to send an approve transaction
        which allow receiver to spend a amount of ONT or ONG asset in sender's account.
        """
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        tx = self.new_approve_tx(approver.get_address(), spender, amount, payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(approver)
        if approver.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        return self._sdk.default_network.send_raw_transaction(tx)

    def transfer_from(self, spender: Account, from_address: Union[str, Address], receiver: Union[str, Address],
                      amount: int, payer: Account, gas_price: int, gas_limit: int) -> str:
        """
        This interface is used to generate a Transaction object for transfer that  allow one account to
        transfer a amount of ONT or ONG Asset to another account, in the condition of the first account had approved.
        """
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        tx = self.new_transfer_from_tx(spender.get_address(), from_address, receiver, amount, payer.get_address(),
                                       gas_price, gas_limit)
        tx.sign_transaction(spender)
        if spender.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        return self._sdk.default_network.send_raw_transaction(tx)
