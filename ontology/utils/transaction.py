#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


def ensure_bytearray_contract_address(contract_address: str or bytes or bytearray) -> bytearray:
    if isinstance(contract_address, str) and len(contract_address) == 40:
        contract_address = bytearray.fromhex(contract_address)
        contract_address.reverse()
    if isinstance(contract_address, bytes):
        contract_address = bytearray(contract_address)
    elif isinstance(contract_address, bytearray):
        pass
    else:
        raise SDKException(ErrorCode.params_type_error('Invalid type of contract address.'))
    return contract_address
