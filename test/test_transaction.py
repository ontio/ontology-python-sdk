#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.core.transaction import Transaction
from ontology.utils import util


class TestTransaction(unittest.TestCase):
    def test_deserialize_from(self):
        tx_hex = "00d14b09645bf401000000000000204e0000000000004756c9dd829b2142883adbe1ae4f8689a1f673e97100c66b14dfa5e7" \
                 "b46640490f7fd2fcd82fe986e7e3f14a696a7cc814d2c124dd088190f709b684e0bc676d70c41b37766a7cc8516a7cc86c51" \
                 "c1087472616e736665721400000000000000000000000000000000000000010068164f6e746f6c6f67792e4e61746976652e" \
                 "496e766f6b65000242410113141b59b1a62dc3837da026bbd8d541529632377ab7749d4150b71b97ea39798220f15fa039d8" \
                 "521608a6db5ef582cbc6b007106ae86d30344986adb906af7d232103036c12be3726eb283d078dff481175e96224f0b0c632" \
                 "c7a37e10eb40fe6be889ac844101ceda8a7a51cf2ee0094f25bf422b12c0be0e40d6c27d4ef8d9d7fb853645881b9b9dfa20" \
                 "f377bcd2139e36f654812fdc15f8c98bd163548a04322e59ff52a9ff410186372e64013a6455c06f4aa65b5301c85c68fe77" \
                 "df8e6a5096041aa2baa7ff6bf99be09811ce5855ca11cc750c8ee561361a28ca9a41acbaa042d93c2a62f39769522103036c" \
                 "12be3726eb283d078dff481175e96224f0b0c632c7a37e10eb40fe6be88921020f9ce29ede5f0e271b67e61b2480dccc98c3" \
                 "aabad095c604ef9ab1d92a475c0a21035384561673e76c7e3003e705e4aa7aee67714c8b68d62dd1fb3221f48c5d3da053ae"

        tx = Transaction.deserialize_from(util.hex_to_bytes(tx_hex))
        self.assertGreaterEqual(tx.gas_limit, 0)
        self.assertGreaterEqual(tx.gas_price, 0)
        self.assertGreaterEqual(tx.nonce, 0)


if __name__ == '__main__':
    unittest.main()
