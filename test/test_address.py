#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.utils import util
from ontology.common.address import Address


class TestAddress(unittest.TestCase):
    def test_address_from_vm_code(self):
        code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
               '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
               '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        code_address = Address.address_from_vm_code(code)
        contract_hex_address = 'd0ed0f908896b4eb916584d461ca3e8b60b52c36'
        self.assertEqual(code_address.to_hex_str(), contract_hex_address)

    def test_b58decode(self):
        length = 20
        rand_code = util.get_random_bytes(length)
        address = Address(rand_code)
        b58_address = address.b58encode()
        zero = Address.b58decode(b58_address).to_array()
        self.assertEqual(rand_code, zero)
        decode_address = Address.b58decode(b58_address).to_array()
        self.assertEqual(rand_code, decode_address)


if __name__ == '__main__':
    unittest.main()
