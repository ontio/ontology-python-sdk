#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique
from cryptography.hazmat.primitives.asymmetric import ec


@unique
class Curve(Enum):
    P224 = ec.SECP224R1()
    P256 = ec.SECP256R1()
    P384 = ec.SECP384R1()
    P521 = ec.SECP521R1()

    @staticmethod
    def from_label(label: int):
        label = bytes([label])
        if Curve.P224.value == label:
            return Curve.P224.name
        elif Curve.P256.value == label:
            return Curve.P256.name
        elif Curve.P384.value == label:
            return Curve.P384.name
        elif Curve.P521.value == label:
            return Curve.P521.name
