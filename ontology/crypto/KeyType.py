#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class KeyType(Enum):
    ECDSA = b'0x12'
    SM2 = b'0x13'
    EDDSA = b'0x14'

