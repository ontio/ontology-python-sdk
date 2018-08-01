from ontology.crypto.key_type import KeyType
from ontology.vm.op_code import PUSHBYTES75, PUSHBYTES1, PUSHDATA1, PUSHDATA2, PUSHDATA4, CHECKSIG, CHECKMULTISIG
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from ontology.utils.util import bytes_reader
from ontology.vm.params_builder import ParamsBuilder
from ecdsa import util
from ontology.common import define


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

    @staticmethod
    def compare_pubkey(o1):
        if KeyType.from_pubkey(o1) == KeyType.SM2:
            raise Exception("not supported")
        elif KeyType.from_pubkey(o1) == KeyType.ECDSA:
            x = o1[1:]
            return util.string_to_number(x)
        else:
            return str(o1)

    @staticmethod
    def sort_publickeys(publicKeys: []):
        return sorted(publicKeys, key=ProgramBuilder.compare_pubkey)

    @staticmethod
    def program_from_multi_pubkey(m: int, pubkeys: []):
        n = len(pubkeys)
        if  m <= 0 or m > n or n > define.MULTI_SIG_MAX_PUBKEY_SIZE:
            raise Exception("param error")
        builder = ParamsBuilder()
        builder.emit_push_integer(m)
        pubkeys = ProgramBuilder.sort_publickeys(pubkeys)
        for pubkey in pubkeys:
            builder.emit_push_byte_array(pubkey)
        builder.emit_push_integer(n)
        builder.emit(CHECKMULTISIG)
        return builder.to_array()






