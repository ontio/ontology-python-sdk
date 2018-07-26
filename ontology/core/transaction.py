from ontology.common.serialize import write_byte, write_uint32, write_uint64, write_var_uint
from ontology.crypto.Digest import Digest
from ontology.io.BinaryWriter import BinaryWriter
from ontology.io.MemoryStream import StreamManager
from ontology.utils.util import bytes_reader
from ontology.core.program import ProgramBuilder
from binascii import b2a_hex, a2b_hex

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
        writer.WriteBytes(bytes(self.payer))
        writer.WriteVarBytes(bytes(self.payload))
        writer.WriteVarInt(len(self.attributes))
        ms.flush()
        res = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        return res

    def hash256(self):
        tx_serial = self.serialize_unsigned()
        tx_serial = a2b_hex(tx_serial)
        r = Digest.hash256(tx_serial)
        #print(a2b_hex(b2a_hex(r))[::-1].hex())   [::-1]
        return a2b_hex(b2a_hex(r))

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
        return a2b_hex(temp)



