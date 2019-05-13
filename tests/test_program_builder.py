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

from ontology.core.program import ProgramBuilder


class TestProgramBuilder(unittest.TestCase):
    def test_sort_public_keys(self):
        pub_keys = ['02035b015221686aef1054b02605da2c3958885670b8298d36706593d3c451fa7e',
                    '022b06295115ef825b8a17524815d77cd79a44c9c8980288e35bab542792425fc2',
                    '03616dbe28eb6f2efdebe6a7b8fd824a56cf3e2ea5e03f802e19e686cb347d986f',
                    '0364c210b769c73ffc2782c74beb881581148023e42562a53d6dd8273e26845901',
                    '0296b60945cdbe44e9c8cfbeef7f6e462cb638dc65a5424e364ab0304063043950',
                    '02a2d9e83c40303a3439db54e55052c0133cbbc61580f008197d2d9c03abc2a8ef',
                    '02f7ec18df95f869e475361923105b9511dd8491d06ec0072530c174783a837846']
        pub_keys = ProgramBuilder.sort_public_keys(pub_keys)
        self.assertEqual(7, len(pub_keys))


if __name__ == '__main__':
    unittest.main()
