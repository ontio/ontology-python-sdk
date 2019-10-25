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


class BaseInvokeFunc(object):
    def __init__(self, func_name: str, parameters: list = None, return_type: str = ''):
        self._func_name = func_name
        if parameters is None:
            parameters = list()
        self._parameters = parameters
        self._return_type = return_type

    @property
    def func_name(self):
        return self._func_name

    @property
    def parameters(self):
        return self._parameters

    @property
    def return_type(self):
        return self._return_type

    def set_params_value(self, *params):
        if len(self._parameters) != 0:
            self._parameters = list()
        for param in params:
            self._parameters.append(param)

    def add_params_value(self, *params):
        if self._parameters is None:
            self._parameters = list()
        for param in params:
            self._parameters.append(param)
