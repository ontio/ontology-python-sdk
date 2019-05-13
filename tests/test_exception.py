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

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.exception.exception import SDKRuntimeException


class TestSDKException(unittest.TestCase):
    def test_sdk_exception(self):
        try:
            raise SDKException(ErrorCode.param_error)
        except SDKException as e:
            self.assertEqual('param error', e.args[1])

        try:
            raise SDKException(ErrorCode.asset_name_error)
        except SDKException as e:
            self.assertEqual('OntAsset Error, asset name error', e.args[1])

    def test_sdk_runtime_exception(self):
        try:
            raise SDKRuntimeException(ErrorCode.encrypted_pri_key_error)
        except SDKRuntimeException as e:
            self.assertEqual("Account Error, Prikey length error", e.args[1])

        try:
            raise SDKRuntimeException(ErrorCode.left_tree_full)
        except SDKRuntimeException as e:
            self.assertEqual("left tree always full", e.args[1])


if __name__ == '__main__':
    unittest.main()
