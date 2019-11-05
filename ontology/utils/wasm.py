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

from typing import Union

from ontology.common.address import Address
from ontology.contract.wasm.params_builder import WasmParamsBuilder


class WasmData(object):
    @staticmethod
    def to_int(value: Union[str, bytes]):
        if isinstance(value, str):
            value = bytes.fromhex(value)
        return int.from_bytes(value, byteorder='little', signed=True)

    @staticmethod
    def detect_to_utf8(value: Union[str, bytes]):
        if isinstance(value, str):
            value = bytes.fromhex(value)
        builder = WasmParamsBuilder(value)
        return builder.pop_str()

    @staticmethod
    def to_utf8(value: Union[str, bytes]):
        if isinstance(value, str):
            value = bytes.fromhex(value)
        return value.decode('utf-8')

    @staticmethod
    def to_b58_address(value: Union[str, bytes]) -> str:
        if isinstance(value, str):
            value = bytes.fromhex(value)
        return Address(value).b58encode()
