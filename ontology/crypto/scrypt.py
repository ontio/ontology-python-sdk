#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Crypto.Protocol import KDF



class Scrypt:
    def __init__(self, n=16384, r=8, p=8, dk_len=64):
        self.__n = n
        self.__r = r
        self.__p = p
        self.__dk_len = dk_len

    def set_dk_len(self, dk_len: int):
        self.__dk_len = dk_len

    def get_dk_len(self):
        return self.__dk_len

    def set_n(self, n):
        self.__n = n

    def get_n(self):
        return self.__n

    def set_r(self, r: int):
        self.__r = r

    def get_r(self):
        return self.__r

    def set_p(self, p):
        self.__p = p

    def get_p(self):
        return self.__p

    def generate_kd(self, password: bytes, salt: bytes):
        dk = KDF.scrypt(password, salt, self.__dk_len, self.__n, self.__r, self.__p)
        return dk
