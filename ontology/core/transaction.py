from ontology.common.serialize import write_byte, write_uint32, write_uint64, write_var_uint
from ontology.crypto.Digest import Digest
from ontology.io.BinaryWriter import BinaryWriter
from ontology.io.MemoryStream import StreamManager
from ontology.utils.util import bytes_reader
from ontology.core.program import ProgramBuilder


class Transaction(object):
    def __init__(self, version, tx_type, nonce, gas_price, gas_limit, payer, payload, attributes, sigs, hash):
        self.version = version
        self.tx_type = tx_type
        self.nonce = nonce
        self.gas_price = gas_price
        self.gas_limit = gas_limit
        self.payer = payer  # common.address [20]bytes
        self.payload = payload
        self.attributes = attributes
        self.sigs = sigs  # Sig class array
        self.hash = hash  # [32]byte

    def serialize_unsigned(self):
        ms = StreamManager.GetStream()
        writer = BinaryWriter(ms)
        writer.WriteUInt8(self.version)
        writer.WriteUInt8(self.tx_type)
        writer.WriteUInt32(self.nonce)
        writer.WriteUInt64(self.gas_price)
        writer.WriteUInt64(self.gas_limit)
        writer.WriteBytes(bytes(self.payer.encode()))
        writer.WriteBytes(bytes(self.payload))
        writer.WriteVarInt(len(self.attributes))
        ms.flush()
        res = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        return res

    def hash256(self):
        tx_serial = self.serialize_unsigned()
        tx_serial = bytes_reader(tx_serial)
        r = Digest.hash256(tx_serial)
        return r

    def serialize(self):
        ms = StreamManager.GetStream()
        writer = BinaryWriter(ms)
        writer.WriteBytes(self.serialize_unsigned())
        writer.WriteVarInt(len(self.sigs))

        for sig in self.sigs:
            writer.WriteBytes(sig.serialize())

        ms.flush()
        temp = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        return bytes_reader(temp)


class Sig(object):
    def __init__(self, public_keys, M, sig_data):
        self.public_keys = public_keys  # a list to save public keys
        self.M = M
        self.sig_data = sig_data

    def serialize(self):
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
