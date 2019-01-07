#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from test import password, acct2, acct3, acct4

from ontology.crypto.curve import Curve
from ontology.crypto.signature import Signature
from ontology.utils.contract_data_parser import ContractDataParser
from ontology.smart_contract.native_contract.ontid import Attribute
from ontology.utils.contract_event_parser import ContractEventParser

from Cryptodome.Random.random import randint

from ontology.utils import utils
from ontology.ont_sdk import OntologySdk
from ontology.common.define import DID_ONT
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme

sdk = OntologySdk()
sdk.rpc.connect_to_test_net()
sdk.restful.connect_to_test_net()


class TestOntId(unittest.TestCase):
    def test_get_merkle_proof(self):
        ont_id = sdk.native_vm.ont_id()
        tx_hash = '7842ed25e4f028529e666bcecda2795ec49d570120f82309e3d5b94f72d30ebb'
        ont_id.get_merkle_proof(tx_hash)

    def test_get_public_keys(self):
        ont_id = 'did:ont:APywVQ2UKBtitqqJQ9JrpNeY8VFAnrZXiR'
        pub_keys = sdk.native_vm.ont_id().get_public_keys(ont_id)
        for pk in pub_keys:
            self.assertIn(ont_id, pk['PubKeyId'])
            self.assertEqual('ECDSA', pk['Type'])
            self.assertEqual('P256', pk['Curve'])
            self.assertEqual(66, len(pk['Value']))
        ont_id = 'did:ont:ANDfjwrUroaVtvBguDtrWKRMyxFwvVwnZD'
        pub_keys = sdk.native_vm.ont_id().get_public_keys(ont_id)
        for pk in pub_keys:
            self.assertIn(ont_id, pk['PubKeyId'])
            self.assertEqual('ECDSA', pk['Type'])
            self.assertEqual('P256', pk['Curve'])
            self.assertEqual(66, len(pk['Value']))

    def test_get_ddo(self):
        ont_id = 'did:ont:AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        ddo = sdk.native_vm.ont_id().get_ddo(ont_id)
        for pk in ddo['Owners']:
            self.assertIn(ont_id, pk['PubKeyId'])
            self.assertEqual('ECDSA', pk['Type'])
            self.assertEqual('P256', pk['Curve'])
            self.assertEqual(66, len(pk['Value']))
        self.assertEqual('AXBNi95PVZGP9gvYSgg8SjhqJxQFdwky9f', ddo['Recovery'])
        self.assertEqual(ont_id, ddo['OntId'])

    def test_new_registry_ont_id_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        hex_public_key = acct2.get_public_key_hex()
        b58_address = acct2.get_address_base58()
        acct_did = DID_ONT + b58_address
        gas_limit = 20000
        gas_price = 500
        tx = ont_id.new_registry_ont_id_transaction(acct_did, hex_public_key, b58_address, gas_limit, gas_price)
        tx.sign_transaction(acct2)
        self.assertEqual(64, len(tx.hash256_hex()))
        self.assertEqual(600, len(tx.serialize(is_hex=True)))
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            self.assertIn('already registered', e.args[1])

    def test_registry_ont_id(self):
        ont_id = sdk.native_vm.ont_id()
        label = 'label'
        try:
            identity = sdk.wallet_manager.create_identity(label, password)
            ctrl_acct = sdk.wallet_manager.get_control_account_by_index(identity.ont_id, 0, password)
        except SDKException as e:
            self.assertIn('Wallet identity exists', e.args[1])
            return
        gas_limit = 20000
        gas_price = 500
        try:
            ont_id.registry_ont_id(identity.ont_id, ctrl_acct, acct2, gas_limit, gas_price)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            self.assertIn('already registered', e.args[1])

    def test_add_and_remove_public_key(self):
        label = 'label'
        identity = sdk.wallet_manager.create_identity(label, password)
        ctrl_acct = sdk.wallet_manager.get_control_account_by_index(identity.ont_id, 0, password)
        gas_limit = 20000
        gas_price = 500
        tx_hash = sdk.native_vm.ont_id().registry_ont_id(identity.ont_id, ctrl_acct, acct3, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(6, 10))
        event = sdk.restful.get_smart_contract_event_by_tx_hash(tx_hash)
        hex_contract_address = sdk.native_vm.ont_id().contract_address
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertEqual(hex_contract_address, notify['ContractAddress'])
        self.assertEqual('Register', notify['States'][0])
        self.assertEqual(identity.ont_id, notify['States'][1])

        private_key = utils.get_random_bytes(32)
        public_key = Signature.ec_get_public_key_by_private_key(private_key, Curve.P256)
        hex_new_public_key = public_key.hex()

        tx_hash = sdk.native_vm.ont_id().add_public_key(identity.ont_id, ctrl_acct, hex_new_public_key, acct4,
                                                        gas_limit,
                                                        gas_price)
        time.sleep(randint(6, 10))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        hex_contract_address = sdk.native_vm.ont_id().contract_address
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertIn('PublicKey', notify['States'])
        self.assertIn('add', notify['States'])
        self.assertIn(identity.ont_id, notify['States'])
        self.assertIn(hex_new_public_key, notify['States'])
        try:
            sdk.native_vm.ont_id().add_public_key(identity.ont_id, ctrl_acct, hex_new_public_key, acct4, gas_limit,
                                                  gas_price)
        except SDKException as e:
            self.assertIn('already exists', e.args[1])
        tx_hash = sdk.native_vm.ont_id().remove_public_key(identity.ont_id, ctrl_acct, hex_new_public_key, acct3,
                                                           gas_limit, gas_price)
        time.sleep(randint(6, 10))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertIn('PublicKey', notify['States'])
        self.assertIn('remove', notify['States'])
        self.assertIn(identity.ont_id, notify['States'])
        self.assertIn(hex_new_public_key, notify['States'])
        try:
            sdk.native_vm.ont_id().remove_public_key(identity.ont_id, ctrl_acct, hex_new_public_key, acct3, gas_limit,
                                                     gas_price)
        except SDKException as e:
            self.assertIn('public key has already been revoked', e.args[1])

    def test_add_and_remove_attribute(self):
        ont_id = sdk.native_vm.ont_id()
        label = 'label'
        identity = sdk.wallet_manager.create_identity(label, password)
        ctrl_acct = sdk.wallet_manager.get_control_account_by_index(identity.ont_id, 0, password)
        gas_limit = 20000
        gas_price = 500
        tx_hash = sdk.native_vm.ont_id().registry_ont_id(identity.ont_id, ctrl_acct, acct3, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(6, 10))
        event = sdk.restful.get_smart_contract_event_by_tx_hash(tx_hash)
        hex_contract_address = sdk.native_vm.ont_id().contract_address
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertEqual(hex_contract_address, notify['ContractAddress'])
        self.assertEqual('Register', notify['States'][0])
        self.assertEqual(identity.ont_id, notify['States'][1])

        attribute = Attribute('hello', 'string', 'attribute')
        gas_limit = 20000
        gas_price = 500
        tx_hash = ont_id.add_attribute(identity.ont_id, ctrl_acct, attribute, acct2, gas_limit, gas_price)
        time.sleep(randint(6, 10))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertEqual('Attribute', notify['States'][0])
        self.assertEqual('add', notify['States'][1])
        self.assertEqual(identity.ont_id, notify['States'][2])
        self.assertEqual('hello', ContractDataParser.to_utf8_str(notify['States'][3][0]))

        attrib_key = 'hello'
        tx_hash = ont_id.remove_attribute(identity.ont_id, ctrl_acct, attrib_key, acct3, gas_limit, gas_price)
        time.sleep(randint(6, 10))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertEqual('Attribute', notify['States'][0])
        self.assertEqual('remove', notify['States'][1])
        self.assertEqual(identity.ont_id, notify['States'][2])
        self.assertEqual('hello', ContractDataParser.to_utf8_str(notify['States'][3]))
        try:
            ont_id.remove_attribute(identity.ont_id, ctrl_acct, attrib_key, acct3, gas_limit, gas_price)
        except SDKException as e:
            self.assertIn('attribute not exist', e.args[1])
        attrib_key = 'key'
        try:
            ont_id.remove_attribute(identity.ont_id, ctrl_acct, attrib_key, acct3, gas_limit, gas_price)
        except SDKException as e:
            self.assertIn('attribute not exist', e.args[1])

    def test_new_remove_attribute_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        hex_public_key = acct2.get_public_key_hex()
        b58_address = acct2.get_address_base58()
        acct_did = "did:ont:" + b58_address
        gas_limit = 20000
        gas_price = 500
        path = 'try'
        tx = ont_id.new_remove_attribute_transaction(acct_did, hex_public_key, path, b58_address, gas_limit, gas_price)
        tx.sign_transaction(acct2)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(tx.hash256_explorer(), tx_hash)
            time.sleep(randint(6, 10))
            notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
            self.assertEqual('Attribute', notify[0]['States'][0])
            self.assertEqual('remove', notify[0]['States'][1])
            self.assertEqual(acct_did, notify[0]['States'][2])
            self.assertEqual('try', bytes.fromhex(notify[0]['States'][3]).decode())
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            self.assertIn('attribute not exist', e.args[1])

    def test_add_attributes(self):
        ont_id = sdk.native_vm.ont_id()
        attribute = {'key': 'try', 'type': 'string', 'value': 'attribute'}
        attribute_list = [attribute]
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        try:
            identity = sdk.wallet_manager.create_identity_from_private_key('label', password, private_key)
        except SDKException as e:
            self.assertIn('identity exists', e.args[1])
            return
        gas_limit = 20000
        gas_price = 500
        tx_hash = ont_id.add_attribute(identity.ont_id, password, attribute_list, acct, gas_limit, gas_price)
        time.sleep(randint(6, 10))
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('Attribute', notify[0]['States'][0])
        self.assertEqual('add', notify[0]['States'][1])
        self.assertEqual(identity.ont_id, notify[0]['States'][2])
        self.assertEqual('try', bytes.fromhex(notify[0]['States'][3][0]).decode())

    def test_add_recovery(self):
        label = 'label'
        identity = sdk.wallet_manager.create_identity(label, password)
        ctrl_acct = sdk.wallet_manager.get_control_account_by_index(identity.ont_id, 0, password)
        gas_limit = 20000
        gas_price = 500
        tx_hash = sdk.native_vm.ont_id().registry_ont_id(identity.ont_id, ctrl_acct, acct3, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(6, 10))
        event = sdk.restful.get_smart_contract_event_by_tx_hash(tx_hash)
        hex_contract_address = sdk.native_vm.ont_id().contract_address
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertEqual(hex_contract_address, notify['ContractAddress'])
        self.assertEqual('Register', notify['States'][0])
        self.assertEqual(identity.ont_id, notify['States'][1])

        rand_private_key = utils.get_random_bytes(32).hex()
        recovery = Account(rand_private_key, SignatureScheme.SHA256withECDSA)
        b58_recovery_address = recovery.get_address_base58()
        gas_limit = 20000
        gas_price = 500
        tx_hash = sdk.native_vm.ont_id().add_recovery(identity.ont_id, ctrl_acct, b58_recovery_address, acct2,
                                                      gas_limit, gas_price)
        time.sleep(randint(6, 10))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertEqual(hex_contract_address, notify['ContractAddress'])
        self.assertEqual('Recovery', notify['States'][0])
        self.assertEqual('add', notify['States'][1])
        self.assertEqual(identity.ont_id, notify['States'][2])
        self.assertEqual(recovery.get_address_hex_reverse(), notify['States'][3])
        ddo = sdk.native_vm.ont_id().get_ddo(identity.ont_id)
        self.assertIn(ctrl_acct.get_ont_id(), ddo['Owners'][0]['PubKeyId'])
        self.assertEqual('ECDSA', ddo['Owners'][0]['Type'])
        self.assertEqual('P256', ddo['Owners'][0]['Curve'])
        self.assertEqual(ctrl_acct.get_public_key_hex(), ddo['Owners'][0]['Value'])
        self.assertEqual(0, len(ddo['Attributes']))
        self.assertEqual(recovery.get_address_base58(), ddo['Recovery'])
        self.assertEqual(identity.ont_id, ddo['OntId'])

        private_key = utils.get_random_bytes(32)
        public_key = Signature.ec_get_public_key_by_private_key(private_key, Curve.P256)
        hex_new_public_key = public_key.hex()
        tx_hash = sdk.native_vm.ont_id().add_public_key(identity.ont_id, recovery, hex_new_public_key,
                                                        acct2, gas_limit, gas_price, True)
        time.sleep(randint(6, 10))
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertEqual(hex_contract_address, notify['ContractAddress'])
        self.assertEqual('PublicKey', notify['States'][0])
        self.assertEqual('add', notify['States'][1])
        self.assertEqual(identity.ont_id, notify['States'][2])
        self.assertEqual(2, notify['States'][3])
        self.assertEqual(hex_new_public_key, notify['States'][4])

        ddo = sdk.native_vm.ont_id().get_ddo(identity.ont_id)
        self.assertIn(ctrl_acct.get_ont_id(), ddo['Owners'][0]['PubKeyId'])
        self.assertEqual('ECDSA', ddo['Owners'][0]['Type'])
        self.assertEqual('P256', ddo['Owners'][0]['Curve'])
        self.assertEqual(ctrl_acct.get_public_key_hex(), ddo['Owners'][0]['Value'])
        self.assertIn(ctrl_acct.get_ont_id(), ddo['Owners'][1]['PubKeyId'])
        self.assertEqual('ECDSA', ddo['Owners'][1]['Type'])
        self.assertEqual('P256', ddo['Owners'][1]['Curve'])
        self.assertEqual(hex_new_public_key, ddo['Owners'][1]['Value'])
        self.assertEqual(0, len(ddo['Attributes']))
        self.assertEqual(recovery.get_address_base58(), ddo['Recovery'])
        self.assertEqual(identity.ont_id, ddo['OntId'])
        self.assertEqual(b58_recovery_address, ContractDataParser.to_b58_address(ddo['Recovery']))

    def test_remove_attribute(self):
        ont_id = sdk.native_vm.ont_id()
        label = 'label'
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        identity = sdk.wallet_manager.create_identity_from_private_key(label, password, private_key)
        gas_limit = 20000
        gas_price = 500
        path = 'try'
        try:
            tx_hash = ont_id.remove_attribute(identity, password, path, acct2, gas_limit, gas_price)
            time.sleep(randint(6, 10))
            notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
            self.assertEqual('Attribute', notify[0]['States'][0])
            self.assertEqual('remove', notify[0]['States'][1])
            self.assertEqual(identity.ont_id, notify[0]['States'][2])
            self.assertEqual('try', bytes.fromhex(notify[0]['States'][3]).decode())
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            self.assertIn('attribute not exist', e.args[1])

    def test_new_add_remove_public_key_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        hex_public_key = acct.get_public_key_hex()
        rand_private_key = utils.get_random_bytes(32).hex()
        rand_acct = Account(rand_private_key, SignatureScheme.SHA256withECDSA)
        hex_new_public_key = rand_acct.get_public_key_hex()
        b58_address = acct.get_address_base58()
        acct_did = "did:ont:" + b58_address
        gas_limit = 20000
        gas_price = 500
        tx = ont_id.new_add_public_key_transaction(acct_did, hex_public_key, hex_new_public_key, b58_address, gas_limit,
                                                   gas_price)
        tx.sign_transaction(acct)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        time.sleep(randint(6, 10))
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('PublicKey', notify[0]['States'][0])
        self.assertEqual('add', notify[0]['States'][1])
        self.assertEqual(acct_did, notify[0]['States'][2])
        self.assertEqual(hex_new_public_key, notify[0]['States'][4])
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            self.assertIn('already exists', e.args[1])

        tx = ont_id.new_remove_public_key_transaction(acct_did, hex_public_key, hex_new_public_key, b58_address,
                                                      gas_limit, gas_price)
        tx.sign_transaction(acct)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        time.sleep(randint(6, 10))
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('PublicKey', notify[0]['States'][0])
        self.assertEqual('remove', notify[0]['States'][1])
        self.assertEqual(acct_did, notify[0]['States'][2])
        self.assertEqual(hex_new_public_key, notify[0]['States'][4])
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            self.assertIn('already been revoked', e.args[1])

    def test_new_add_recovery_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        gas_limit = 20000
        gas_price = 500
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        b58_address = acct.get_address_base58()
        acct_did = "did:ont:" + b58_address
        hex_public_key = acct.get_public_key_hex()
        rand_private_key = utils.get_random_bytes(32).hex()
        recovery = Account(rand_private_key, SignatureScheme.SHA256withECDSA)
        b58_recovery_address = recovery.get_address_base58()
        tx = ont_id.new_add_recovery_transaction(acct_did, hex_public_key, b58_recovery_address, b58_address, gas_limit,
                                                 gas_price)
        tx.sign_transaction(acct)
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            self.assertIn('already set recovery', e.args[1])


if __name__ == '__main__':
    unittest.main()
