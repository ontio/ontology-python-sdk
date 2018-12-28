#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description:
    Derive key from a passphrase.

Usage:
    from ontology.crypto.scrypt import Scrypt
"""

from Cryptodome.Protocol import KDF

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Scrypt:
    def __init__(self, n=16384, r=8, p=8, dk_len=64):
        self.__n = n
        self.__r = r
        self.__p = p
        self.__dk_len = dk_len

    def __iter__(self):
        data = dict()
        data['n'] = self.__n
        data['r'] = self.__r
        data['p'] = self.__p
        data['dkLen'] = self.__dk_len
        for key, value in data.items():
            yield (key, value)

    @property
    def dk_len(self):
        return self.__dk_len

    @dk_len.setter
    def dk_len(self, dk_len: int):
        if not isinstance(dk_len, int):
            raise SDKException(ErrorCode.other_error('Invalid dkLen in scrypt.'))
        self.__dk_len = dk_len

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, n: int):
        if not isinstance(n, int):
            raise SDKException(ErrorCode.other_error('Invalid n in scrypt.'))
        self.__n = n

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, r: int):
        self.__r = r

    @property
    def p(self):
        return self.__p

    @p.setter
    def p(self, p):
        self.__p = p

    def generate_kd(self, password: str, salt: str):
        dk = KDF.scrypt(password, salt, self.__dk_len, self.__n, self.__r, self.__p)
        return dk
