#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
