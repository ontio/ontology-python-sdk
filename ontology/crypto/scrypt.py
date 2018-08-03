#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Cryptodome.Protocol import KDF



class Scrypt:
    def __init__(self, n=16384, r=8, p=8, dk_len=64):
        self.n = n
        self.r = r
        self.p = p
        self.dk_len = dk_len

    def set_dk_len(self, dk_len: int):
        self.dk_len = dk_len

    def get_dk_len(self):
        return self.dk_len

    def set_n(self, n):
        self.n = n

    def get_n(self):
        return self.n

    def set_r(self, r: int):
        self.r = r

    def get_r(self):
        return self.r

    def set_p(self, p):
        self.p = p

    def get_p(self):
        return self.p

    def generate_kd(self, password: str, salt: str):
        dk = KDF.scrypt(password, salt, self.dk_len, self.n, self.r, self.p)
        return dk
