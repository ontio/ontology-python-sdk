#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from ontology.common.define import DID_ONT
from ontology.wallet.control import Control
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Identity(object):
    def __init__(self, ont_id: str = '', label: str = '', lock: bool = False, controls: List[Control] = None,
                 is_default=False):
        if controls is None:
            controls = list()
        if not isinstance(ont_id, str):
            raise SDKException(ErrorCode.require_str_params)
        if len(ont_id) != 0 and not ont_id.startswith(DID_ONT):
            raise SDKException(ErrorCode.invalid_ont_id_format(ont_id))
        self.__ont_id = ont_id
        self.label = label
        self.lock = lock
        self.__controls = controls
        self.is_default = is_default

    def __iter__(self):
        data = dict()
        data['ontid'] = self.__ont_id
        data['label'] = self.label
        data['lock'] = self.lock
        data['controls'] = self.__controls
        data['isDefault'] = self.is_default
        for key, value in data.items():
            yield (key, value)

    @property
    def ont_id(self):
        return self.__ont_id

    @ont_id.setter
    def ont_id(self, ont_id: str):
        if not isinstance(ont_id, str):
            raise SDKException(ErrorCode.require_str_params)
        if len(ont_id) != 0 and not ont_id.startswith(DID_ONT):
            raise SDKException(ErrorCode.invalid_ont_id_format(ont_id))
        self.__ont_id = ont_id

    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, ctrl_lst: List[Control]):
        if not isinstance(ctrl_lst, list):
            raise SDKException(ErrorCode.require_list_params)
        for ctrl in ctrl_lst:
            if not isinstance(ctrl, Control):
                raise SDKException(ErrorCode.require_control_params)
        self.__controls = ctrl_lst

    def add_control(self, ctrl: Control):
        if not isinstance(ctrl, Control):
            raise SDKException(ErrorCode.require_control_params)
        self.__controls.append(ctrl)
