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

from ontology.contract.neo.oep4 import Oep4
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.utils.contract import Data, Event
from ontology.exception.exception import SDKException


class AioOep4(Oep4):
    def __init__(self, hex_contract_address: str = '', sdk=None):
        super().__init__(hex_contract_address, sdk)

    async def name(self):
        """
        This interface is used to get the name of the token asynchronously. E.g. "DXToken".
        """
        tx = self.new_name_tx()
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response.get('Result', ''))

    async def symbol(self):
        """
        This interface is used to get the symbol of the token asynchronously. E.g. “DX”.
        """
        tx = self.new_symbol_tx()
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        return Data.to_utf8_str(response.get('Result', ''))

    async def decimals(self):
        """
        This interface is used to the number of decimals the token uses asynchronously.
        E.g. 8, means to divide the token amount by 100000000 to get its user representation.
        """
        tx = self.new_decimals_tx()
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        return Data.to_int(response.get('Result', ''))

    async def total_supply(self) -> int:
        """
        This interface is used to get the total token supply asynchronously.
        """
        tx = self.new_total_supply_tx()
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        try:
            total_supply = Data.to_int(response['Result'])
        except SDKException:
            total_supply = 0
        return total_supply

    async def init(self, founder: Account, payer: Account, gas_price: int, gas_limit: int):
        tx = self.new_init_tx(payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(founder)
        if founder.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    async def balance_of(self, owner: Union[str, Address]) -> int:
        """
        This interface is used to get the account balance of another account with owner address asynchronously.
        """
        tx = self.new_balance_of_tx(owner)
        result = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        try:
            balance = Data.to_int(result['Result'])
        except SDKException:
            balance = 0
        return balance

    async def transfer(self, from_acct: Account, to_address: Union[str, Address], amount: int, payer: Account,
                       gas_price: int, gas_limit: int) -> str:
        """
        This interface is used to transfer amount of tokens to to_address asynchronously.
        """
        tx = self.new_transfer_tx(from_acct.get_address(), to_address, amount, payer.get_address(), gas_price,
                                  gas_limit)
        tx.sign_transaction(from_acct)
        if from_acct.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    async def transfer_multi(self, transfer_list: list, signers: list, payer_acct: Account, gas_price: int,
                             gas_limit: int) -> str:
        """
        This interface is used to transfer amount of token from from-account to to-account multiple times asynchronously.
        """
        tx = self.new_transfer_multi_tx(transfer_list, payer_acct.get_address(), gas_price, gas_limit)
        tx.sign_transaction(payer_acct)
        for signer in signers:
            tx.add_sign_transaction(signer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    async def approve(self, owner: Account, spender: Union[str, bytes, Address], amount: int, payer: Account,
                      gas_price: int, gas_limit: int) -> str:
        """
        This interface is used to allow spender to withdraw from owner account multiple times, up to the _value amount.
        If this function is called again it overwrites the current allowance with amount value.
        """
        tx = self.new_approve_tx(owner.get_address(), spender, amount, payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(owner)
        if owner.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    async def query_transfer_event(self, tx_hash: str):
        event = await self._sdk.default_aio_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self._contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify

    async def query_multi_transfer_event(self, tx_hash: str) -> list:
        event = await self._sdk.default_aio_network.get_contract_event_by_tx_hash(tx_hash)
        return self._parse_multi_transfer_event(event)

    async def query_approve_event(self, tx_hash: str):
        event = await self._sdk.default_aio_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self._contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify

    async def allowance(self, owner: Union[str, bytes, Address], spender: Union[str, bytes, Address]) -> int:
        tx = self.new_allowance_tx(owner, spender)
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        result = response.get('Result')
        if len(result) == 0:
            return 0
        return int(result, base=16)

    async def transfer_from(self, spender: Account, owner: Union[str, bytes, Address],
                            to_address: Union[str, bytes, Address], value: int, payer: Account, gas_price: int,
                            gas_limit: int) -> str:
        tx = self.new_transfer_from_tx(spender.get_address(), owner, to_address, value, payer.get_address(), gas_price,
                                       gas_limit)
        tx.sign_transaction(spender)
        if spender.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    async def query_transfer_from_event(self, tx_hash: str):
        event = await self._sdk.default_aio_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self._contract_address)
        notify = Data.parse_addr_addr_int_notify(notify)
        return notify
