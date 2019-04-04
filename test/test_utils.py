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
