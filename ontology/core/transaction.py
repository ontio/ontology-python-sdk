from ontology.crypto.digest import Digest
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from binascii import b2a_hex, a2b_hex


class Transaction(object):
    def __init__(self, version, tx_type, nonce, gas_price, gas_limit, payer, payload, attributes, sigs, hash):
        self.version = version
        self.tx_type = tx_type
        self.nonce = nonce
        self.gas_price = gas_price
        self.gas_limit = gas_limit
        self.payer = payer  # 20 bytes
        self.payload = payload
        self.attributes = attributes
        self.sigs = sigs  # Sig class array
        self.hash = hash  # 32 bytes

    def serialize_unsigned(self) -> bytes:
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

    def hash256(self) -> bytes:
        tx_serial = self.serialize_unsigned()
        tx_serial = a2b_hex(tx_serial)
        r = Digest.hash256(tx_serial)
        return a2b_hex(b2a_hex(r))

    def serialize(self) -> bytes:
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
