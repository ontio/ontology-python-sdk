#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import a2b_hex
from unittest import TestCase

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.program import ProgramBuilder
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk

sdk = OntologySdk.get_instance()
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
    # def test_open_wallet(self):
    #     a = sdk.open_wallet("./wallet/test.json")
    #     print(a)

    def test_bb(self):
        print(sdk.rpc.get_balance(acc.get_address_base58()))
        print(sdk.rpc.get_balance(multi_addr.to_base58()))

    def test_add_multi_sign_transaction(self):
        print(multi_addr.to_base58())
        # tx = sdk.native_vm.asset.new_transfer_transaction("ong",acc.get_address_base58() ,multi_addr.to_base58(), 100000000,
        #                                                   acc.get_address_base58(), 20000, 500)
        # sdk.add_sign_transaction(tx, acc)

        tx = sdk.native_vm.asset.new_transfer_transaction("ont", multi_addr.to_base58(), acc2.get_address_base58(), 1,
                                                          acc.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx, acc)
        sdk.add_multi_sign_transaction(tx, 2, pubkeys, acc)
        sdk.add_multi_sign_transaction(tx, 2, pubkeys, acc2)
        sdk.rpc.send_raw_transaction(tx)

    def test_aa(self):
        pubkeys = [acc.get_public_key(), acc2.get_public_key(), acc3.get_public_key()]
        p = ProgramBuilder()
        a = p.sort_publickeys(pubkeys)
        print(a[0].hex())
        print(a[1].hex())
        print(a[2].hex())
