#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.crypto.digest import Digest


class TestDigest(unittest.TestCase):
    def test_sha256(self):
        msg = b'Nobody inspects the spammish repetition'
        sha256_digest = b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
        hex_sha256_digest = '031edd7d41651593c5fe5c006fa5752b37fddff7bc4e843aa6af0c950f4b9406'
        self.assertEqual(sha256_digest, Digest.sha256(msg))
        self.assertEqual(hex_sha256_digest, Digest.sha256(msg, is_hex=True))

    def test_hash256(self):
        msg = b'Nobody inspects the spammish repetition'
        hash256_digest = b"\x9f>\x9eV\xb0\xe6K\x8a\xd0\xd8\xfd\xb4\x87\xfb\x0b\xfc\xfc\xd2\xb2x\xa3\xf2\x04\xdb\xc6t\x10\xdbL@\x90'"
        hex_hash256_digest = '9f3e9e56b0e64b8ad0d8fdb487fb0bfcfcd2b278a3f204dbc67410db4c409027'
        self.assertEqual(hash256_digest, Digest.hash256(msg))
        self.assertEqual(hex_hash256_digest, Digest.hash256(msg, is_hex=True))

    def test_hash160(self):
        msg = b'Nobody inspects the spammish repetition'
        hash160_digest = b'\x1c\x9b{H\x04\x9a\x8f\x98i\x9b\xca"\xa5\x85l^\xf5q\xcdh'
        hex_hash160_digest = '1c9b7b48049a8f98699bca22a5856c5ef571cd68'
        self.assertEqual(hash160_digest, Digest.hash160(msg))
        self.assertEqual(hex_hash160_digest, Digest.hash160(msg, is_hex=True))


if __name__ == '__main__':
    unittest.main()
