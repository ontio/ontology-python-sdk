#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
