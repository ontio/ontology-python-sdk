"""
Copyright (C) 2018-2019 The ontology Authors
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

    def test_sha256_xor(self):
        h1 = Digest.sha256(int.to_bytes(1000, 2, 'little'), is_hex=True)
        h2 = Digest.sha256(int.to_bytes(89, 1, 'little'), is_hex=True)
        h = hex(int(h1, 16) ^ int(h2, 16))[2::]
        self.assertEqual('4307fbbb7e5b7c8f0339b060d171c49c881901d78ab712e60d805af9f9dc4ca1', h1)
        self.assertEqual('18f5384d58bcb1bba0bcd9e6a6781d1a6ac2cc280c330ecbab6cb7931b721552', h2)
        self.assertEqual('5bf2c3f626e7cd34a38569867709d986e2dbcdff86841c2da6eced6ae2ae59f3', h)


if __name__ == '__main__':
    unittest.main()
