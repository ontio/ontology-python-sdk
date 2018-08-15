#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from ontology.common.error_code import ErrorCode


class TestErrorCode(unittest.TestCase):
    def test_get_error(self):
        code = 123
        msg = 'test'
        error_code = ErrorCode.get_error(code, msg)
        self.assertEqual(json.loads(error_code)["Error"], code)
        self.assertEqual(json.loads(error_code)["Desc"], msg)

    def test_constructed_root_hash_err(self):
        code = 54003
        msg = 'TEST'
        desc = "Other Error, " + msg
        value = ErrorCode.constructed_root_hash_err(msg)
        self.assertEqual(json.loads(value)["Error"], code)
        self.assertEqual(json.loads(value)["Desc"], desc)

    def test_connect_url_err(self):
        code = 58403
        msg = 'TEST'
        desc = "connect error: " + msg
        value = ErrorCode.connect_err(msg)
        self.assertEqual(json.loads(value)["Error"], code)
        self.assertEqual(json.loads(value)["Desc"], desc)

    def test_other_error(self):
        code = 59000
        msg = 'TEST'
        desc = "Other Error, " + msg
        value = ErrorCode.other_error(msg)
        self.assertEqual(json.loads(value)["Error"], code)
        self.assertEqual(json.loads(value)["Desc"], desc)

    def test_param_err(self):
        code = 58005
        msg = 'TEST'
        value = ErrorCode.param_err(msg)
        self.assertEqual(json.loads(value)["Error"], code)
        self.assertEqual(json.loads(value)["Desc"], msg)

    def test_invalid_params(self):
        code = 51001
        desc = "Account Error,invalid params"
        value = ErrorCode.invalid_params
        self.assertEqual(type(value), str)
        self.assertEqual(json.loads(value)["Error"], code)
        self.assertEqual(json.loads(value)["Desc"], desc)

    def test_param_length_not_same(self):
        code = 58105
        desc = "OntAsset Error,param length is not the same"
        value = ErrorCode.param_length_not_same
        self.assertEqual(type(value), str)
        self.assertEqual(json.loads(value)["Error"], code)
        self.assertEqual(json.loads(value)["Desc"], desc)


if __name__ == '__main__':
    unittest.main()
