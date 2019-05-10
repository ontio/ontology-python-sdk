"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

import hmac
from typing import Union

import base58
import hashlib

from ecdsa import curves, SigningKey, VerifyingKey, ellipticcurve, ecdsa, util, numbertheory

from ontology.crypto.digest import Digest
from ontology.crypto.hd_key import HDKey, HARDENED_INDEX


class HDPublicKey(HDKey):
    __VERSION = 0x0488B21E

    def __init__(self, public_key: VerifyingKey, chain_code, index, depth, parent_fingerprint=b'\x00\x00\x00\x00'):
        super().__init__(public_key, chain_code, index, depth, parent_fingerprint)
        x_str = util.number_to_string(self._key.pubkey.point.x(), self._key.pubkey.order)
        if self._key.pubkey.point.y() % 2 == 0:
            self._compressed_key = util.b('\x02') + x_str
        else:
            self._compressed_key = util.b('\x03') + x_str

    def __bytes__(self):
        version = HDPublicKey.__VERSION
        return b''.join([version.to_bytes(length=4, byteorder='big'),
                         bytes([self._depth]),
                         self.parent_fingerprint,
                         self.index.to_bytes(length=4, byteorder='big'),
                         self.chain_code,
                         self.compressed_key])

    @property
    def compressed_key(self):
        """
        Byte string corresponding to a compressed representation of this public key.
        """
        return self._compressed_key

    @compressed_key.setter
    def compressed_key(self, b: bytes):
        self._compressed_key = b

    def to_hash160(self, is_compressed=True):
        return Digest.hash160(self.to_bytes(is_compressed))

    @property
    def identifier(self):
        """ Returns the identifier for the key.

        A key's identifier and fingerprint are defined as:
        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#key-identifiers

        In this case, it will return the RIPEMD-160 hash of the non-extended public key.
        """
        return self.to_hash160(is_compressed=True)

    def to_bytes(self, is_compressed=True):
        if is_compressed:
            return self.compressed_key
        else:
            return self.key.to_string()

    def hex(self, is_compressed=True):
        return self.to_bytes(is_compressed).hex()

    @classmethod
    def from_hex(cls, h):
        return cls.from_bytes(bytes.fromhex(h))

    @staticmethod
    def from_parent(parent_key, i):
        if i & HARDENED_INDEX:
            raise ValueError("Can't generate a hardened child key from a parent public key.")

        child = hmac.new(parent_key.chain_code,
                         parent_key.compressed_key + i.to_bytes(length=4, byteorder='big'),
                         hashlib.sha512).digest()
        child_left, child_right = child[:32], child[32:]
        if int.from_bytes(child_left, 'big') >= ecdsa.generator_256.order():
            return None

        temp_pri_key = SigningKey.from_string(string=child_left, curve=curves.NIST256p)

        ki = temp_pri_key.verifying_key.pubkey.point + parent_key.key.pubkey.point
        if ki == ellipticcurve.INFINITY:
            return None

        return HDPublicKey(public_key=VerifyingKey.from_public_point(point=ki, curve=curves.NIST256p),
                           chain_code=child_right,
                           index=i,
                           depth=parent_key.depth + 1,
                           parent_fingerprint=parent_key.fingerprint)

    @classmethod
    def from_bytes(cls, data: bytes):
        """ Generates either a HDPublicKey from the underlying bytes.

        The serialization must conform to the description in:
        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#serialization-format
        """
        if len(data) < 78:
            raise ValueError("b must be at least 78 bytes long.")

        version = int.from_bytes(data[:4], 'big')
        depth = data[4]
        parent_fingerprint = data[5:9]
        index = int.from_bytes(data[9:13], 'big')
        chain_code = data[13:45]
        key_bytes = data[45:78]

        if version != HDPublicKey.__VERSION:
            raise ValueError('invalid HD Public Key.')

        if key_bytes[0] != 0x02 and key_bytes[0] != 0x03:
            raise ValueError("First byte of public key must be 0x02 or 0x03!")

        # The curve of points satisfying y^2 = x^3 + a*x + b (mod p).
        curve = ecdsa.curve_256
        x = util.string_to_number(key_bytes[1:])
        y = (x * x * x + curve.a() * x + curve.b()) % curve.p()
        y = numbertheory.square_root_mod_prime(y, curve.p())
        if key_bytes[0] == 0x03:
            y = (y * -1) % curve.p()
        order = curves.NIST256p.order
        s_key = util.number_to_string(x, order) + util.number_to_string(y, order)

        public_key = VerifyingKey.from_string(string=s_key, curve=curves.NIST256p)
        rv = cls(
            public_key=public_key,
            chain_code=chain_code,
            index=index,
            depth=depth,
            parent_fingerprint=parent_fingerprint)
        return rv

    def b58encode(self):
        """ Generates a Base58Check encoding of this key.
        """
        return base58.b58encode_check(bytes(self))

    @classmethod
    def b58decode(cls, key: Union[str, bytes]):
        """ Decodes a Base58Check encoded key.

        The encoding must conform to the description in:
        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#serialization-format
        """
        return cls.from_bytes(base58.b58decode_check(key))
