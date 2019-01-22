#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.utils import utils


class TestUtil(unittest.TestCase):
    def test_get_random_bytes(self):
        self.assertRaises(ValueError, utils.get_random_bytes, -1)
        len_list = [0, 1, 64, 256, 1024, 2048]
        for length in len_list:
            self.assertEqual(len(utils.get_random_bytes(length)), length)

    def test_get_random_hex_str(self):
        self.assertRaises(ValueError, utils.get_random_hex_str, -1)
        len_list = [0, 1, 64, 256, 1024, 2048]
        for length in len_list:
            self.assertEqual(len(utils.get_random_hex_str(length)), length)


if __name__ == '__main__':
    unittest.main()
