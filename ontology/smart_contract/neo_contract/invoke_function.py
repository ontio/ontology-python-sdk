#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams


class InvokeFunction(object):
    def __init__(self, func_name: str, parameters: list = None, return_type: str = ''):
        self.__func_name = func_name
        if parameters is None:
            parameters = list()
        self.__parameters = parameters
        self.__return_type = return_type

    def set_params_value(self, *params):
        if len(self.__parameters) != 0:
            self.__parameters = list()
        for param in params:
            self.__parameters.append(param)

    def create_invoke_code(self):
        param_list = list()
        param_list.append(self.__func_name.encode('utf-8'))
        param_list.append(self.__parameters)
        invoke_code = BuildParams.create_code_params_script(param_list)
        return invoke_code
