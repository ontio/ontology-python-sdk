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

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.utils.contract import Data, Event
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.contract.neo.invoke_function import InvokeFunction


class ClaimRecord(object):
    def __init__(self, sdk, hex_contract_address: str = ''):
        self._sdk = sdk
        if isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            self.__hex_contract_address = hex_contract_address
        else:
            self.__hex_contract_address = '36bb5c053b6b839c8f6b923fe852f91239b9fccc'

    @property
    def hex_contract_address(self):
        return self.__hex_contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address):
        if isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            self.__hex_contract_address = hex_contract_address
        else:
            raise SDKException(ErrorCode.invalid_contract_address(hex_contract_address))

    def new_commit_tx(self, claim_id: str, issuer_address: Union[str, bytes, Address], owner_ont_id: str,
                      payer_address: Union[str, bytes, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        func = InvokeFunction('Commit')
        func.set_params_value(claim_id, Address.b58decode(issuer_address), owner_ont_id)
        tx = InvokeTransaction(Address.b58decode(payer_address), gas_price, gas_limit)
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def commit(self, claim_id: str, issuer: Account, owner_ont_id: str, payer: Account, gas_price: int,
               gas_limit: int) -> str:
        tx = self.new_commit_tx(claim_id, issuer.get_address(), owner_ont_id, payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(issuer)
        if issuer.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    def new_revoke_tx(self, claim_id: str, issuer: Union[str, bytes, Address], payer: Union[str, bytes, Address],
                      gas_price: int, gas_limit: int):
        func = InvokeFunction('Revoke')
        func.set_params_value(claim_id, Address.b58decode(issuer))
        tx = InvokeTransaction(Address.b58decode(payer), gas_price, gas_limit)
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def revoke(self, claim_id: str, issuer: Account, payer: Account, gas_price: int, gas_limit: int):
        tx = self.new_revoke_tx(claim_id, issuer.get_address(), payer.get_address(), gas_price, gas_limit)
        tx.sign_transaction(issuer)
        if issuer.get_address_bytes() != payer.get_address_bytes():
            tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    def new_get_status_tx(self, claim_id: str) -> InvokeTransaction:
        func = InvokeFunction('GetStatus')
        func.set_params_value(claim_id)
        tx = InvokeTransaction()
        tx.add_invoke_code(self.__hex_contract_address, func)
        return tx

    def get_status(self, claim_id: str):
        tx = self.new_get_status_tx(claim_id)
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        return self.parse_status(response)

    @staticmethod
    def parse_status(result: dict):
        status = result['Result']
        if status == '':
            status = False
        else:
            status = Data.to_dict(status)
            status = bool(status[3])
        return status

    def query_commit_event(self, tx_hash: str):
        event = self._sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self.__hex_contract_address)
        if len(notify) == 0:
            return notify
        if len(notify['States']) == 4:
            notify['States'][0] = Data.to_utf8_str(notify['States'][0])
            notify['States'][1] = Data.to_b58_address(notify['States'][1])
            notify['States'][2] = Data.to_utf8_str(notify['States'][2])
            notify['States'][3] = Data.to_hex_str(notify['States'][3])
        if len(notify['States']) == 3:
            notify['States'][0] = Data.to_utf8_str(notify['States'][0])
            notify['States'][1] = Data.to_hex_str(notify['States'][1])
            notify['States'][2] = Data.to_utf8_str(notify['States'][2])
        return notify

    def query_revoke_event(self, tx_hash: str):
        event = self._sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, self.__hex_contract_address)
        if len(notify['States']) == 4:
            notify['States'][0] = Data.to_utf8_str(notify['States'][0])
            notify['States'][1] = Data.to_b58_address(notify['States'][1])
            notify['States'][2] = Data.to_utf8_str(notify['States'][2])
            notify['States'][3] = Data.to_hex_str(notify['States'][3])
        return notify
