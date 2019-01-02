#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from ontology.crypto.digest import Digest
from ontology.utils.crypto_utils import str_to_bytes


def pbkdf2(seed: str or bytes, dk_len: int) -> bytes:
    """
    Derive one key from a seed.

    :param seed: the secret pass phrase to generate the keys from.
    :param dk_len: the length in bytes of every derived key.
    :return:
    """
    key = b''
    index = 1
    bytes_seed = str_to_bytes(seed)
    while len(key) < dk_len:
        key += Digest.sha256(b''.join([bytes_seed, index.to_bytes(4, 'big', signed=True)]))
        index += 1
    return key[:dk_len]
