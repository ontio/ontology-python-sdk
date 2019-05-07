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

    def generate_kd(self, password: bytes or str, salt: bytes or str) -> bytes:
        dk = KDF.scrypt(password, salt, self.__dk_len, self.__n, self.__r, self.__p)
        return dk
