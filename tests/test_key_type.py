#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import unittest

from ontology.crypto.key_type import KeyType
from ontology.crypto.signature_scheme import SignatureScheme


class TestKeyType(unittest.TestCase):
    def test_from_signature_scheme(self):
        key_type = KeyType.from_signature_scheme(SignatureScheme.SM3withSM2)
        self.assertTrue(key_type is KeyType.SM2)
        ecdsa_scheme = [SignatureScheme.SHA224withECDSA, SignatureScheme.SHA256withECDSA,
                        SignatureScheme.SHA384withECDSA, SignatureScheme.SHA384withECDSA,
                        SignatureScheme.SHA512withECDSA, SignatureScheme.SHA3_224withECDSA,
                        SignatureScheme.SHA3_256withECDSA, SignatureScheme.SHA3_384withECDSA,
                        SignatureScheme.SHA3_512withECDSA, SignatureScheme.RIPEMD160withECDSA]
        for scheme in ecdsa_scheme:
            key_type = KeyType.from_signature_scheme(scheme)
            self.assertTrue(key_type is KeyType.ECDSA)
