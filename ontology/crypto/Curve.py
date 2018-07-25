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

