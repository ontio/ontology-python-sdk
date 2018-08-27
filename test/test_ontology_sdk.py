#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from binascii import a2b_hex
from unittest import TestCase

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.program import ProgramBuilder
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk
from ontology.wallet.wallet import WalletData

rpc_address = "http://polaris3.ont.io:20336"
sdk = OntologySdk()
sdk.rpc.set_address(rpc_address)

private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"

acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)

pub_keys = [acct1.get_public_key(), acct2.get_public_key(), acct3.get_public_key()]
multi_address = Address.address_from_multi_pub_keys(2, pub_keys)


class TestOntologySdk(TestCase):
    def test_open_wallet(self):
        path = os.path.join(os.getcwd(), 'test.json')
        wallet = sdk.open_wallet(path)
        self.assertTrue(wallet, isinstance(wallet, WalletData))
        os.remove(path)

    def test_add_multi_sign_transaction(self):
        self.assertEqual(multi_address.b58encode(), 'AcAR5ZhtxiS66ydXrKWTZMXo13LcsvgYnD')
        tx = sdk.native_vm().asset().new_transfer_transaction("ong", acct1.get_address_base58(),
                                                              multi_address.b58encode(),
                                                              100000000,
                                                              acct1.get_address_base58(), 20000, 500)
        sdk.add_sign_transaction(tx, acct1)

        tx = sdk.native_vm().asset().new_transfer_transaction("ont", multi_address.b58encode(),
                                                              acct2.get_address_base58(),
                                                              1,
                                                              acct1.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx, acct1)
        sdk.add_multi_sign_transaction(tx, 2, pub_keys, acct1)
        sdk.add_multi_sign_transaction(tx, 2, pub_keys, acct2)
        sdk.rpc.send_raw_transaction(tx)

    def test_sort_public_key(self):
        pub_keys = [acct1.get_public_key(), acct2.get_public_key(), acct3.get_public_key()]
        p = ProgramBuilder()
        a = p.sort_publickeys(pub_keys)
        self.assertEqual("03036c12be3726eb283d078dff481175e96224f0b0c632c7a37e10eb40fe6be889", a[0].hex())
        self.assertEqual("020f9ce29ede5f0e271b67e61b2480dccc98c3aabad095c604ef9ab1d92a475c0a", a[1].hex())
        self.assertEqual("035384561673e76c7e3003e705e4aa7aee67714c8b68d62dd1fb3221f48c5d3da0", a[2].hex())
