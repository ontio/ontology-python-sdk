#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum

from ontology.utils import utils
from ontology.common.address import Address
from ontology.exception.error_code import ErrorCode
from ontology.vm.params_builder import ParamsBuilder
from ontology.exception.exception import SDKException
from ontology.contract.neo.abi.struct_type import Struct
from ontology.contract.neo.abi.abi_function import AbiFunction

from ontology.vm.op_code import (
    PACK,
    NEWMAP,
    TOALTSTACK,
    DUPFROMALTSTACK,
    SETITEM,
    FROMALTSTACK,
    NEWSTRUCT,
    SWAP,
    APPEND
)


class BuildParams(object):
    class Type(Enum):
        bytearray_type = 0x00
        bool_type = 0x01
        int_type = 0x02
        array_type = 0x80
        struct_type = 0x81
        dict_type = 0x82

    @staticmethod
    def serialize_abi_function(abi_func: AbiFunction):
        param_list = list()
        param_list.append(bytes(abi_func.name.encode('utf-8')))
        temp_list = list()
        for param in abi_func.parameters:
            try:
                if isinstance(param.value, list):
                    temp_param_list = []
                    for item in param.value:
                        if isinstance(item, list):
                            temp_list.append(item)
                        else:
                            temp_param_list.append(item)
                    if len(temp_param_list) != 0:
                        temp_list.append(temp_param_list)
                else:
                    temp_list.append(param.value)
            except AttributeError:
                pass
        param_list.append(temp_list)
        return BuildParams.create_code_params_script(param_list)

    @staticmethod
    def create_code_params_script(param_list: []) -> bytearray:
        builder = ParamsBuilder()
        length = len(param_list)
        for j in range(length):
            i = length - 1 - j
            BuildParams.push_param(param_list[i], builder)
        return builder.to_bytearray()

    @staticmethod
    def create_code_params_script_builder(param_list: list, builder: ParamsBuilder):
        length = len(param_list)
        for j in range(length):
            i = length - 1 - j
            BuildParams.push_param(param_list[i], builder)
        return builder.to_bytes()

    @staticmethod
    def push_param(param, builder: ParamsBuilder):
        if isinstance(param, bytearray) or isinstance(param, bytes):
            builder.emit_push_bytearray(param)
        elif isinstance(param, str):
            builder.emit_push_bytearray(bytes(param.encode()))
        elif isinstance(param, bool):
            builder.emit_push_bool(param)
        elif isinstance(param, int):
            builder.emit_push_int(param)
        elif isinstance(param, dict):
            BuildParams.push_map(param, builder)
        elif isinstance(param, list):
            BuildParams.create_code_params_script_builder(param, builder)
            builder.emit_push_int(len(param))
            builder.emit(PACK)
        elif isinstance(param, Struct):
            BuildParams.push_struct(param, builder)
        elif isinstance(param, Address):
            builder.emit_push_bytearray(param.to_bytes())
        else:
            raise SDKException(ErrorCode.other_error('parameter type is error'))

    @staticmethod
    def push_map(dict_param: dict, builder: ParamsBuilder):
        builder.emit(NEWMAP)
        builder.emit(TOALTSTACK)
        for key, value in dict_param.items():
            builder.emit(DUPFROMALTSTACK)
            BuildParams.push_param(key, builder)
            BuildParams.push_param(value, builder)
            builder.emit(SETITEM)
        builder.emit(FROMALTSTACK)

    @staticmethod
    def push_struct(struct_param: Struct, builder: ParamsBuilder):
        builder.emit_push_int(0)
        builder.emit(NEWSTRUCT)
        builder.emit(TOALTSTACK)
        for item in struct_param.param_list:
            BuildParams.push_param(item, builder)
            builder.emit(DUPFROMALTSTACK)
            builder.emit(SWAP)
            builder.emit(APPEND)
        builder.emit(FROMALTSTACK)

    @staticmethod
    def get_map_bytes(param_dict: dict):
        builder = ParamsBuilder()
        builder.emit(BuildParams.Type.dict_type.value)
        builder.emit(utils.big_int_to_neo_bytearray(len(param_dict)))
        for key, value in param_dict.items():
            builder.emit(BuildParams.Type.bytearray_type.value)
            builder.emit_push_bytearray(str(key).encode())
            if isinstance(value, bytearray) or isinstance(value, bytes):
                builder.emit(BuildParams.Type.bytearray_type.value)
                builder.emit_push_bytearray(bytearray(value))
            elif isinstance(value, str):
                builder.emit(BuildParams.Type.bytearray_type.value)
                builder.emit_push_bytearray(value.encode())
            elif isinstance(value, bool):
                builder.emit(BuildParams.Type.bool_type.value)
                builder.emit_push_bool(value)
            elif isinstance(value, int):
                builder.emit(BuildParams.Type.int_type.value)
                builder.emit_push_int(int(value))
            else:
                raise Exception("param error")
        return builder.to_bytes()
