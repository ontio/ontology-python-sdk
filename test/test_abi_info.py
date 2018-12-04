#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo


class TestAbiInfo(unittest.TestCase):
    def test_init(self):
        str_abi = '{"hash":"0x362cb5608b3eca61d4846591ebb49688900fedd0","entrypoint":"Main","functions":' \
                  '[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args",' \
                  '"type":"Array"}],"returntype":"Any"},{"name":"Hello","parameters":[{"name":"msg",' \
                  '"type":"String"}],"returntype":"Void"}],"events":[]}'
        dict_abi = json.loads(str_abi)
        abi_info = AbiInfo(dict_abi['hash'], dict_abi['entrypoint'], dict_abi['functions'], dict_abi['events'])
        self.assertTrue(isinstance(abi_info, AbiInfo))

    def test_get_function(self):
        str_abi = '{"hash":"0x362cb5608b3eca61d4846591ebb49688900fedd0","entrypoint":"Main","functions":' \
                  '[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args",' \
                  '"type":"Array"}],"returntype":"Any"},{"name":"Hello","parameters":[{"name":"msg",' \
                  '"type":"String"}],"returntype":"Void"}],"events":[]}'
        dict_abi = json.loads(str_abi)
        abi_info = AbiInfo(dict_abi['hash'], dict_abi['entrypoint'], dict_abi['functions'], dict_abi['events'])
        func_name = 'Hello'
        func = abi_info.get_function(func_name)
        self.assertEqual(func_name, func.name)

    def test_set_params_value(self):
        str_abi = '{"hash":"0x362cb5608b3eca61d4846591ebb49688900fedd0","entrypoint":"Main","functions":' \
                  '[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args",' \
                  '"type":"Array"}],"returntype":"Any"},{"name":"Hello","parameters":[{"name":"msg",' \
                  '"type":"String"}],"returntype":"Void"}],"events":[]}'
        dict_abi = json.loads(str_abi)
        abi_info = AbiInfo(dict_abi['hash'], dict_abi['entrypoint'], dict_abi['functions'], dict_abi['events'])
        func_name = 'Hello'
        func = abi_info.get_function(func_name)
        func.set_params_value('Value')
        self.assertEqual('Value', func.parameters[0].value)

    def test_get_parameter(self):
        str_abi = '{"hash":"0x362cb5608b3eca61d4846591ebb49688900fedd0","entrypoint":"Main","functions":' \
                  '[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args",' \
                  '"type":"Array"}],"returntype":"Any"},{"name":"Hello","parameters":[{"name":"msg",' \
                  '"type":"String"}],"returntype":"Void"}],"events":[]}'
        dict_abi = json.loads(str_abi)
        abi_info = AbiInfo(dict_abi['hash'], dict_abi['entrypoint'], dict_abi['functions'], dict_abi['events'])
        func_name = 'Hello'
        func = abi_info.get_function(func_name)
        func.set_params_value('Value')
        param_name = 'msg'
        parameter = func.get_parameter(param_name)
        self.assertEqual(param_name, parameter.name)
        self.assertEqual('String', parameter.type)
        self.assertEqual('Value', parameter.value)


if __name__ == '__main__':
    unittest.main()
