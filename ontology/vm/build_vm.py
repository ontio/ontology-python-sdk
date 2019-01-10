#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.vm.op_code import *
from ontology.vm.params_builder import ParamsBuilder


def build_native_invoke_code(contract_address: bytes, version: bytes, method: str, params):
    builder = ParamsBuilder()
    build_neo_vm_param(builder, params)
    builder.emit_push_byte_array(method.encode())
    builder.emit_push_byte_array(contract_address)
    builder.emit_push_integer(int.from_bytes(version, 'little'))
    builder.emit(SYSCALL)
    builder.emit_push_byte_array(b'Ontology.Native.Invoke')
    return builder.to_bytes()


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
        builder.emit_push_byte_array(params.encode('utf-8'))
        # builder.emit_push_byte_array(util.bytes_reader(params.encode()))
    elif isinstance(params, bytes):
        builder.emit_push_byte_array(params)
    elif isinstance(params, bytearray):
        builder.emit_push_byte_array(params)
    elif isinstance(params, int):
        builder.emit_push_integer(params)
    elif isinstance(params, list):
        for p in params:
            build_neo_vm_param(builder, p)
        builder.emit_push_integer(len(params))
        builder.emit(PACK)
