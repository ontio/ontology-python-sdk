#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.core.sig import Sig
from ontology.crypto.digest import Digest
from ontology.io.binary_writer import BinaryWriter
from ontology.io.binary_reader import BinaryReader
from ontology.io.memory_stream import StreamManager
from binascii import b2a_hex, a2b_hex


class Transaction(object):
    def __init__(self, version= 0, tx_type= None, nonce= None, gas_price= None, gas_limit= None, payer= None, payload= None,
                 attributes= None, sigs= None, hash= None):
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
        self.serialize_exclusive_data(writer)
        if hasattr(self, "payload"):
            writer.WriteVarBytes(bytes(self.payload))
        writer.WriteVarInt(len(self.attributes))
        ms.flush()
        res = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        return res

    def serialize_exclusive_data(self, writer):
        pass

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

    @staticmethod
    def deserialize_from(txbytes: bytes):
        ms = StreamManager.GetStream(txbytes)
        reader = BinaryReader(ms)
        tx = Transaction()
        tx.version = reader.ReadUInt8()
        tx.tx_type = reader.ReadUInt8()
        tx.nonce = reader.ReadUInt32()
        tx.gas_price = reader.ReadUInt64()
        tx.gas_limit = reader.ReadUInt64()
        tx.payer = reader.read_bytes(20)
        tx.payload = reader.ReadVarBytes()
        attri_len = reader.ReadVarInt()
        if attri_len is 0:
            tx.attributes = bytearray()
        sigs_len = reader.ReadVarInt()
        tx.sigs = []
        for i in range(sigs_len):
            tx.sigs.append(Sig.deserialize(reader))
        return tx




