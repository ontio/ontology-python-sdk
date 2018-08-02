#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

try:
    import Cryptodome
except ModuleNotFoundError:
    os.system('pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple pycryptodomex')
try:
    import cryptography
except ModuleNotFoundError:
    os.system('pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple cryptography')
try:
    import ecdsa
except ModuleNotFoundError:
    os.system('pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple ecdsa')
try:
    import base58
except ModuleNotFoundError:
    os.system('pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple base58')
