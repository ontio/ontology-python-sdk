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

from Cryptodome import Random


def get_random_bytes(length: int) -> bytes:
    """
    This interface is used to get a random byte string of the desired length.

    :param length: the desired length of a random byte string.
    :return: a random byte string of the desired length.
    """
    return Random.get_random_bytes(length)


def get_random_hex_str(length: int) -> str:
    """

    :param length:
    :return: a random hexadecimal string of the desired length.
    """
    return Random.get_random_bytes(length).hex()[:length]


def hex_to_bytes(value: str) -> bytearray:
    return bytearray.fromhex(value)


def to_array_reverse(arr: bytearray) -> bytearray:
    bytearray.reverse(arr)
    return arr


def bytes_reader(b):
    res = bytearray()
    for i in range(len(b) // 2):
        res += bytearray.fromhex(b[2 * i:2 * i + 2].decode())
    return res
