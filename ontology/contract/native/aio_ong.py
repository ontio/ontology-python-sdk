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
from ontology.account.account import Account
from ontology.contract.native.ong import Ong
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.contract.native.aio_asset import AioAsset


class AioOng(Ong, AioAsset):
    def __init__(self, sdk):
        super().__init__(sdk)

    async def unbound(self, address: Union[str, Address]) -> int:
        """
        This interface is used to query the amount of account's unbound ong.
        """
        ont_contract = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        if isinstance(address, Address):
            address = address.b58encode()
        return int(await self._sdk.default_aio_network.get_allowance('ong', Address(ont_contract).b58encode(), address))

    async def withdraw(self, claimer: Account, receiver: Union[str, Address], amount: int, payer: Account,
                       gas_price: int, gas_limit: int) -> str:
        """
        This interface is used to withdraw a amount of ong and transfer them to receive address.
        """
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        tx = self.new_withdraw_tx(claimer.get_address(), receiver, amount, payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(claimer)
        if claimer.get_address_base58() != payer.get_address_base58():
            tx.add_sign_transaction(payer)
        return await self._sdk.default_aio_network.send_raw_transaction(tx)
