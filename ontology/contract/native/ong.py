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
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.vm.build_vm import build_native_invoke_code
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.contract.native.asset import Asset


class Ong(Asset):
    def __init__(self, sdk):
        super().__init__(sdk)
        self._contract_address = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._invoke_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'

    def new_withdraw_tx(self, claimer: Union[str, Address], receiver: Union[str, Address], amount: int,
                        payer: Union[str, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a Transaction object that
        allow one account to withdraw an amount of ong and transfer them to receive address.
        """
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        payer = Address.b58decode(payer)
        ont_contract = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        args = dict(claimer=Address.b58decode(claimer), from_address=ont_contract,
                    to_address=Address.b58decode(receiver), value=amount)
        invoke_code = build_native_invoke_code(self._invoke_address, self._version, 'transferFrom', args)
        return InvokeTransaction(payer, gas_price, gas_limit, invoke_code)

    def unbound(self, address: Union[str, Address]) -> int:
        """
        This interface is used to query the amount of account's unbound ong.
        """
        ont_contract = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        if isinstance(address, Address):
            address = address.b58encode()
        return int(self._sdk.default_network.get_allowance('ong', Address(ont_contract).b58encode(), address))

    def withdraw(self, claimer: Account, receiver: Union[str, Address], amount: int, payer: Account, gas_price: int,
                 gas_limit: int) -> str:
        """
        This interface is used to withdraw a amount of ong and transfer them to receive address.
        """
        if amount <= 0:
            raise SDKException(ErrorCode.other_error('the amount should be greater than than zero.'))
        tx = self.new_withdraw_tx(claimer.get_address(), receiver, amount, payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(claimer)
        if claimer.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        return self._sdk.default_network.send_raw_transaction(tx)
