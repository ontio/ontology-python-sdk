#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from test import sdk

from ontology.utils import utils
from ontology.common.address import Address


class TestAddress(unittest.TestCase):
    def test_address_from_vm_code(self):
        code = '55c56b6a00527ac46a51527ac46a00c30548656c6c6f7d9c7c756419006a51c300c36a52527ac46a52c3650d006c7' \
               '566620300006c756652c56b6a00527ac46a00c3681553797374656d2e52756e74696d652e4e6f74696679516c7566'
        contract_address = 'f2b6efc3e4360e69b8ff5db8ce8ac73651d07a12'
        self.assertEqual(contract_address, sdk.neo_vm.address_from_avm_code(code).hex())

    def test_b58decode(self):
        length = 20
        rand_code = utils.get_random_bytes(length)
        address = Address(rand_code)
        b58_address = address.b58encode()
        zero = Address.b58decode(b58_address).to_bytes()
        self.assertEqual(rand_code, zero)
        decode_address = Address.b58decode(b58_address).to_bytes()
        self.assertEqual(rand_code, decode_address)


if __name__ == '__main__':
    unittest.main()
