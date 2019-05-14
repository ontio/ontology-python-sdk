#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2018 The ontology Authors
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

from tests import sdk, not_panic_exception


class TestMerkleVerifier(unittest.TestCase):
    def check_tx_in_block(self, height: int):
        block = sdk.rpc.get_block_by_height(height)
        for tx in block.get('Transactions', dict()):
            result = sdk.service.tx_verifier().verify_by_tx_hash(tx['Hash'])
            self.assertTrue(result)

    @not_panic_exception
    def test_verifier(self):
        try:
            sdk.rpc.connect_to_main_net()
            self.check_tx_in_block(0)
            sdk.rpc.connect_to_test_net()
            self.check_tx_in_block(0)
        finally:
            sdk.rpc.connect_to_test_net()

    @not_panic_exception
    def test_verify_by_tx_hash(self):
        tx_hash = 'bf74e9208c0a20ec417de458ab6c9d29c12c614e77fb943be4566c95fab61454'
        self.assertTrue(sdk.service.tx_verifier().verify_by_tx_hash(tx_hash))
        tx_hash_lst = ['c17e574dda17f268793757fab0c274d44427fa1b67d63113bd31e39b31d1a026',
                       '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e']
        for tx_hash in tx_hash_lst:
            try:
                sdk.rpc.connect_to_main_net()
                self.assertTrue(sdk.service.tx_verifier().verify_by_tx_hash(tx_hash))
            finally:
                sdk.rpc.connect_to_test_net()


if __name__ == '__main__':
    unittest.main()
