#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import json
from binascii import b2a_hex, a2b_hex

from ontology.common.address import Address
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

    def __iter__(self):
        data = dict()
        data['version'] = self.version
        data['txType'] = self.tx_type
        data['nonce'] = self.nonce
        data['gasPrice'] = self.gas_price
        data['gasLimit'] = self.gas_limit
        data['payer'] = Address(self.payer).b58encode()
        data['payload'] = binascii.b2a_hex(self.payload).decode('ascii')
        data['attributes'] = binascii.b2a_hex(self.attributes).decode('ascii')
        data['sigs'] = list()
        for sig in self.sigs:
            data['sigs'].append(dict(sig))
        for key, value in data.items():
            yield (key, value)

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

    def hash256_explorer(self) -> str:
        tx_serial = self.serialize_unsigned()
        tx_serial = a2b_hex(tx_serial)
        digest = Digest.hash256(tx_serial)
        if isinstance(digest, bytes):
            return b2a_hex(digest[::-1]).decode('ascii')
        else:
            return ''

    def hash256_bytes(self) -> bytes:
        tx_serial = self.serialize_unsigned()
        tx_serial = a2b_hex(tx_serial)
        r = Digest.hash256(tx_serial, False)
        if isinstance(r, bytes):
            return r
        else:
            raise RuntimeError

    def hash256_hex(self) -> str:
        tx_serial = self.serialize_unsigned()
        tx_serial = a2b_hex(tx_serial)
        r = Digest.hash256(tx_serial, True)
        if isinstance(r, str):
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
        bytes_tx = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        if is_hex:
            return bytes_tx
        else:
            return a2b_hex(bytes_tx)

    @staticmethod
    def deserialize_from(bytes_tx: bytes):
        ms = StreamManager.GetStream(bytes_tx)
        reader = BinaryReader(ms)
        tx = Transaction()
        tx.version = reader.read_uint8()
        tx.tx_type = reader.read_uint8()
        tx.nonce = reader.read_uint32()
        tx.gas_price = reader.read_uint64()
        tx.gas_limit = reader.read_uint64()
        tx.payer = reader.read_bytes(20)
        tx.payload = reader.read_var_bytes()
        attribute_len = reader.read_var_int()
        if attribute_len is 0:
            tx.attributes = bytearray()
        sigs_len = reader.read_var_int()
        tx.sigs = []
        for i in range(0, sigs_len):
            tx.sigs.append(Sig.deserialize(reader))
        return tx
