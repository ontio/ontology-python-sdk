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

from typing import Union

from ontology.utils.crypto import to_bytes
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException

MAX_INDEX = 0xffffffff
HARDENED_INDEX = 0x80000000
MASTER_KEY_FINGERPRINT = b'\x00\x00\x00\x00'


class HDKey(object):
    def __init__(self, key, chain_code: bytes, index: int, depth: int, parent_fingerprint: bytes):
        if index < 0 or index > MAX_INDEX:
            raise SDKException(ErrorCode.hd_index_out_of_range)
        if not isinstance(chain_code, bytes):
            raise SDKException(ErrorCode.require_bytes_params)
        if depth == 0:
            parent_fingerprint = MASTER_KEY_FINGERPRINT
        self._key = key
        self._chain_code = chain_code
        self._depth = depth
        self._index = index
        self._parent_fingerprint = to_bytes(parent_fingerprint)

    @property
    def key(self):
        return self._key

    @property
    def chain_code(self):
        return self._chain_code

    @property
    def depth(self):
        return self._depth

    @property
    def index(self):
        return self._index

    @property
    def parent_fingerprint(self):
        return self._parent_fingerprint

    @property
    def is_master(self):
        """
        Whether this is a master node.
        """
        return self._depth == 0

    @property
    def hardened(self):
        """
        Whether this is a hardened node.

        Hardened nodes are those with indices >= HARDENED_INDEX.

        A hardened key is a key with index >= 2 ** 31, so we check that the MSB of a uint32 is set.
        """
        return self._index & HARDENED_INDEX

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: bytes):
        self._identifier = identifier

    @property
    def fingerprint(self):
        """ Returns the key's fingerprint, which is the first 4 bytes of its identifier(RIPEMD-160 hash).

        A key's identifier and fingerprint are defined as:
        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#key-identifiers
        """
        return self.identifier[:4]

    @staticmethod
    def parse_path(path: Union[str, bytes]) -> list:
        """parse a str path to list  and remove trailing '/'
        """
        if isinstance(path, str):
            p = path.rstrip("/").split("/")
        elif isinstance(path, bytes):
            p = path.decode('utf-8').rstrip("/").split("/")
        else:
            p = list(path)
        return p

    @staticmethod
    def from_path(root_key, path: Union[str, bytes] = "m/44'/1024'/0'"):
        """iterate path and generate extendkey from last extendkey
        the derive order is
            m/purpose'/coin_type'/account'/change/address_index
            mnemonic->seed->master_key
            root_key = m->purpose'->coin_type'->account'
            address_key = root_key->change_key->index_key
        """
        p = HDKey.parse_path(path)
        if p[0] == "m":
            if not root_key.is_master:
                raise SDKException(ErrorCode.hd_root_key_not_master_key)
            p = p[1:]
        keys = [root_key]
        for i in p:
            if isinstance(i, str):
                hardened = i[-1] == "'"
                index = int(i[:-1], 0) | HARDENED_INDEX if hardened else int(i, 0)
            else:
                index = i
            k = keys[-1]
            klass = k.__class__
            keys.append(klass.from_parent(k, index))
        return keys

    def __bytes__(self):
        pass

    @classmethod
    def from_bytes(cls, data: bytes):
        pass
