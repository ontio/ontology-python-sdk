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

from test import acct1, acct2, acct3, sdk, not_panic_exception

from ontology.common.address import Address
from ontology.wallet.wallet import WalletData
from ontology.core.program import ProgramBuilder
from ontology.exception.exception import SDKException


class TestOntologySdk(unittest.TestCase):
    @not_panic_exception
    def test_add_multi_sign_transaction(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        m = 2
        b58_multi_address = Address.from_multi_pub_keys(m, pub_keys).b58encode()
        amount = 1
        gas_price = 500
        gas_limit = 20000
        tx_hash = sdk.native_vm.ont().transfer(acct2, b58_multi_address, amount, acct2, gas_price, gas_limit)
        self.assertEqual(64, len(tx_hash))
        tx_hash = sdk.native_vm.ong().transfer(acct2, b58_multi_address, amount, acct2, gas_price, gas_limit)
        self.assertEqual(64, len(tx_hash))
        b58_acct1_address = acct1.get_address_base58()
        b58_acct2_address = acct2.get_address_base58()
        self.assertEqual('ATyGGJBnANKFbf2tQMp4muUEZK7KuZ52k4', b58_multi_address)
        tx = sdk.native_vm.ong().new_transfer_tx(b58_acct1_address, b58_multi_address, amount, b58_acct1_address,
                                                 gas_price, gas_limit)
        tx.add_sign_transaction(acct1)

        tx = sdk.native_vm.ont().new_transfer_tx(b58_multi_address, b58_acct2_address, amount, b58_acct1_address,
                                                 gas_price, gas_limit)
        tx.sign_transaction(acct1)
        tx.add_multi_sign_transaction(m, pub_keys, acct1)
        tx.add_multi_sign_transaction(m, pub_keys, acct2)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))

    def test_sort_public_key(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        builder = ProgramBuilder()
        sort_pub_keys = builder.sort_public_keys(pub_keys)
        self.assertEqual("023cab3b268c4f268456a972c672c276d23a9c3ca3dfcfc0004d786adbf1fb9282", sort_pub_keys[0].hex())
        self.assertEqual("03d0fdb54acba3f81db3a6e16fa02e7ea3678bd205eb4ed2f1cfa8ab5e5d45633e", sort_pub_keys[1].hex())
        self.assertEqual("02e8e84be09b87985e7f9dfa74298f6bb7f70f85515afca7e041fe964334e4b6c1", sort_pub_keys[2].hex())


if __name__ == '__main__':
    unittest.main()
