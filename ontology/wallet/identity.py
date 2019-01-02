#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from ontology.wallet.control import Control
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Identity(object):
    def __init__(self, ont_id: str = '', label: str = '', lock: bool = False, controls: List[Control] = None,
                 is_default=False):
        if controls is None:
            controls = list()
        if not isinstance(ont_id, str):
            raise SDKException(ErrorCode.other_error('Invalid OntId.'))
        self.ont_id = ont_id
        self.label = label
        self.lock = lock
        self.controls = controls
        self.is_default = is_default

    def __iter__(self):
        data = dict()
        data['ontid'] = self.ont_id
        data['label'] = self.label
        data['lock'] = self.lock
        data['controls'] = self.controls
        data['isDefault'] = self.is_default
        for key, value in data.items():
            yield (key, value)
