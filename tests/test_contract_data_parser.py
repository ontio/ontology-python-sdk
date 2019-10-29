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

import unittest

from ontology.utils.neo import Data
from ontology.contract.neo.params_builder import NeoParamsBuilder


class TestContractDataParser(unittest.TestCase):
    def test_bigint_to_neo_bytes(self):
        value_list = [9175052165852779861, -9175052165852779861, 9199634313818843819, -9199634313818843819, 8380656,
                      -8380656, 8446192, -8446192, 0]
        for value in value_list:
            neo_bytearray = Data.big_int_to_neo_bytearray(value)
            self.assertTrue(isinstance(neo_bytearray, bytearray))
            neo_value = Data.neo_bytearray_to_big_int(neo_bytearray)
            self.assertEqual(value, neo_value)

    def test_op_code_to_int(self):
        builder = NeoParamsBuilder()
        for num in range(100000):
            builder.push_int(num)
            op_code = builder.to_bytes().hex()
            builder.clear_up()
            value = Data.op_code_to_int(op_code)
            self.assertEqual(num, value)
