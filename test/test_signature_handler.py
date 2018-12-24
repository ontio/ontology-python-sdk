#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.account.account import Account
from ontology.crypto.signature_handler import SignatureHandler

from ontology.crypto.key_type import KeyType
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk

acc = Account("75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf")
sdk = OntologySdk()


class TestSignatureHandler(unittest.TestCase):
    def test_signature_data(self):
        sig = sdk.signature_data(acc, "sss".encode())
        self.assertTrue(sdk.verify_signature(acc.serialize_public_key(), "sss".encode(), sig))

    def testTx(self):
        tx = sdk.native_vm.asset().new_transfer_transaction("ont",acc.get_address_base58(),acc.get_address_base58(),10,acc.get_address_base58(),20000,0)
        sdk.add_sign_transaction(tx, acc)
        self.assertTrue(sdk.verify_signature(tx.sigs[0].public_keys[0], tx.hash256_bytes(), tx.sigs[0].sig_data[0]))

    def test_generateSignature(self):
        acc = Account("75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf")
        sigaa = "01cf157a48216bfcd455a97a39c0ad65bd1b27d1da07965b19848146045c9f2e5a12f905a5ee0923412d589e615a5d6954c58cade367dce67fcf13eaa82c12e87a"
        byte_signature = acc.generate_signature("sss".encode(), SignatureScheme.SHA256withECDSA)

        handler = SignatureHandler(KeyType.ECDSA, SignatureScheme.SHA256withECDSA)

        res = handler.verify_signature(acc.serialize_public_key(), "sss".encode(), bytearray.fromhex(sigaa))
        self.assertTrue(res)