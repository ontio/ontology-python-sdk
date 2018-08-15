#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import b2a_hex, a2b_hex

from ontology.core.sig import Sig
from ontology.crypto.digest import Digest
from ontology.io.binary_writer import BinaryWriter
from ontology.io.binary_reader import BinaryReader
from ontology.io.memory_stream import StreamManager


class Transaction(object):
    def __init__(self, version=0, tx_type=None, nonce=None, gas_price=None, gas_limit=None, payer=None, payload=None,
                 attributes=None, sigs=None, hash=None):
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
        writer.write_uint8(self.version)
        writer.write_uint8(self.tx_type)
        writer.write_uint32(self.nonce)
        writer.write_uint64(self.gas_price)
        writer.write_uint64(self.gas_limit)
        writer.write_bytes(bytes(self.payer))
        self.serialize_exclusive_data(writer)
        if hasattr(self, "payload"):
            writer.write_var_bytes(bytes(self.payload))
        writer.write_var_int(len(self.attributes))
        ms.flush()
        res = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        return res

    def serialize_exclusive_data(self, writer):
        pass

    def explorer_hash256(self) -> str:
        tx_serial = self.serialize_unsigned()
        tx_serial = a2b_hex(tx_serial)
        digest = Digest.hash256(tx_serial)
        if isinstance(digest, bytes):
            return b2a_hex(digest[::-1]).decode('ascii')
        else:
            return ''

    def hash256(self, is_hex: bool = False) -> bytes or str:
        tx_serial = self.serialize_unsigned()
        tx_serial = a2b_hex(tx_serial)
        r = Digest.hash256(tx_serial, is_hex)
        if isinstance(r, bytes) or isinstance(r, str):
            return r
        else:
            raise RuntimeError

    def serialize(self, is_hex: bool = False) -> bytes:
        ms = StreamManager.GetStream()
        writer = BinaryWriter(ms)
        writer.write_bytes(self.serialize_unsigned())
        writer.write_var_int(len(self.sigs))

        for sig in self.sigs:
            writer.write_bytes(sig.serialize())

        ms.flush()
        temp = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        if is_hex:
            return temp
        else:
            return a2b_hex(temp)

    @staticmethod
    def deserialize_from(txbytes: bytes):
        ms = StreamManager.GetStream(txbytes)
        reader = BinaryReader(ms)
        tx = Transaction()
        tx.version = reader.read_uint8()
        tx.tx_type = reader.read_uint8()
        tx.nonce = reader.read_uint32()
        tx.gas_price = reader.read_uint64()
        tx.gas_limit = reader.read_uint64()
        tx.payer = reader.read_bytes(20)
        tx.payload = reader.read_var_bytes()
        attri_len = reader.read_var_int()
        if attri_len is 0:
            tx.attributes = bytearray()
        sigs_len = reader.read_var_int()
        tx.sigs = []
        for i in range(sigs_len):
            tx.sigs.append(Sig.deserialize(reader))
        return tx
