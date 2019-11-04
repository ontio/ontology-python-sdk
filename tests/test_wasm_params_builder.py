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
from ontology.contract.wasm.params_builder import WasmParamsBuilder, WASM_INT128_MAX, WASM_INT128_MIN
from ontology.exception.exception import SDKException


class TestWasmVm(unittest.TestCase):
    def setUp(self):
        self.builder = WasmParamsBuilder()

    def tearDown(self):
        self.builder.clear_up()

    def test_push_int(self):
        py_int_list = [-2 ** 127, -2, -1, 0, 1, 2, 2 ** 127 - 1]
        wasm_int_list = ['00000000000000000000000000000080', 'feffffffffffffffffffffffffffffff',
                         'ffffffffffffffffffffffffffffffff', '00000000000000000000000000000000',
                         '01000000000000000000000000000000', '02000000000000000000000000000000',
                         'ffffffffffffffffffffffffffffff7f']
        for index, value in enumerate(py_int_list):
            self.builder.push_int(value)
            self.assertEqual(wasm_int_list[index], self.builder.to_bytes().hex())
            self.builder.clear_up()
        self.assertRaises(SDKException, self.builder.push_int, WASM_INT128_MAX + 1)
        self.assertRaises(SDKException, self.builder.push_int, WASM_INT128_MIN - 1)

    def test_push_address(self):
        b58_address_list = [
            'AS7MjVEicEsJ4zjEfm2LoKoYoFsmapD7rT',
            'AFmseVrdL9f9oyCzZefL9tG6UbviEH9ugK',
            'AS3SCXw8GKTEeXpdwVw7EcC4rqSebFYpfb',
            'AJkkLbouowk6teTaxz1F2DYKfJh24PVk3r',
            'Ad4pjz2bqep4RhQrUAzMuZJkBC3qJ1tZuT',
            'AK98G45DhmPXg4TFPG1KjftvkEaHbU8SHM'
        ]
        wasm_address_list = [
            '71609b2c2f7b9447b089ad1da31586f42ca9eb10',
            '0000000000000000000000000000000000000007',
            '70a2ababdae0a9d1f9fc7296df3c6d343b772cf7',
            '20b1dc499cdf56ba70a574a1e17ac986d1f06ec2',
            'e98f4998d837fcdd44a50561f7f32140c7c6c260',
            '24ed4f965d3a5a76f5d0e87633c0b76941fc8827'
        ]
        for index, b58_address in enumerate(b58_address_list):
            self.builder.push_address(Address.b58decode(b58_address))
            self.assertEqual(wasm_address_list[index], self.builder.to_bytes().hex())
            self.builder.clear_up()

    def test_push_pop_str(self):
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
        for index, wasm_str in enumerate(wasm_str_list):
            self.builder.set_buffer(wasm_str)
            self.assertEqual(str_list[index], self.builder.pop_str())

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

    def test_read_var_uint(self):
        wasm_hex_uint = [
            '00',
            '01',
            'fdfe00',
            'fe00000100',
            'fe01000100',
            'feffffffff',
            'ff0000000001000000',
            'ffffffffffffffff0f',
            'ffffffffffffffffff',
        ]
        int_data = [
            0,
            1,
            254,
            65536,
            65537,
            4294967295,
            4294967296,
            1152921504606846975,
            18446744073709551615
        ]
        for index, hex_uint in enumerate(wasm_hex_uint):
            self.builder.write_var_uint(int_data[index])
            self.assertEqual(wasm_hex_uint[index], self.builder.to_bytes().hex())
            self.builder.clear_up()
            self.builder.set_buffer(hex_uint)
            self.assertEqual(int_data[index], self.builder.read_var_uint())
            self.builder.clear_up()

    def test_pop_str_struct(self):
        hex_wasm_str = '01606438646337313735616137333633323165343639643539623663303661396531666462356432373735633' \
                       '83261396638333364333463643361343033356132303166653964633762333961653832643963356339316262' \
                       '663564313634366364042e6a70672032303165393337366361616131366561393832623561333165626130663' \
                       '36634823034383436383165383932333630646334373030363036323733626631366236613063343133393864' \
                       '65326532643936306633343030373936313061656538383536363736623231323233313966613037323665633' \
                       '16666323735396664336339313232646438333461666531376535316164666665626638326162633037656363'
        target_struct = [
            [
                'd8dc7175aa736321e469d59b6c06a9e1fdb5d2775c82a9f833d34cd3a4035a201fe9dc7b39ae82d9c5c91bbf5d1646cd',
                '.jpg',
                '201e9376caaa16ea982b5a31eba0f3f4',
                '0484681e892360dc4700606273bf16b6a0c41398de2e2d960f340079610aee885'
                '6676b2122319fa0726ec1ff2759fd3c9122dd834afe17e51adffebf82abc07ecc'
            ]
        ]
        self.builder.set_buffer(hex_wasm_str)
        item_len = self.builder.read_var_uint()
        for index in range(item_len):
            self.assertEqual(target_struct[index][0], self.builder.pop_str())
            self.assertEqual(target_struct[index][1], self.builder.pop_str())
            self.assertEqual(target_struct[index][2], self.builder.pop_str())
            self.assertEqual(target_struct[index][3], self.builder.pop_str())
