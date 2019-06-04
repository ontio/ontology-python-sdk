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

from ontology.exception.error_code import ErrorCode


class TestErrorCode(unittest.TestCase):
    def test_get_error(self):
        code = 123
        msg = 'test'
        error_code = ErrorCode.get_error(code, msg)
        self.assertEqual(error_code["error"], code)
        self.assertEqual(error_code["desc"], msg)

    def test_constructed_root_hash_err(self):
        msg = 'TEST'
        desc = "Other Error, " + msg
        value = ErrorCode.constructed_root_hash_err(msg)
        self.assertEqual(value["desc"], desc)

    def test_connect_url_err(self):
        msg = 'TEST'
        desc = "connect error: " + msg
        value = ErrorCode.connect_err(msg)
        self.assertEqual(value["desc"], desc)

    def test_other_error(self):
        msg = 'TEST'
        desc = "Other Error, " + msg
        value = ErrorCode.other_error(msg)
        self.assertEqual(value["desc"], desc)

    def test_param_err(self):
        msg = 'TEST'
        value = ErrorCode.param_err(msg)
        self.assertEqual(value["desc"], msg)

    def test_invalid_acct_params(self):
        desc = "Account Error, invalid private key."
        value = ErrorCode.invalid_private_key
        self.assertEqual(type(value), dict)
        self.assertEqual(value["desc"], desc)

    def test_param_length_not_same(self):
        desc = "OntAsset Error, param length is not the same"
        value = ErrorCode.param_length_not_same
        self.assertEqual(type(value), dict)
        self.assertEqual(value["desc"], desc)


if __name__ == '__main__':
    unittest.main()
