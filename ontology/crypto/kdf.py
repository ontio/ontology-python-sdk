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

from ontology.crypto.digest import Digest
from ontology.utils.crypto import to_bytes


def pbkdf2(seed: str or bytes, dk_len: int) -> bytes:
    """
    Derive one key from a seed.

    :param seed: the secret pass phrase to generate the keys from.
    :param dk_len: the length in bytes of every derived key.
    :return:
    """
    key = b''
    index = 1
    bytes_seed = to_bytes(seed)
    while len(key) < dk_len:
        key += Digest.sha256(b''.join([bytes_seed, index.to_bytes(4, 'big', signed=True)]))
        index += 1
    return key[:dk_len]
