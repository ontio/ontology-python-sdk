from enum import Enum
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.utils import util
from ontology.vm.op_code import PACK, NEWMAP, TOALTSTACK, DUPFROMALTSTACK, SETITEM, FROMALTSTACK
from ontology.vm.params_builder import ParamsBuilder


class BuildParams(object):
    class Type(Enum):
        bytearraytype = 0x00
        booltype = 0x01
        integertype = 0x02
        arraytype = 0x80
        structtype = 0x81
        maptype = 0x82

    @staticmethod
    def serialize_abi_function(abi_func: AbiFunction):
        param_list = list()
        param_list.append(bytes(abi_func.name.encode()))
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
        print('param_list:', param_list)
        return BuildParams.create_code_params_script(param_list)

    @staticmethod
    def create_code_params_script(param_list: []) -> bytearray:
        builder = ParamsBuilder()
        length = len(param_list)
        for j in range(length):
            i = length - 1 - j
            if isinstance(param_list[i], bytearray) or isinstance(param_list[i], bytes):
                builder.emit_push_byte_array(param_list[i])
            elif isinstance(param_list[i], str):
                builder.emit_push_byte_array(str.encode(param_list[i]))
            elif isinstance(param_list[i], bool):
                builder.emit_push_bool(param_list[i])
            elif isinstance(param_list[i], int):
                builder.emit_push_integer(param_list[i])
            elif isinstance(param_list[i], dict):
                # builder.emit_push_byte_array(BuildParams.get_map_bytes(dict(param_list[i])))
                BuildParams.push_map(param_list[i], builder)
            elif isinstance(param_list[i], list):
                BuildParams.create_code_params_script_builder(param_list[i], builder)
                builder.emit_push_integer(len(param_list[i]))
                builder.emit(PACK)
        return bytearray(builder.to_array())

    @staticmethod
    def create_code_params_script_builder(param_list: list, builder: ParamsBuilder):
        length = len(param_list)
        for j in range(length):
            i = length - 1 - j
            if isinstance(param_list[i], bytearray) or isinstance(param_list[i], bytes):
                builder.emit_push_byte_array(param_list[i])
            elif isinstance(param_list[i], str):
                builder.emit_push_byte_array(bytes(param_list[i].encode()))
            elif isinstance(param_list[i], int):
                builder.emit_push_integer(param_list[i])
            elif isinstance(param_list[i], bool):
                builder.emit_push_bool(param_list[i])
            elif isinstance(param_list[i], dict):
                # builder.emit_push_byte_array(BuildParams.get_map_bytes(dict(param_list[i])))
                BuildParams.push_map(param_list[i], builder)
            elif isinstance(param_list[i], list):
                BuildParams.create_code_params_script_builder(param_list[i], builder)
                builder.emit_push_integer(len(param_list[i]))
                builder.emit(PACK)
        return builder.to_array()

    @staticmethod
    def push_param(param, builder: ParamsBuilder):
        if isinstance(param, bytearray) or isinstance(param, bytes):
            builder.emit_push_byte_array(param)
        elif isinstance(param, str):
            builder.emit_push_byte_array(bytes(param.encode()))
        elif isinstance(param, bool):
            builder.emit_push_bool(param)
        elif isinstance(param, int):
            builder.emit_push_integer(param)
        elif isinstance(param, dict):
            # builder.emit_push_byte_array(BuildParams.get_map_bytes(dict(param)))
            BuildParams.push_map(param, builder)
        elif isinstance(param, list):
            BuildParams.create_code_params_script_builder(param, builder)
            builder.emit_push_integer(len(param))
            builder.emit(PACK)

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
    def get_map_bytes(param_dict: dict):
        builder = ParamsBuilder()
        builder.emit(BuildParams.Type.maptype.value)
        builder.emit(util.bigint_to_neo_bytes(len(param_dict)))
        for key, value in param_dict.items():
            builder.emit(BuildParams.Type.bytearraytype.value)
            builder.emit_push_byte_array(str(key).encode())
            if isinstance(value, bytearray) or isinstance(value, bytes):
                builder.emit(BuildParams.Type.bytearraytype.value)
                builder.emit_push_byte_array(bytearray(value))
            elif isinstance(value, str):
                builder.emit(BuildParams.Type.bytearraytype.value)
                builder.emit_push_byte_array(value.encode())
            elif isinstance(value, bool):
                builder.emit(BuildParams.Type.booltype.value)
                builder.emit_push_bool(value)
            elif isinstance(value, int):
                builder.emit(BuildParams.Type.integertype.value)
                builder.emit_push_integer(int(value))
            else:
                raise Exception("param error")
        return builder.to_array()
