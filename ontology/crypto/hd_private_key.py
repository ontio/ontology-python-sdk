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

import base58
import hashlib

from os import urandom
from typing import Union
from mnemonic import Mnemonic
from ecdsa import ecdsa, curves, SigningKey, util

from ontology.crypto.hd_key import HDKey, HARDENED_INDEX
from ontology.utils.crypto import to_bytes
from ontology.crypto.hd_public_key import HDPublicKey


class HDPrivateKey(HDKey):
    __VERSION = 0x0488ADE4

    def __init__(self, key, chain_code: bytes, index: int, depth: int, parent_fingerprint: bytes = b''):
        if isinstance(key, int):
            key = util.number_to_string(key, curves.NIST256p.order)
        private_key = SigningKey.from_string(string=key, curve=curves.NIST256p)
        super().__init__(private_key, chain_code, index, depth, parent_fingerprint)
        self._public_key = HDPublicKey(
            public_key=self._key.verifying_key,
            chain_code=self._chain_code,
            index=self._index,
            depth=self._depth,
            parent_fingerprint=self._parent_fingerprint
        )

    def __bytes__(self):
        version = HDPrivateKey.__VERSION
        key_bytes = b'\x00' + self.key.to_string()
        return b''.join([version.to_bytes(length=4, byteorder='big'),
                         bytes([self._depth]),
                         self._parent_fingerprint,
                         self._index.to_bytes(length=4, byteorder='big'),
                         self._chain_code,
                         key_bytes
                         ])

    def hex(self):
        return self._key.to_string().hex()

    @property
    def identifier(self):
        """ Returns the identifier for the key.

        A key's identifier and fingerprint are defined as:
        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#key-identifiers

        In this case, it will return the RIPEMD-160 hash of the corresponding public key.

        """
        return self.public_key.identifier

    @property
    def public_key(self):
        """
        Returns the public key associated with this private key.
        """
        return self._public_key

    @staticmethod
    def master_key_from_mnemonic(mnemonic: str, passphrase: str = ''):
        """Generates a master key from a mnemonic.

        The mnemonic sentence representing the seed from which to generate the master key.

        The passphrase representing the password if one was used.

        """
        seed = Mnemonic.to_seed(mnemonic, passphrase)
        return HDPrivateKey.master_key_from_seed(seed)

    @staticmethod
    def master_key_from_seed(seed: Union[bytes, str]):
        """
        Generates a master private key from a provided seed which should be a string of bytes or a hex string.
        """
        bytes_seed_name = b"Nist256p1 seed"

        S = to_bytes(seed)
        child = hmac.new(bytes_seed_name, S, hashlib.sha512).digest()
        child_left, child_right = child[:32], child[32:]
        parse_child_left = int.from_bytes(child_left, 'big')
        if parse_child_left == 0 or parse_child_left >= ecdsa.generator_256.order():
            raise ValueError("Bad seed, resulting in invalid key!")

        return HDPrivateKey(key=child_left, chain_code=child_right, index=0, depth=0)

    def b58encode(self) -> str:
        """
        Generates a Base58Check encoding of this private key.
        """
        return base58.b58encode_check(bytes(self)).decode('ascii')

    @classmethod
    def b58decode(cls, key):
        """
        Decodes a Base58Check encoding private-key.
        """
        return cls.from_bytes(base58.b58decode_check(key))

    @classmethod
    def from_bytes(cls, data: bytes):
        """Generates either a HDPrivateKey or HDPublicKey from the underlying bytes.

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

        if version != HDPrivateKey.__VERSION:
            raise ValueError('invalid HD Public Key.')

        if key_bytes[0] != 0:
            raise ValueError("First byte of private key must be 0x00!")

        rv = HDPrivateKey(key=key_bytes[1:],
                          chain_code=chain_code,
                          index=index,
                          depth=depth,
                          parent_fingerprint=parent_fingerprint)

        return rv

    @staticmethod
    def master_key_from_entropy(passphrase='', strength=128):
        """Generates a master key from system entropy.

        strength is the amount of entropy desired, which should be a multiple of 32 between 128 and 256.

        passphrase is an optional passphrase for the generated mnemonic string.
        """
        if strength % 32 != 0:
            raise ValueError("strength must be a multiple of 32")
        if strength < 128 or strength > 256:
            raise ValueError("strength should be >= 128 and <= 256")
        entropy = urandom(strength // 8)
        m = Mnemonic(language='english')
        n = m.to_mnemonic(entropy)
        return HDPrivateKey.master_key_from_seed(
            Mnemonic.to_seed(n, passphrase)), n

    @staticmethod
    def from_parent(parent_key, i):
        """Derives a child private key from a parent private key.

        It is not possible to derive a child private key from a public parent key.
        """
        if not isinstance(parent_key, HDPrivateKey):
            raise TypeError("parent_key must be an HDPrivateKey object.")

        curve_g_n = parent_key._key.verifying_key.curve.generator.order()

        if i & HARDENED_INDEX:
            hmac_data = b'\x00' + bytes(parent_key._key.to_string()) + i.to_bytes(length=4, byteorder='big')
        else:
            hmac_data = parent_key.public_key.compressed_key + i.to_bytes(length=4, byteorder='big')

        child = hmac.new(parent_key._chain_code, hmac_data, hashlib.sha512).digest()
        child_left, child_right = child[:32], child[32:]

        parse_Il = int.from_bytes(child_left, 'big')

        if parse_Il >= curve_g_n:
            return None

        child_key = (parse_Il + parent_key._key.privkey.secret_multiplier) % curve_g_n

        if child_key == 0:
            # Incredibly unlucky choice
            return None

        return HDPrivateKey(
            key=child_key,
            chain_code=child_right,
            index=i,
            depth=parent_key._depth + 1,
            parent_fingerprint=parent_key.fingerprint
        )
