#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import unittest

from ontology.crypto.scrypt import Scrypt


class TestScrypt(unittest.TestCase):
    def test_set_dk_len(self):
        dk_len = 64
        scrypt = Scrypt()
        scrypt.dk_len = dk_len
        self.assertEqual(dk_len, scrypt.dk_len)

    def test_set_n(self):
        n = 5
        scrypt = Scrypt()
        scrypt.n = n
        self.assertEqual(n, scrypt.n)

    def test_set_p(self):
        n = 5
        scrypt = Scrypt()
        scrypt.n = n
        self.assertEqual(n, scrypt.n)

    def test_set_r(self):
        r = 5
        scrypt = Scrypt(r)
        scrypt.r = r
        self.assertEqual(r, scrypt.r)

    def test_generate_kd(self):
        scrypt = Scrypt()
        salt = ''.join(map(chr, bytes([0xfa, 0xa4, 0x88, 0x3d])))
        kd = scrypt.generate_kd('passwordtest', salt)
        target_kd = '9f0632e05eab137baae6e0a83300341531e8638612a08042d3a4074578869af1' \
                    'ccf5008e434d2cae9477f9e6e4c0571ab65a60e32e8c8fc356d95f64dd9717c9'
        target_kd = binascii.a2b_hex(target_kd)
        self.assertEqual(target_kd, kd)


if __name__ == '__main__':
    unittest.main()
