#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from test import acct1, acct2, acct3

from ontology.common.address import Address
from ontology.core.program import ProgramBuilder
from ontology.ont_sdk import OntologySdk
from ontology.wallet.wallet import WalletData

sdk = OntologySdk()
sdk.rpc.connect_to_test_net()


class TestOntologySdk(unittest.TestCase):
    def test_open_wallet(self):
        path = os.path.join(os.path.dirname(__file__), 'test.json')
        wallet = sdk.open_wallet(path)
        self.assertTrue(wallet, isinstance(wallet, WalletData))
        os.remove(path)

    def test_add_multi_sign_transaction(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        m = 2
        multi_address = Address.address_from_multi_pub_keys(m, pub_keys)
        b58_multi_address = multi_address.b58encode()
        b58_acct1_address = acct1.get_address_base58()
        b58_acct2_address = acct2.get_address_base58()
        amount = 1
        gas_price = 500
        gas_limit = 20000
        asset = sdk.native_vm.asset()
        self.assertEqual('ATyGGJBnANKFbf2tQMp4muUEZK7KuZ52k4', b58_multi_address)
        tx = asset.new_transfer_transaction('ong', b58_acct1_address, b58_multi_address, amount, b58_acct1_address,
                                            gas_limit, gas_price)
        sdk.add_sign_transaction(tx, acct1)

        tx = asset.new_transfer_transaction('ont', b58_multi_address, b58_acct2_address, amount, b58_acct1_address,
                                            gas_limit, gas_price)
        sdk.sign_transaction(tx, acct1)
        sdk.add_multi_sign_transaction(tx, m, pub_keys, acct1)
        sdk.add_multi_sign_transaction(tx, m, pub_keys, acct2)
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
