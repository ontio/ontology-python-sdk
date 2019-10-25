"""
Copyright (C) 2018-2019 The ontology Authors
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

from enum import Enum
from typing import List

from ontology.contract.neo.abi.abi_function import AbiFunction
from ontology.contract.neo.params_builder import NeoParamsBuilder
from ontology.contract.wasm.params_builder import WasmParamsBuilder


class BuildParams(object):
    class Type(Enum):
        bytearray_type = 0x00
        bool_type = 0x01
        int_type = 0x02
        array_type = 0x80
        struct_type = 0x81
        dict_type = 0x82

    @staticmethod
    def serialize_abi_function(abi_func: AbiFunction):
        param_list = list()
        param_list.append(bytes(abi_func.name.encode('utf-8')))
        temp_list = list()
        for param in abi_func.parameters:
            try:
                if isinstance(param.value, list):
                    temp_param_list = []
                    for item in param.value:
                        if isinstance(item, list):
                            temp_list.append(item)
                        else:
                            temp_param_list.append(item)
                    if len(temp_param_list) != 0:
                        temp_list.append(temp_param_list)
                else:
                    temp_list.append(param.value)
            except AttributeError:
                pass
        param_list.append(temp_list)
        return BuildParams.create_neo_vm_invoke_code(param_list)

    @staticmethod
    def create_neo_vm_invoke_code(param_list: List) -> bytearray:
        builder = NeoParamsBuilder()
        length = len(param_list)
        for j in range(length):
            i = length - 1 - j
            builder.push_vm_param(param_list[i])
        return builder.to_bytearray()

    @staticmethod
    def create_wasm_vm_invoke_code(param_list: List) -> bytearray:
        builder = WasmParamsBuilder()
        for param in param_list:
            builder.push_vm_param(param)
        return builder.pack_as_bytearray()
