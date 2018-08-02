#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

try:
    import Cryptodome
except ModuleNotFoundError:
    os.system('pip install pycryptodomex')
try:
    import cryptography
except ModuleNotFoundError:
    os.system('pip install cryptography')
try:
    import ecdsa
except ModuleNotFoundError:
    os.system('pip install ecdsa')
try:
    import base58
except ModuleNotFoundError:
    os.system('pip install base58')
