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

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.contract.neo.abi.parameter import Parameter


class AbiFunction(object):
    def __init__(self, name: str, parameters: list, return_type: str = ''):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters

    def set_params_value(self, *params):
        """
        This interface is used to set parameter value for an function in abi file.
        """
        if len(params) != len(self.parameters):
            raise Exception("parameter error")
        for i, p in enumerate(params):
            self.parameters[i] = Parameter(self.parameters[i]['name'], self.parameters[i]['type'], p)

    def get_parameter(self, param_name: str) -> Parameter:
        """
        This interface is used to get a Parameter object from an AbiFunction object
        which contain given function parameter's name, type and value.

        :param param_name: a string used to indicate which parameter we want to get from AbiFunction.
        :return: a Parameter object which contain given function parameter's name, type and value.
        """
        for p in self.parameters:
            if p.name == param_name:
                return p
        raise SDKException(ErrorCode.param_err('get parameter failed.'))
