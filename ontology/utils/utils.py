#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
