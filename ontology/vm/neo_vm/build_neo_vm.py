from ontology.vm.neo_vm.params_builder import ParamsBuilder
from ontology.vm.neo_vm.OP_code import *
from ontology.utils import util


def build_native_invoke_code(contractAddres, cversion, method, params):
    builder = ParamsBuilder()
    build_neo_vm_param(builder, params)
    builder.emit_push_byte_array(method.encode())
    builder.emit_push_byte_array(contractAddres)
    builder.emit_push_integer(int.from_bytes(cversion, 'little'))
    builder.emit(SYSCALL)
    builder.emit_push_byte_array("Ontology.Native.Invoke".encode())
    return builder.get_builder()

def build_neo_vm_param(builder, params):
    if isinstance(params, dict):
        builder.emit_push_integer(0)
        builder.emit(NEWSTRUCT)
        builder.emit(TOALTSTACK)
        for i in params.values():
            build_neo_vm_param(builder, i)
            builder.emit(DUPFROMALTSTACK)
            builder.emit(SWAP)
            builder.emit(APPEND)
        builder.emit(FROMALTSTACK)
    elif isinstance(params, str):
        builder.emit_push_byte_array(util.bytes_reader(params.encode()))
    elif isinstance(params, bytes):
        builder.emit_push_byte_array(params)
    elif isinstance(params, bytearray):
        builder.emit_push_byte_array(params)
    elif isinstance(params, int):
        builder.emit_push_integer(params)
    elif isinstance(params, list):
        build_neo_vm_param(builder, params[0])
        builder.emit_push_integer(len(params))
        builder.emit(PACK)

