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

from ontology.common.address import Address
from ontology.exception.exception import SDKException
from ontology.contract.wasm.params_builder import WasmParamsBuilder, WASM_UINT128_MAX, WASM_UINT128_MIN


class TestWasmVm(unittest.TestCase):
    def setUp(self):
        self.builder = WasmParamsBuilder()

    def tearDown(self):
        self.builder.clear_up()

    def test_push_int(self):
        py_int_list = [0, 1, 9007199254740993, 2 ** 128 - 1]
        wasm_int_list = ['00000000000000000000000000000000', '01000000000000000000000000000000',
                         '01000000000020000000000000000000', 'ffffffffffffffffffffffffffffffff']
        for index, value in enumerate(py_int_list):
            self.builder.push_int(value)
            self.assertEqual(wasm_int_list[index], self.builder.to_bytes().hex())
            self.builder.clear_up()
        self.assertRaises(SDKException, self.builder.push_int, WASM_UINT128_MAX + 1)
        self.assertRaises(SDKException, self.builder.push_int, WASM_UINT128_MIN - 1)

    def test_push_address(self):
        b58_address_list = ['AS3SCXw8GKTEeXpdwVw7EcC4rqSebFYpfb', 'AJkkLbouowk6teTaxz1F2DYKfJh24PVk3r',
                            'Ad4pjz2bqep4RhQrUAzMuZJkBC3qJ1tZuT', 'AK98G45DhmPXg4TFPG1KjftvkEaHbU8SHM']
        wasm_address_list = ['70a2ababdae0a9d1f9fc7296df3c6d343b772cf7', '20b1dc499cdf56ba70a574a1e17ac986d1f06ec2',
                             'e98f4998d837fcdd44a50561f7f32140c7c6c260', '24ed4f965d3a5a76f5d0e87633c0b76941fc8827']
        for index, b58_address in enumerate(b58_address_list):
            self.builder.push_address(Address.b58decode(b58_address))
            self.assertEqual(wasm_address_list[index], self.builder.to_bytes().hex())
            self.builder.clear_up()

    def test_push_str(self):
        str_list = [
            'Hello, world!',
            'Ontology',
            '!@#$%^&*()_+1234567890-=',
            '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        ]
        wasm_str_list = [
            '0d48656c6c6f2c20776f726c6421',
            '084f6e746f6c6f6779',
            '1821402324255e262a28295f2b313233343536373839302d3d',
            '3e313233343536373839304142434445464748494a4b4c4d4e4f50515253545'
            '5565758595a6162636465666768696a6b6c6d6e6f707172737475767778797a'
        ]
        for index, value in enumerate(str_list):
            self.builder.push_str(value)
            self.assertEqual(wasm_str_list[index], self.builder.to_bytes().hex())
            self.builder.clear_up()

    def test_push_bool(self):
        bool_list = [True, False]
        wasm_bool_list = ['01', '00']
        for index, value in enumerate(bool_list):
            self.builder.push_bool(value)
            self.assertEqual(wasm_bool_list[index], self.builder.to_bytes().hex())
            self.builder.clear_up()

    def test_push_list(self):
        py_list = ['Hello, world!', 100, True]
        wasm_list = '030d48656c6c6f2c20776f726c64216400000000000000000000000000000001'
        self.builder.push_list(py_list)
        self.assertEqual(wasm_list, self.builder.to_bytes().hex())
