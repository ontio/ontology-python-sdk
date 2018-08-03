#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import a2b_hex
from unittest import TestCase

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.program import ProgramBuilder
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk

sdk = OntologySdk()
rpc_address = "http://polaris3.ont.io:20336"
sdk.rpc.set_address(rpc_address)
private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
acc = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acc2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
acc3 = Account(a2b_hex(private_key3.encode()), SignatureScheme.SHA256withECDSA)
pubkeys = [acc.get_public_key(), acc2.get_public_key(), acc3.get_public_key()]
multi_addr = Address.address_from_multi_pubKeys(2, pubkeys)


class TestOntologySdk(TestCase):
    def test_open_wallet(self):
        a = sdk.open_wallet("./wallet/test.json")
        print(a)

    def test_add_multi_sign_transaction(self):
        print(multi_addr.to_base58())
        tx = sdk.native_vm().asset().new_transfer_transaction("ong", acc.get_address_base58(), multi_addr.to_base58(),
                                                              100000000,
                                                              acc.get_address_base58(), 20000, 500)
        sdk.add_sign_transaction(tx, acc)

        tx = sdk.native_vm().asset().new_transfer_transaction("ont", multi_addr.to_base58(), acc2.get_address_base58(),
                                                              1,
                                                              acc.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx, acc)
        sdk.add_multi_sign_transaction(tx, 2, pubkeys, acc)
        sdk.add_multi_sign_transaction(tx, 2, pubkeys, acc2)
        sdk.rpc.send_raw_transaction(tx)

    def test_sort_public_key(self):
        pub_keys = [acc.get_public_key(), acc2.get_public_key(), acc3.get_public_key()]
        p = ProgramBuilder()
        a = p.sort_publickeys(pub_keys)
        self.assertEqual("03036c12be3726eb283d078dff481175e96224f0b0c632c7a37e10eb40fe6be889", a[0].hex())
        self.assertEqual("020f9ce29ede5f0e271b67e61b2480dccc98c3aabad095c604ef9ab1d92a475c0a", a[1].hex())
        self.assertEqual("035384561673e76c7e3003e705e4aa7aee67714c8b68d62dd1fb3221f48c5d3da0", a[2].hex())


