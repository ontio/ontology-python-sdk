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


if __name__ == '__main__':
    unittest.main()
