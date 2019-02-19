#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.utils.contract_data import ContractDataParser


class TestContractDataParser(unittest.TestCase):
    def test_bigint_to_neo_bytes(self):
        value_list = [9175052165852779861, -9175052165852779861, 9199634313818843819, -9199634313818843819, 8380656,
                      -8380656, 8446192, -8446192, 0]
        for value in value_list:
            neo_bytearray = ContractDataParser.big_int_to_neo_bytearray(value)
            self.assertTrue(isinstance(neo_bytearray, bytearray))
            neo_value = ContractDataParser.neo_bytearray_to_big_int(neo_bytearray)
            self.assertEqual(value, neo_value)