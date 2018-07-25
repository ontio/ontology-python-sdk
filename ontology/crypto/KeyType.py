#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class KeyType(Enum):
    ECDSA = b'\x12'
    SM2 = b'\x13'
    EDDSA = b'\x14'

    @staticmethod
    def from_label(label: int):
        label = bytes([label])
        if KeyType.ECDSA.value == label:
            return KeyType.ECDSA.name
        elif KeyType.SM2.value == label:
            return KeyType.SM2.name
        elif KeyType.EDDSA.value == label:
            return KeyType.EDDSA.name

