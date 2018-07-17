from ontology.vm.neo_vm.OP_code import PUSHDATA1, PUSHDATA2, PUSHDATA4, PUSHF, PUSHT, PACK, PUSH0, PUSH1, PUSHM1, \
    PUSHBYTES75, APPCALL, TAILCALL, SYSCALL
from ontology.utils import util


class ParamsBuilder:
    def __init__(self):
        self.code = bytearray()

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
        return self.emit(num)

    def emit_push_byte_array(self, data: bytearray):
        l = len(data)
        if l < int(PUSHBYTES75):
            self.write_byte(bytearray(l))
        elif l < 0x100:
            self.emit(PUSHDATA1)
            self.write_byte(bytearray(l))
        elif l < 0x10000:
            self.emit(PUSHDATA2)
            self.write_byte(bytearray(l))
            b = bytearray(2)
            b = util.put_uint16(b, l)
            self.write_byte(b)
        else:
            self.emit(PUSHDATA4)
            b = bytearray(4)
            b = util.put_uint32(b, l)
            self.write_byte(b)
        self.write_byte(data)

    def emit_push_call(self, address):
        self.emit(APPCALL)
        self.write_byte(address)

    def write_byte(self, value):
        if type(value) is bytearray:
            self.code += value
        elif type(value) is str:
            self.code += value.encode()
        elif type(value) is int:
            self.code += (bytes([value]))

    def get_builder(self):
        return self.code


builder = ParamsBuilder()
builder.emit(b'\x00')
builder.emit_push_bool(True)
builder.emit_push_integer(4)
util.print_byte_array(builder.get_builder())
