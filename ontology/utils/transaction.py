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


def ensure_bytearray_contract_address(contract_address: Union[str, bytes, bytearray, Address]) -> bytearray:
    if isinstance(contract_address, str) and len(contract_address) == 40:
        contract_address = bytearray.fromhex(contract_address)
        contract_address.reverse()
    if isinstance(contract_address, bytes):
        contract_address = bytearray(contract_address)
    elif isinstance(contract_address, Address):
        contract_address = contract_address.to_bytearray()
    elif isinstance(contract_address, bytearray):
        pass
    else:
        raise SDKException(ErrorCode.params_type_error('Invalid type of contract address.'))
    return contract_address


def ensure_bytes_address(*objs: str or bytes or Account):
    result = list()
    for obj in objs:
        if isinstance(obj, bytes):
            result.append(obj)
        elif isinstance(obj, str):
            result.append(Address.b58decode(obj).to_bytes())
        elif isinstance(obj, Account):
            result.append(obj.get_address_bytes())
        else:
            raise SDKException(ErrorCode.param_error)
    return tuple(result)
