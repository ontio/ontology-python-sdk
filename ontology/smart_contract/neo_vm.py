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
from ontology.smart_contract.neo_contract.oep4 import Oep4
from ontology.core.deploy_transaction import DeployTransaction
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.smart_contract.neo_contract.claim_record import ClaimRecord
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class NeoVm(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def oep4(self):
        return Oep4(self.__sdk)

    def claim_record(self):
        return ClaimRecord(self.__sdk)

    @staticmethod
    def avm_code_to_hex_contract_address(avm_code: str):
        hex_contract_address = Address.address_from_vm_code(avm_code).to_hex_str()
        return hex_contract_address

    @staticmethod
    def avm_code_to_bytes_contract_address(avm_code: str):
        bytes_contract_address = Address.address_from_vm_code(avm_code).to_bytes()
        return bytes_contract_address

    @staticmethod
    def avm_code_to_bytearray_contract_address(avm_code: str):
        bytearray_contract_address = Address.address_from_vm_code(avm_code).to_bytearray()
        return bytearray_contract_address

    @staticmethod
    def make_deploy_transaction(code: str, need_storage: bool, name: str, code_version: str, author: str,
                                email: str, description: str, gas_price: int, gas_limit: int,
                                b58_payer_address: str) -> DeployTransaction:
        tx = DeployTransaction(code, need_storage, name, code_version, author, email, description, gas_price, gas_limit,
                               b58_payer_address)
        return tx

    @staticmethod
    def make_invoke_transaction(contract_address: str or bytes or bytearray, func: AbiFunction or InvokeFunction,
                                payer: bytes or str = b'', gas_price: int = 0, gas_limit: int = 0):
        tx = InvokeTransaction(payer, gas_price, gas_limit)
        tx.add_invoke_code(contract_address, func)
        return tx
