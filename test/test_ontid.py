#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk

# rpc_address = "http://127.0.0.1:20336"
rpc_address = "http://polaris3.ont.io:20336"
sdk = OntologySdk()
sdk.rpc.set_address(rpc_address)
private_key = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key2 = "c19f16785b8f3543bbaf5e1dbb5d398dfa6c85aaad54fc9d71203ce83e505c07"
acc = Account(private_key, SignatureScheme.SHA256withECDSA)
acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
did = "did:ont:" + acc2.get_address_base58()


class TestOntId(unittest.TestCase):
    def test_new_registry_ontid_transaction(self):
        tx = sdk.native_vm().ont_id().new_registry_ontid_transaction(did, acc2.get_public_key(),
                                                                     acc.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc)
        self.assertEqual(len(tx.hash256(is_hex=True)), 64)
        self.assertEqual(len(tx.serialize(is_hex=True)), 806)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx.explorer_hash256(), tx_hash)

    def test_new_get_ddo_transaction(self):
        tx = sdk.native_vm().ont_id().new_get_ddo_transaction(did)
        ddo = sdk.rpc.send_raw_transaction_preexec(tx)
        estimate_ddo = "26010000002102d3d048aca7bdee582a611d0b8ac" \
                       "c45642950dc6167aee63abbdcd1a5781c63190014" \
                       "d2c124dd088190f709b684e0bc676d70c41b3776"
        self.assertEqual(estimate_ddo, ddo)
        parsed_ddo = sdk.native_vm().ont_id().parse_ddo(did, ddo)
        self.assertEqual(parsed_ddo['Owners'][0]['PubKeyId'][:len(did)], did)

    def test_new_add_attribute_transaction(self):
        attris = []
        attri = {}
        attri["key"] = "key1"
        attri["type"] = "string"
        attri["value"] = "value100"
        attris.append(attri)
        tx = sdk.native_vm().ont_id().new_add_attribute_transaction(did, acc2.get_public_key(), attris,
                                                                    acc.get_address_base58(), 20000,
                                                                    500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.explorer_hash256())

    def test_new_remove_attribute_transaction(self):
        tx = sdk.native_vm().ont_id().new_remove_attribute_transaction(did, acc2.get_public_key(), "key1",
                                                                       acc.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.explorer_hash256())

    def test_new_add_pubkey_transaction(self):
        tx = sdk.native_vm().ont_id().new_add_pubkey_transaction(did, acc2.get_public_key(), acc.get_public_key(),
                                                                 acc.get_address_base58(), 20000,
                                                                 500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.explorer_hash256())

    def test_new_remove_pubkey_transaction(self):
        tx = sdk.native_vm().ont_id().new_remove_pubkey_transaction(did, acc2.get_public_key(), acc.get_public_key(),
                                                                    acc.get_address_base58(), 20000,
                                                                    500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.explorer_hash256())

    def test_new_add_recovery_transaction(self):
        tx = sdk.native_vm().ont_id().new_add_rcovery_transaction(did, acc2.get_public_key(), acc.get_address_base58(),
                                                                  acc.get_address_base58(), 20000,
                                                                  500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.explorer_hash256())


if __name__ == '__main__':
    unittest.main()
