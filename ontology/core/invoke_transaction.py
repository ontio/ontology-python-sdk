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

from ontology.vm.op_code import APPCALL
from ontology.common.address import Address
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.transaction import Transaction, TransactionType
from ontology.utils.transaction import ensure_bytearray_contract_address
from ontology.contract.neo.abi.abi_function import AbiFunction
from ontology.contract.neo.abi.build_params import BuildParams
from ontology.contract.neo.invoke_function import InvokeFunction


class InvokeTransaction(Transaction):
    def __init__(self, payer: Union[str, bytes, Address] = b'', gas_price: int = 0, gas_limit: int = 0,
                 payload: bytearray = None, version: int = 0):
        super().__init__(version, TransactionType.InvokeCode.value, gas_price, gas_limit, payer, payload)

    @staticmethod
    def generate_invoke_code(contract_address: Union[str, bytes, bytearray, Address],
                             func: Union[AbiFunction, InvokeFunction]):
        if isinstance(func, AbiFunction):
            params = BuildParams.serialize_abi_function(func)
        elif isinstance(func, InvokeFunction):
            params = func.create_invoke_code()
        else:
            raise SDKException(ErrorCode.other_error('the type of func is error.'))
        contract_address = ensure_bytearray_contract_address(contract_address)
        params.append(int.from_bytes(APPCALL, byteorder='little'))
        for i in contract_address:
            params.append(i)
        return params

    def add_invoke_code(self, contract_address: Union[str, bytes, bytearray, Address],
                        func: AbiFunction or InvokeFunction):
        self.payload = self.generate_invoke_code(contract_address, func)
