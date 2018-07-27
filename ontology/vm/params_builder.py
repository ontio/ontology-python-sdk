from ontology.vm.op_code import PUSHDATA1, PUSHDATA2, PUSHDATA4, PUSHF, PUSHT, PACK, PUSH0, PUSH1, PUSHM1, \
    PUSHBYTES75, APPCALL, TAILCALL, SYSCALL
from ontology.common.serialize import put_uint16, put_uint32
from ontology.io.MemoryStream import MemoryStream
from binascii import b2a_hex, a2b_hex

class ParamsBuilder:
    def __init__(self):
        self.ms = MemoryStream()

    def emit(self, op):
        self.write_byte(op)

    def emit_push_bool(self, data: bool):
        return self.emit(PUSHT) if data else self.emit(PUSHF)

    def emit_push_integer(self, num):
        if num == -1:
            return self.emit(PUSHM1)
        elif num == 0:
            return self.emit(PUSH0)
        elif num > 0 and num < 16:
            return self.emit(int.from_bytes(PUSH1, 'little') - 1 + num)
        elif num < 0x10000:
            return self.emit_push_byte_array(num.to_bytes(2, "little"))
        else:
            return self.emit_push_byte_array(num.to_bytes(4, "little"))
        return self.emit(num)

    def emit_push_byte_array(self, data):
        l = len(data)
        if l < int.from_bytes(PUSHBYTES75, 'little'):
            self.write_byte(bytearray([l]))
        elif l < 0x100:
            self.emit(PUSHDATA1)
            self.write_byte(bytearray([l]))
        elif l < 0x10000:
            self.emit(PUSHDATA2)
            self.write_byte(len(data).to_bytes(2, "little"))
        else:
            self.emit(PUSHDATA4)
            self.write_byte(len(data).to_bytes(4, "little"))
        self.write_byte(data)

    def emit_push_call(self, address):
        self.emit(APPCALL)
        self.write_byte(address)

    def write_byte(self, value):
        if isinstance(value, bytearray) or isinstance(value, bytes):
            self.ms.write(value)
        elif isinstance(value, str):
            self.ms.write(value.encode())
        elif isinstance(value, int):
           self.ms.write(bytes([value]))
        else:
            raise TypeError

    def to_array(self):
        return a2b_hex(self.ms.ToArray())