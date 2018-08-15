#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.utils import util


class TestUtil(unittest.TestCase):
    def test_get_random_bytes(self):
        try:
            length = -1
            util.get_random_bytes(length)
        except ValueError:
            raised = True
            self.assertTrue(raised, 'Exception raised')
        length = 0
        self.assertEqual(len(util.get_random_bytes(length)), length)
        length = 1
        self.assertEqual(len(util.get_random_bytes(length)), length)
        length = 64
        self.assertEqual(len(util.get_random_bytes(length)), length)
        length = 256
        self.assertEqual(len(util.get_random_bytes(length)), length)
        length = 1024
        self.assertEqual(len(util.get_random_bytes(length)), length)
        length = 2048
        self.assertEqual(len(util.get_random_bytes(length)), length)

    def test_get_random_str(self):
        try:
            length = -1
            util.get_random_str(length)
        except ValueError:
            raised = True
            self.assertTrue(raised, 'Exception raised')
        length = 0
        self.assertEqual(len(util.get_random_str(length)), length)
        length = 1
        self.assertEqual(len(util.get_random_str(length)), length)
        length = 64
        self.assertEqual(len(util.get_random_str(length)), length)
        length = 256
        self.assertEqual(len(util.get_random_str(length)), length)
        length = 1024
        self.assertEqual(len(util.get_random_str(length)), length)
        length = 2048
        self.assertEqual(len(util.get_random_str(length)), length)

    def test_bigint_to_neo_bytes(self):
        bs = util.bigint_to_neo_bytes(1)
        self.assertEqual(bs.hex(), '01')


if __name__ == '__main__':
    unittest.main()
