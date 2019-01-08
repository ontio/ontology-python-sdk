#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
