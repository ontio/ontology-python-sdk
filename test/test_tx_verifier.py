#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

from test import sdk


class TestMerkleVerifier(unittest.TestCase):
    def check_tx_in_block(self, height: int):
        block = sdk.rpc.get_block_by_height(height)
        for tx in block.get('Transactions', dict()):
            result = sdk.service.tx_verifier().verify_by_tx_hash(tx['Hash'])
            self.assertTrue(result)

    def test_verifier(self):
        try:
            sdk.rpc.connect_to_main_net()
            self.check_tx_in_block(0)
            sdk.rpc.connect_to_test_net()
            self.check_tx_in_block(0)
        finally:
            sdk.rpc.connect_to_test_net()


if __name__ == '__main__':
    unittest.main()
