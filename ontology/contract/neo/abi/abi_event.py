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


class AbiEvent(object):
    def __init__(self, name: str, return_type: str, parameters: []):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters

    def get_parameters(self):
        return self.parameters

    def set_params_value(self, *objs):
        if len(self.parameters) != len(objs):
            raise SDKException(ErrorCode.other_error('Param error.'))
        for i, v in enumerate(objs):
            self.parameters[i].set_value(v)
