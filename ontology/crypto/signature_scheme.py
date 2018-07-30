#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class SignatureScheme(Enum):
    SHA224withECDSA = 0
    SHA256withECDSA = 1
    SHA384withECDSA = 2
    SHA512withECDSA = 3
    SHA3_224withECDSA = 4
    SHA3_256withECDSA = 5
    SHA3_384withECDSA = 6
    SHA3_512withECDSA = 7
    RIPEMD160withECDSA = 8
    SM3withSM2 = 9
