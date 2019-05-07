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
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.contract.native.asset import Asset


class AioAsset(Asset):
    def __init__(self, sdk):
        super().__init__(sdk)

    async def name(self) -> str:
        """
        This interface is used to query the asset's name of ONT or ONG.
        """
        tx = self.new_name_tx()
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response['Result'])

    async def symbol(self) -> str:
        """
        This interface is used to query the asset's symbol of ONT or ONG.
        """
        tx = self.new_symbol_tx()
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response['Result'])

    async def decimals(self) -> int:
        """
        This interface is used to query the asset's decimals of ONT or ONG.
        """
        tx = self.new_decimals_tx()
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        try:
            decimal = Data.to_int(response['Result'])
            return decimal
        except SDKException:
            return 0

    async def balance_of(self, owner: Union[str, Address]) -> int:
        """
        This interface is used to query the account's ONT or ONG balance.
        """
        tx = self.new_balance_of_tx(owner)
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        try:
            balance = Data.to_int(response['Result'])
            return balance
        except SDKException:
            return 0

    async def allowance(self, from_address: Union[str, Address], to_address: Union[str, Address]) -> int:
        tx = self.new_allowance_tx(from_address, to_address)
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        try:
            allowance = Data.to_int(response['Result'])
            return allowance
        except SDKException:
            return 0

    async def transfer(self, from_acct: Account, to_address: Union[str, Address], amount: int, payer: Account,
                       gas_price: int, gas_limit: int):
        """
        This interface is used to send a transfer transaction that only for ONT or ONG.
        """
        tx = self.new_transfer_tx(from_acct.get_address(), to_address, amount, payer.get_address(), gas_price,
                                  gas_limit)
        tx.sign_transaction(from_acct)
        if from_acct.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        return await self._sdk.default_aio_network.send_raw_transaction(tx)

    async def approve(self, approver: Account, spender: Union[str, Address], amount: int, payer: Account,
                      gas_price: int, gas_limit: int) -> str:
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
        return await self._sdk.default_aio_network.send_raw_transaction(tx)

    async def transfer_from(self, spender: Account, from_address: Union[str, Address], receiver: Union[str, Address],
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
        return await self._sdk.default_aio_network.send_raw_transaction(tx)
