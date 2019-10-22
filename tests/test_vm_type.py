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

import unittest

from ontology.exception.exception import SDKException

from ontology.vm.vm_type import VmType


class TestVmType(unittest.TestCase):
    def test_from_int(self):
        self.assertEqual(VmType.Neo, VmType.from_int(VmType.Neo.value))
        self.assertEqual(VmType.Wasm, VmType.from_int(VmType.Wasm.value))
        self.assertRaises(SDKException, VmType.from_int, 0)
