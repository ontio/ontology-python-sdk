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

from ontology.contract.neo.abi.build_params import BuildParams


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

    def add_params_value(self, *params):
        if self.__parameters is None:
            self.__parameters = list()
        for param in params:
            self.__parameters.append(param)

    def create_invoke_code(self):
        param_list = list()
        param_list.append(self.__func_name.encode('utf-8'))
        param_list.append(self.__parameters)
        invoke_code = BuildParams.create_code_params_script(param_list)
        return invoke_code
