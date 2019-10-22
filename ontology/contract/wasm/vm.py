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

from os import path
from typing import Union

from ontology.vm.vm_type import VmType
from ontology.common.address import Address
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.deploy_transaction import DeployTransaction


class WasmVm(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    @staticmethod
    def open_wasm(wasm_file_path: str):
        if not path.isfile(wasm_file_path):
            raise SDKException(ErrorCode.require_file_path_params)
        with open(wasm_file_path, 'rb') as f:
            content = f.read()
            return content.hex()

    @staticmethod
    def make_deploy_transaction(code: str,
                                name: str,
                                code_version: str,
                                author: str,
                                email: str,
                                description: str,
                                gas_price: int,
                                gas_limit: int,
                                payer: Union[str, bytes, Address]) -> DeployTransaction:
        tx = DeployTransaction(code, VmType.Wasm, name, code_version, author, email, description, gas_price, gas_limit,
                               payer)
        return tx
