#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.utils import utils


class TestUtil(unittest.TestCase):
    def test_get_random_bytes(self):
        try:
            length = -1
            utils.get_random_bytes(length)
        except ValueError:
            raised = True
            self.assertTrue(raised, 'Exception raised')
        length = 0
        self.assertEqual(len(utils.get_random_bytes(length)), length)
        length = 1
        self.assertEqual(len(utils.get_random_bytes(length)), length)
        length = 64
        self.assertEqual(len(utils.get_random_bytes(length)), length)
        length = 256
        self.assertEqual(len(utils.get_random_bytes(length)), length)
        length = 1024
        self.assertEqual(len(utils.get_random_bytes(length)), length)
        length = 2048
        self.assertEqual(len(utils.get_random_bytes(length)), length)

    def test_get_random_hex_str(self):
        try:
            length = -1
            utils.get_random_hex_str(length)
        except ValueError:
            raised = True
            self.assertTrue(raised, 'Exception raised')
        length = 0
        self.assertEqual(len(utils.get_random_hex_str(length)), length)
        length = 1
        self.assertEqual(len(utils.get_random_hex_str(length)), length)
        length = 64
        self.assertEqual(len(utils.get_random_hex_str(length)), length)
        length = 256
        self.assertEqual(len(utils.get_random_hex_str(length)), length)
        length = 1024
        self.assertEqual(len(utils.get_random_hex_str(length)), length)
        length = 2048
        self.assertEqual(len(utils.get_random_hex_str(length)), length)

    def test_bigint_to_neo_bytes(self):
        bs = utils.bigint_to_neo_bytes(-9175052165852779861)
        bs1 = utils.bigint_to_neo_bytes(9175052165852779861)
        bs2 = utils.bigint_to_neo_bytes(-9199634313818843819)
        bs3 = utils.bigint_to_neo_bytes(9199634313818843819)
        bs4 = utils.bigint_to_neo_bytes(-8380656)
        bs5 = utils.bigint_to_neo_bytes(8380656)
        bs6 = utils.bigint_to_neo_bytes(-8446192)
        bs7 = utils.bigint_to_neo_bytes(8446192)
        bs8 = utils.bigint_to_neo_bytes(-0)
        bs9 = utils.bigint_to_neo_bytes(0)
        self.assertEqual(bs.hex(), "abaaaaaaaaaaab80")
        self.assertEqual(bs1.hex(), "555555555555547f")
        self.assertEqual(bs2.hex(), "5555555555555480")
        self.assertTrue(bs3.hex() == "abaaaaaaaaaaab7f")
        self.assertTrue(bs4.hex() == "101f80")
        self.assertTrue(bs5.hex() == "f0e07f")
        self.assertTrue(bs6.hex() == "101f7fff")
        self.assertTrue(bs7.hex() == "f0e08000")


if __name__ == '__main__':
    unittest.main()
