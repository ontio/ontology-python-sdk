from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from ontology.utils.util import bytes_reader
from ontology.core.program import ProgramBuilder


class Sig(object):
    def __init__(self, public_keys=None, M=0, sig_data=None):
        self.public_keys = public_keys  # a list to save public keys
        self.M = M
        self.sig_data = sig_data

    def serialize(self) -> bytes:
        invoke_script = ProgramBuilder.program_from_params(self.sig_data)
        if len(self.public_keys) == 0:
            raise ValueError("no public key in sig")

        if len(self.public_keys) == 1:
            verification_script = ProgramBuilder.program_from_pubkey(self.public_keys[0])
        else:
            verification_script = ProgramBuilder.program_from_multi_pubkey(self.M, self.public_keys)
        ms = StreamManager.GetStream()
        writer = BinaryWriter(ms)
        writer.WriteVarBytes(invoke_script)
        writer.WriteVarBytes(verification_script)
        ms.flush()
        res = ms.ToArray()
        res = bytes_reader(res)
        StreamManager.ReleaseStream(ms)
        return res

    @staticmethod
    def deserialize_from(sigbytes: bytes):
        ms = StreamManager.GetStream(sigbytes)
        reader = BinaryReader(ms)
        return Sig.deserialize(reader)

    @staticmethod
    def deserialize(reader: BinaryReader):

        invocation_script = reader.ReadVarBytes()
        verification_script = reader.ReadVarBytes()
        sig = Sig()
        sig.sig_data = ProgramBuilder.get_param_info(invocation_script)
        info = ProgramBuilder.get_program_info(verification_script)

        sig.public_keys = info.pubkeys
        sig.M = info.m
        return sig



