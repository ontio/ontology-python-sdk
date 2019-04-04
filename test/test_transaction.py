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

from time import sleep

from test import acct1, acct2, acct3, sdk

from ontology.utils import utils
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.utils.contract_event import ContractEventParser


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

        tx = Transaction.deserialize_from(utils.hex_to_bytes(tx_hex))
        self.assertGreaterEqual(tx.gas_limit, 0)
        self.assertGreaterEqual(tx.gas_price, 0)
        self.assertGreaterEqual(tx.nonce, 0)

    def test_multi_serialize(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        m = 2
        multi_address = Address.address_from_multi_pub_keys(m, pub_keys)
        b58_multi_address = multi_address.b58encode()
        b58_acct1_address = acct1.get_address_base58()
        b58_acct2_address = acct2.get_address_base58()
        gas_price = 500
        gas_limit = 20000
        tx1 = sdk.native_vm.asset().new_transfer_transaction('ong', b58_multi_address, b58_acct2_address, 1000000000,
                                                             b58_acct1_address, gas_limit, gas_price)
        tx_bytes = tx1.serialize()
        tx2 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx1), dict(tx2))

        tx2.sign_transaction(acct1)
        tx_bytes = tx2.serialize()
        tx3 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx2), dict(tx3))
        tx3.add_multi_sign_transaction(m, pub_keys, acct1)
        tx_bytes = tx3.serialize()
        tx4 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx3), dict(tx4))
        tx4.add_multi_sign_transaction(m, pub_keys, acct2)
        tx_bytes = tx4.serialize()
        tx5 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx4), dict(tx5))
        tx_hash = sdk.rpc.send_raw_transaction(tx5)
        self.assertEqual(64, len(tx_hash))
        sleep(6)
        event = sdk.rpc.get_contract_event_by_tx_hash(tx_hash)
        contract_address = '0200000000000000000000000000000000000000'
        notify = ContractEventParser.get_notify_list_by_contract_address(event, contract_address)
        for event in notify:
            self.assertEqual(event['States'][0], 'transfer')
        multi_address = Address.address_from_multi_pub_keys(m, pub_keys[::-1])
        b58_multi_address = multi_address.b58encode()
        b58_acct1_address = acct1.get_address_base58()
        b58_acct2_address = acct2.get_address_base58()
        tx1 = sdk.native_vm.asset().new_transfer_transaction('ong', b58_multi_address, b58_acct2_address, 100000,
                                                             b58_acct1_address, gas_limit, gas_price)
        tx_bytes = tx1.serialize()
        tx2 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx1), dict(tx2))

        tx2.sign_transaction(acct1)
        tx_bytes = tx2.serialize()
        tx3 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx2), dict(tx3))
        tx3.add_multi_sign_transaction(m, pub_keys, acct1)
        tx_bytes = tx3.serialize()
        tx4 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx3), dict(tx4))
        tx4.add_multi_sign_transaction(m, pub_keys, acct2)
        tx_bytes = tx4.serialize()
        tx5 = Transaction.deserialize_from(tx_bytes)
        self.assertEqual(dict(tx4), dict(tx5))
        tx_hash = sdk.rpc.send_raw_transaction(tx5)
        self.assertEqual(64, len(tx_hash))
        sleep(6)
        event = sdk.rpc.get_contract_event_by_tx_hash(tx_hash)
        contract_address = '0200000000000000000000000000000000000000'
        notify = ContractEventParser.get_notify_list_by_contract_address(event, contract_address)
        for event in notify:
            self.assertEqual(event['States'][0], 'transfer')


if __name__ == '__main__':
    unittest.main()
