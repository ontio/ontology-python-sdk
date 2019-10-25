from typing import Union

from ontology.vm.op_code import PUSHBYTES75, PUSHDATA1, PUSHDATA2, PUSHDATA4

from ontology.exception.error_code import ErrorCode

from ontology.exception.exception import SDKException

from ontology.io.memory_stream import MemoryStream


class BaseParamsBuilder(object):
    def __init__(self):
        self.ms = MemoryStream()

    def clear_up(self):
        self.ms.clean_up()

    def write_bytes(self, value: bytearray or bytes or str or int):
        if isinstance(value, bytearray) or isinstance(value, bytes):
            self.ms.write(value)
        elif isinstance(value, str):
            self.ms.write(value.encode('utf-8'))
        elif isinstance(value, int):
            self.ms.write(bytes([value]))
        else:
            raise SDKException(ErrorCode.param_err('type error, write byte failed.'))

    def emit(self, op):
        self.write_bytes(op)

    def push_bytearray(self, data: Union[bytes, bytearray]):
        data_len = len(data)
        if data_len < int.from_bytes(PUSHBYTES75, 'little'):
            self.write_bytes(bytearray([data_len]))
        elif data_len < 0x100:
            self.emit(PUSHDATA1)
            self.write_bytes(bytearray([data_len]))
        elif data_len < 0x10000:
            self.emit(PUSHDATA2)
            self.write_bytes(len(data).to_bytes(2, "little"))
        else:
            self.emit(PUSHDATA4)
            self.write_bytes(len(data).to_bytes(4, "little"))
        self.write_bytes(data)

    def to_bytes(self) -> bytes:
        return self.ms.to_bytes()

    def to_bytearray(self) -> bytearray:
        return bytearray(self.ms.to_bytes())
