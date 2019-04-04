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

import hashlib


class Digest(object):
    @staticmethod
    def __sha256(msg: bytes, is_hex: bool = False) -> bytes or str:
        m = hashlib.sha256()
        m.update(msg)
        if is_hex:
            return m.hexdigest()
        else:
            return m.digest()

    @staticmethod
    def ripemd160(msg: bytes, is_hex: bool = False) -> bytes or str:
        h = hashlib.new('ripemd160')
        h.update(msg)
        if is_hex:
            return h.hexdigest()
        else:
            return h.digest()

    @staticmethod
    def sha256(msg: bytes, offset: int = 0, length: int = 0, is_hex: bool = False) -> bytes or str:
        if offset != 0 and len(msg) > offset + length:
            msg = msg[offset:offset + length]
        return Digest.__sha256(msg, is_hex)

    @staticmethod
    def hash256(msg: bytes, is_hex: bool = False) -> bytes or str:
        digest = Digest.sha256(Digest.sha256(msg), is_hex=is_hex)
        return digest

    @staticmethod
    def hash160(msg: bytes, is_hex: bool = False) -> bytes or str:
        digest = Digest.ripemd160(Digest.__sha256(msg), is_hex)
        return digest
