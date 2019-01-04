#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import b2a_hex
import unittest

from ontology.utils import utils
from ontology.common.address import Address
from ontology.utils.contract_data_parser import ContractDataParser
from test import sdk


class TestAddress(unittest.TestCase):
    def test_address_from_vm_code(self):
        code = '55c56b6a00527ac46a51527ac46a00c30548656c6c6f7d9c7c756419006a51c300c36a52527ac46a52c3650d006c7' \
               '566620300006c756652c56b6a00527ac46a00c3681553797374656d2e52756e74696d652e4e6f74696679516c7566'
        code_address = Address.address_from_vm_code(code)
        contract_address = 'f2b6efc3e4360e69b8ff5db8ce8ac73651d07a12'
        self.assertEqual(contract_address, code_address.to_hex_str())
        self.assertEqual(contract_address, b2a_hex(code_address.to_bytes()).decode('ascii'))
        self.assertEqual(contract_address, b2a_hex(code_address.to_bytearray()).decode('ascii'))
        self.assertEqual(contract_address, ContractDataParser.to_reserve_hex_str(code_address.to_reverse_hex_str()))
        self.assertEqual(contract_address, sdk.neo_vm.avm_code_to_hex_contract_address(code))
        bytes_address = sdk.neo_vm.avm_code_to_bytes_contract_address(code)
        self.assertEqual(contract_address, b2a_hex(bytes_address).decode('ascii'))
        bytearray_address = sdk.neo_vm.avm_code_to_bytearray_contract_address(code)
        self.assertEqual(contract_address, b2a_hex(bytearray_address).decode('ascii'))

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
