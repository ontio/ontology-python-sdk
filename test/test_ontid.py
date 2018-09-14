#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import unittest

from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.exception.exception import SDKException
from ontology.ont_sdk import OntologySdk

rpc_address = "http://127.0.0.1:20336"
# rpc_address = 'http://polaris3.ont.io:20336'
sdk = OntologySdk()
sdk.rpc.set_address(rpc_address)
private_key1 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
private_key2 = "c19f16785b8f3543bbaf5e1dbb5d398dfa6c85aaad54fc9d71203ce83e505c07"
private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
acc1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
did = "did:ont:" + acc2.get_address_base58()
password = "111111"
identity = sdk.wallet_manager.create_identity_from_private_key("sss", "111111", private_key2)



class TestOntId(unittest.TestCase):
    def test_new_registry_ontid_transaction(self):
        tx = sdk.native_vm().ont_id().new_registry_ontid_transaction(did, acc2.get_public_key(),
                                                                     acc1.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc1)
        self.assertEqual(len(tx.hash256_hex()), 64)
        self.assertEqual(len(tx.serialize(is_hex=True)), 806)
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] ' \
                  'service execute error!: [Invoke] Native serivce function execute error!: ' \
                  'register ONT ID error: already registered'
            self.assertEqual(msg, e.args[1])

    def test_send_registry(self):
        identity = sdk.wallet_manager.create_identity("ss", "111111")
        txhash = sdk.native_vm().ont_id().send_registry_ontid(identity,"111111",acc1,20000,0)
        print(txhash)
        time.sleep(3)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))

    def test_send_get_ddo(self):
        print(sdk.native_vm().ont_id().send_get_ddo(identity.ont_id))

    def test_new_get_ddo_transaction(self):
        tx = sdk.native_vm().ont_id().new_get_ddo_transaction(did)
        out_ddo = sdk.rpc.send_raw_transaction_pre_exec(tx)
        estimate_ddo = "26010000002102d3d048aca7bdee582a611d0b8acc45642950dc6167aee63abbdcd1a5781c6319"
        self.assertEqual(estimate_ddo[2:], out_ddo[2:len(estimate_ddo)])
        parsed_ddo = sdk.native_vm().ont_id().parse_ddo(did, out_ddo)
        self.assertEqual(parsed_ddo['Owners'][0]['PubKeyId'][:len(did)], did)

    def test_new_add_attribute_transaction(self):
        attris = []
        attri = {}
        attri["key"] = "key1"
        attri["type"] = "string"
        attri["value"] = "value100"
        attris.append(attri)
        tx = sdk.native_vm().ont_id().new_add_attribute_transaction(did, acc2.get_public_key(), attris,
                                                                    acc1.get_address_base58(), 20000,
                                                                    500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.hash256_explorer())

    def test_send_add_attributes(self):
        attris = []
        attri = {}
        attri["key"] = "key1"
        attri["type"] = "string"
        attri["value"] = "value100"
        attris.append(attri)
        txhash = sdk.native_vm().ont_id().send_add_attribute(identity, "111111", attris, acc1, 20000, 0)
        time.sleep(3)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))

    def test_remove_attribute(self):
        txhash = sdk.native_vm().ont_id().send_remove_attribute(identity,password,"key1",acc1,20000,0)
        time.sleep(6)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))

    def test_new_remove_attribute_transaction(self):
        tx = sdk.native_vm().ont_id().new_remove_attribute_transaction(did, acc2.get_public_key(), "key1",
                                                                       acc1.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx_hash, tx.hash256_explorer())

    def test_new_add_pubkey_transaction(self):
        tx = sdk.native_vm().ont_id().new_add_pubkey_transaction(did, acc1.get_public_key(), acc3.get_public_key(),
                                                                 acc3.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc1)
        tx = sdk.add_sign_transaction(tx, acc3)
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute error!:' \
                  ' [Invoke] Native serivce function execute error!: add key failed: already exists'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

    def test_add_public_key(self):
        txhash = sdk.native_vm().ont_id().send_add_pubkey(identity,password,acc1.serialize_public_key().hex(),acc1,20000,0)
        time.sleep(6)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))

    def test_add_recovery(self):
        txhash = sdk.native_vm().ont_id().send_add_rcovery(identity, password, acc3.get_address_base58(), acc1, 20000, 0)
        time.sleep(6)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))

    def test_add_public_key_by_recovery(self):
        txhash = sdk.native_vm().ont_id().send_add_pubkey_by_recovery(identity.ont_id,acc3,acc3.serialize_public_key().hex(),acc1,20000,0)
        time.sleep(6)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))

    def test_remove_public_key(self):
        txhash = sdk.native_vm().ont_id().send_remove_pubkey(identity, password, acc1.serialize_public_key().hex(), acc1,
                                                          20000, 0)
        time.sleep(6)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))

    def test_new_remove_pubkey_transaction(self):
        tx = sdk.native_vm().ont_id().new_remove_pubkey_transaction(did, acc1.get_public_key(), acc3.get_public_key(),
                                                                    acc3.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc1)
        tx = sdk.add_sign_transaction(tx, acc3)
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute error!:' \
                  ' [Invoke] Native serivce function execute error!: remove key failed: public key has already' \
                  ' been revoked'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

    def test_new_add_recovery_transaction(self):
        tx = sdk.native_vm().ont_id().new_add_rcovery_transaction(did, acc1.get_public_key(), acc3.get_address_base58(),
                                                                  acc2.get_address_base58(), 20000,
                                                                  500)
        tx = sdk.sign_transaction(tx, acc2)
        tx = sdk.add_sign_transaction(tx, acc1)
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute ' \
                  'error!: [Invoke] Native serivce function execute error!: add recovery failed: already ' \
                  'set recovery'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])


if __name__ == '__main__':
    unittest.main()
