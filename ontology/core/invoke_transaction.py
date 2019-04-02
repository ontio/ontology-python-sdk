#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time

from ontology.vm.op_code import APPCALL
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.transaction import Transaction, TransactionType
from ontology.utils.transaction import ensure_bytearray_contract_address
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class InvokeTransaction(Transaction):
    def __init__(self, payer: bytes = None, gas_price: int = 0, gas_limit: int = 0, params: bytearray = None,
                 version: int = 0):
        super().__init__(version, TransactionType.InvokeCode.value, int(time()), gas_price, gas_limit, payer, params,
                         bytearray(), [])

    @staticmethod
    def generate_invoke_code(contract_address: str or bytes or bytearray, func: AbiFunction or InvokeFunction):
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

    def add_invoke_code(self, contract_address: str or bytes or bytearray, func: AbiFunction or InvokeFunction):
        self.payload = self.generate_invoke_code(contract_address, func)
