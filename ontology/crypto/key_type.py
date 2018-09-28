#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class KeyType(Enum):

    ECDSA = b'\x12'
    SM2 = b'\x13'
    EDDSA = b'\x14'

    def __init__(self, b: int):
        self.label = b

    def get_label(self):
        return self.label

    @staticmethod
    def from_label(label: int):
        label = bytes([label])
        if KeyType.ECDSA.value == label:
            return KeyType.ECDSA
        elif KeyType.SM2.value == label:
            return KeyType.SM2
        elif KeyType.EDDSA.value == label:
            return KeyType.EDDSA

    @staticmethod
    def from_pubkey(pubkey: []):
        if len(pubkey) == 33:
            return KeyType.ECDSA
        else:
            return KeyType.from_label(pubkey[0])



