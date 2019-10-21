from enum import IntEnum, unique

from ontology.exception.error_code import ErrorCode

from ontology.exception.exception import SDKException


@unique
class VmType(IntEnum):
    Neo = 1
    Wasm = 3

    @classmethod
    def from_int(cls, value: int):
        if value == 1:
            return cls.Neo
        if value == 3:
            return cls.Wasm
        raise SDKException(ErrorCode.unknown_vm_type)
