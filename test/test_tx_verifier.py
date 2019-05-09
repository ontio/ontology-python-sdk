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

from test import sdk, not_panic_exception


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


if __name__ == '__main__':
    unittest.main()
