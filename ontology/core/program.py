from ontology.vm.op_code import PUSHBYTES75, PUSHBYTES1, PUSHDATA1, PUSHDATA2, PUSHDATA4, CHECKSIG
from ontology.io.BinaryWriter import BinaryWriter
from ontology.io.MemoryStream import StreamManager
from ontology.utils.util import bytes_reader
from ontology.vm.params_builder import ParamsBuilder


class ProgramBuilder(object):

    @staticmethod
    def program_from_params(sigs):
        code = bytearray()
        for sig in sigs:
            code += ProgramBuilder.push_bytes(sig)
        return code

    @staticmethod
    def program_from_pubkey(public_key):
        builder = ParamsBuilder()
        builder.emit_push_byte_array(public_key)
        builder.emit(CHECKSIG)
        return builder.to_array()

    @staticmethod
    def push_bytes(data):
        ms = StreamManager.GetStream()
        writer = BinaryWriter(ms)

        if len(data) == 0:
            raise ValueError("push data error: data is null")
        if len(data) <= int.from_bytes(PUSHBYTES75, 'little') + 1 - int.from_bytes(PUSHBYTES1, 'little'):
            num = len(data) + int.from_bytes(PUSHBYTES1, 'little') - 1
            writer.WriteByte(num)
        elif len(data) < 0x100:
            writer.WriteByte(PUSHDATA1)
            writer.WriteUInt8(len(data))
        elif len(data) < 0x10000:
            writer.WriteByte(PUSHDATA2)
            writer.WriteUInt16(len(data))
        else:
            writer.WriteByte(PUSHDATA4)
            writer.WriteUInt32(len(data))
        writer.WriteBytes(data)
        ms.flush()
        res = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        res = bytes_reader(res)
        return res

