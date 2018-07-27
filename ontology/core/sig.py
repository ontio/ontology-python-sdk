from ontology.common.serialize import write_byte, write_uint32, write_uint64, write_var_uint
from ontology.crypto.Digest import Digest
from ontology.io.BinaryWriter import BinaryWriter
from ontology.io.MemoryStream import StreamManager
from ontology.utils.util import bytes_reader
from ontology.core.program import ProgramBuilder
from binascii import b2a_hex, a2b_hex

class Sig(object):
    def __init__(self, public_keys, M, sig_data):
        self.public_keys = public_keys  # a list to save public keys
        self.M = M
        self.sig_data = sig_data

    def serialize(self)->bytes:
        invoke_script = ProgramBuilder.program_from_params(self.sig_data)
        if len(self.public_keys) == 0:
            raise ValueError("np public key in sig")

        verification_script = ProgramBuilder.program_from_pubkey(self.public_keys[0])
        ms = StreamManager.GetStream()
        writer = BinaryWriter(ms)
        writer.WriteVarBytes(invoke_script)
        writer.WriteVarBytes(verification_script)
        ms.flush()
        res = ms.ToArray()
        res = bytes_reader(res)
        StreamManager.ReleaseStream(ms)
        return res