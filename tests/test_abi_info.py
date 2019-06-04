#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import json
import unittest

from ontology.contract.neo.abi.abi_info import AbiInfo


class TestAbiInfo(unittest.TestCase):
    def setUp(self):
        self.func_name = 'Hello'
        str_abi = '{"hash":"0x362cb5608b3eca61d4846591ebb49688900fedd0","entrypoint":"Main","functions":' \
                  '[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args",' \
                  '"type":"Array"}],"returntype":"Any"},{"name":"Hello","parameters":[{"name":"msg",' \
                  '"type":"String"}],"returntype":"Void"}],"events":[]}'
        dict_abi = json.loads(str_abi)
        self.abi_info = AbiInfo(dict_abi['hash'], dict_abi['entrypoint'], dict_abi['functions'], dict_abi['events'])

    def test_init(self):
        self.assertTrue(isinstance(self.abi_info, AbiInfo))

    def test_get_function(self):
        func = self.abi_info.get_function(self.func_name)
        self.assertEqual(self.func_name, func.name)

    def test_set_params_value(self):
        func = self.abi_info.get_function(self.func_name)
        func.set_params_value('Value')
        self.assertEqual('Value', func.parameters[0].value)

    def test_get_parameter(self):
        func = self.abi_info.get_function(self.func_name)
        func.set_params_value('Value')
        param_name = 'msg'
        parameter = func.get_parameter(param_name)
        self.assertEqual(param_name, parameter.name)
        self.assertEqual('String', parameter.type)
        self.assertEqual('Value', parameter.value)


if __name__ == '__main__':
    unittest.main()
