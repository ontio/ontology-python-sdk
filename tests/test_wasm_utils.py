import unittest

from ontology.utils.wasm import WasmData


class TestWasmVm(unittest.TestCase):
    def test_to_int(self):
        wasm_hex_data = ['ffffffffffffffffffffffffffffff7f', '00000000000000000000000000000080',
                         'feffffffffffffffffffffffffffffff', '00000000000000000000000000000000',
                         '01000000000000000000000000000000', '02000000000000000000000000000000']
        int_data = [2 ** 127 - 1, -2 ** 127, -2, 0, 1, 2]
        for index, hex_data in enumerate(wasm_hex_data):
            self.assertEqual(int_data[index], WasmData.to_int(hex_data))

    def test_to_utf8(self):
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
        for index, wasm_str in enumerate(wasm_str_list):
            self.assertEqual(str_list[index], WasmData.to_utf8(wasm_str))
