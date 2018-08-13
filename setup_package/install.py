#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

try:
    import Cryptodome
except ModuleNotFoundError:
    os.system('pip3 install pycryptodomex')
try:
    import cryptography
except ModuleNotFoundError:
    os.system('pip3 install cryptography')
try:
    import ecdsa
except ModuleNotFoundError:
    os.system('pip3 install ecdsa')
try:
    import base58
except ModuleNotFoundError:
    os.system('pip3 install base58')
try:
    import requests
except ModuleNotFoundError:
    os.system('pip3 install requests')
