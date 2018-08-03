#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.crypto.scrypt import Scrypt


class TestScrypt(unittest.TestCase):
    def test_set_dk_len(self):
        dk_len = 64
        scrypt = Scrypt()
        scrypt.set_dk_len(dk_len)
        self.assertEqual(dk_len, scrypt.get_dk_len())

    def test_set_n(self):
        n = 5
        scrypt = Scrypt()
        scrypt.set_n(n)
        self.assertEqual(n, scrypt.get_n())

    def test_set_p(self):
        n = 5
        scrypt = Scrypt()
        scrypt.set_n(n)
        self.assertEqual(n, scrypt.get_n())

    def test_set_r(self):
        r = 5
        scrypt = Scrypt(r)
        scrypt.set_r(r)
        self.assertEqual(r, scrypt.get_r())

    def test_generate_kd(self):
        scrypt = Scrypt()
        password = 'passwordtest'
        salt = "".join(map(chr, bytes([0xfa, 0xa4, 0x88, 0x3d])))
        kd1 = scrypt.generate_kd(password, salt)
        kd2 = bytes.fromhex(
            "9f0632e05eab137baae6e0a83300341531e8638612a08042d3a4074578869af1ccf5008e434d2cae9477f9e6e4c0571ab65a60e32e"
            "8c8fc356d95f64dd9717c9")
        self.assertEqual(kd1, kd2)


if __name__ == '__main__':
    unittest.main()
