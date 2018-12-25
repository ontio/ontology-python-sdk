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
        self.assertEqual('AcAR5ZhtxiS66ydXrKWTZMXo13LcsvgYnD', b58_multi_address)
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
        p = ProgramBuilder()
        a = p.sort_publickeys(pub_keys)
        self.assertEqual("03036c12be3726eb283d078dff481175e96224f0b0c632c7a37e10eb40fe6be889", a[0].hex())
        self.assertEqual("020f9ce29ede5f0e271b67e61b2480dccc98c3aabad095c604ef9ab1d92a475c0a", a[1].hex())
        self.assertEqual("035384561673e76c7e3003e705e4aa7aee67714c8b68d62dd1fb3221f48c5d3da0", a[2].hex())


if __name__ == '__main__':
    unittest.main()
