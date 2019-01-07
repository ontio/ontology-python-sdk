#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps

from ontology.common.define import DID_ONT
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


def check_ont_id(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ont_id = args[1]
        if not isinstance(ont_id, str):
            raise SDKException(ErrorCode.require_str_params)
        if not ont_id.startswith(DID_ONT):
            raise SDKException(ErrorCode.invalid_ont_id_format(ont_id))
        return func(*args, **kwargs)

    return wrapper
