#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from test import acct1, acct2, acct3, acct4

from ontology.utils import utils
from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme

sdk = OntologySdk()
sdk.rpc.connect_to_test_net()


class TestOntId(unittest.TestCase):
    def test_new_registry_ont_id_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        hex_public_key = acct2.get_public_key_hex()
        b58_address = acct2.get_address_base58()
        acct_did = "did:ont:" + b58_address
        gas_limit = 20000
        gas_price = 500
        tx = ont_id.new_registry_ont_id_transaction(acct_did, hex_public_key, b58_address, gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, acct2)
        self.assertEqual(64, len(tx.hash256_hex()))
        self.assertEqual(600, len(tx.serialize(is_hex=True)))
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] ' \
                  'service execute error!: [Invoke] Native serivce function execute error!: ' \
                  'register ONT ID error: already registered'
            self.assertEqual(msg, e.args[1])

    def test_send_registry(self):
        ont_id = sdk.native_vm.ont_id()
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        label = 'label'
        password = 'password'
        try:
            identity = sdk.wallet_manager.create_identity_from_private_key(label, password, private_key)
        except SDKException as e:
            self.assertIn('Wallet identity exists', e.args[1])
            return
        gas_limit = 20000
        gas_price = 500
        try:
            ont_id.send_registry_ont_id_transaction(identity, password, acct2, gas_limit, gas_price)
        except SDKException as e:
            self.assertEqual(59000, e.args[0])
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] ' \
                  'service execute error!: [Invoke] Native serivce function execute error!: ' \
                  'register ONT ID error: already registered'
            self.assertEqual(msg, e.args[1])

    def test_send_get_ddo(self):
        ont_id = sdk.native_vm.ont_id()
        hex_public_key = '035384561673e76c7e3003e705e4aa7aee67714c8b68d62dd1fb3221f48c5d3da0'
        acct_did = 'did:ont:AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        parsed_ddo = ont_id.send_get_ddo(acct_did)
        self.assertIn(acct_did, parsed_ddo['Owners'][0]['PubKeyId'])
        self.assertEqual('ECDSA', parsed_ddo['Owners'][0]['Type'])
        self.assertEqual('P256', parsed_ddo['Owners'][0]['Curve'])
        self.assertEqual(hex_public_key, parsed_ddo['Owners'][0]['Value'])

    def test_new_get_ddo_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        hex_public_key = '035384561673e76c7e3003e705e4aa7aee67714c8b68d62dd1fb3221f48c5d3da0'
        acct_did = 'did:ont:AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        tx = ont_id.new_get_ddo_transaction(acct_did)
        response = sdk.rpc.send_raw_transaction_pre_exec(tx)
        ddo = response['Result']
        parsed_ddo = ont_id.parse_ddo(acct_did, ddo)
        self.assertIn(acct_did, parsed_ddo['Owners'][0]['PubKeyId'])
        self.assertEqual('ECDSA', parsed_ddo['Owners'][0]['Type'])
        self.assertEqual('P256', parsed_ddo['Owners'][0]['Curve'])
        self.assertEqual(hex_public_key, parsed_ddo['Owners'][0]['Value'])

    def test_new_add_attribute_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        attribute = {'key': 'try', 'type': 'string', 'value': 'attribute'}
        attribute_list = [attribute]
        hex_public_key = acct2.get_public_key_hex()
        b58_address = acct2.get_address_base58()
        acct_did = "did:ont:" + b58_address
        gas_limit = 20000
        gas_price = 500
        tx = ont_id.new_add_attribute_transaction(acct_did, hex_public_key, attribute_list, b58_address, gas_limit,
                                                  gas_price)
        tx = sdk.sign_transaction(tx, acct2)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(tx.hash256_explorer(), tx_hash)

    def test_new_remove_attribute_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        hex_public_key = acct2.get_public_key_hex()
        b58_address = acct2.get_address_base58()
        acct_did = "did:ont:" + b58_address
        gas_limit = 20000
        gas_price = 500
        path = 'try'
        tx = ont_id.new_remove_attribute_transaction(acct_did, hex_public_key, path, b58_address, gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, acct2)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(tx.hash256_explorer(), tx_hash)
            time.sleep(6)
            notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
            self.assertEqual('Attribute', notify[0]['States'][0])
            self.assertEqual('remove', notify[0]['States'][1])
            self.assertEqual(acct_did, notify[0]['States'][2])
            self.assertEqual('try', bytes.fromhex(notify[0]['States'][3]).decode())
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: ' \
                  '[SystemCall] service execute error!: [Invoke] Native serivce function execute error!: ' \
                  'remove attribute failed: attribute not exist'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

    def test_send_add_attributes(self):
        ont_id = sdk.native_vm.ont_id()
        attribute = {'key': 'try', 'type': 'string', 'value': 'attribute'}
        attribute_list = [attribute]
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        password = 'password'
        try:
            identity = sdk.wallet_manager.create_identity_from_private_key('label', password, private_key)
        except SDKException as e:
            self.assertIn('Wallet identity exists', e.args[1])
            return
        gas_limit = 20000
        gas_price = 500
        tx_hash = ont_id.send_add_attribute_transaction(identity, password, attribute_list, acct, gas_limit,
                                                        gas_price)
        time.sleep(6)
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('Attribute', notify[0]['States'][0])
        self.assertEqual('add', notify[0]['States'][1])
        self.assertEqual(identity.ont_id, notify[0]['States'][2])
        self.assertEqual('try', bytes.fromhex(notify[0]['States'][3][0]).decode())

    def test_remove_attribute(self):
        ont_id = sdk.native_vm.ont_id()
        label = 'label'
        password = 'password'
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        identity = sdk.wallet_manager.create_identity_from_private_key(label, password, private_key)
        gas_limit = 20000
        gas_price = 500
        path = 'try'
        try:
            tx_hash = ont_id.send_remove_attribute_transaction(identity, password, path, acct2, gas_limit, gas_price)
            time.sleep(6)
            notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
            self.assertEqual('Attribute', notify[0]['States'][0])
            self.assertEqual('remove', notify[0]['States'][1])
            self.assertEqual(identity.ont_id, notify[0]['States'][2])
            self.assertEqual('try', bytes.fromhex(notify[0]['States'][3]).decode())
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: ' \
                  '[SystemCall] service execute error!: [Invoke] Native serivce function execute error!: ' \
                  'remove attribute failed: attribute not exist'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

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
        tx = sdk.sign_transaction(tx, acct)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('PublicKey', notify[0]['States'][0])
        self.assertEqual('add', notify[0]['States'][1])
        self.assertEqual(acct_did, notify[0]['States'][2])
        self.assertEqual(hex_new_public_key, notify[0]['States'][4])
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute error!:' \
                  ' [Invoke] Native serivce function execute error!: add key failed: already exists'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

        tx = ont_id.new_remove_public_key_transaction(acct_did, hex_public_key, hex_new_public_key, b58_address,
                                                      gas_limit, gas_price)
        tx = sdk.sign_transaction(tx, acct)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('PublicKey', notify[0]['States'][0])
        self.assertEqual('remove', notify[0]['States'][1])
        self.assertEqual(acct_did, notify[0]['States'][2])
        self.assertEqual(hex_new_public_key, notify[0]['States'][4])
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute ' \
                  'error!: [Invoke] Native serivce function execute error!: remove key failed: ' \
                  'public key has already been revoked'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

    def test_send_add_remove_public_key_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        label = 'label'
        password = 'password'
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        try:
            identity = sdk.wallet_manager.create_identity_from_private_key(label, password, private_key)
        except SDKException as e:
            self.assertIn('Wallet identity exists', e.args[1])
            return
        rand_private_key = utils.get_random_bytes(32).hex()
        rand_acct = Account(rand_private_key, SignatureScheme.SHA256withECDSA)
        hex_new_public_key = rand_acct.get_public_key_hex()
        password = 'password'
        gas_limit = 20000
        gas_price = 500
        tx_hash = ont_id.send_add_public_key_transaction(identity, password, hex_new_public_key, acct, gas_limit,
                                                         gas_price)
        time.sleep(6)
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('PublicKey', notify[0]['States'][0])
        self.assertEqual('add', notify[0]['States'][1])
        self.assertEqual(identity.ont_id, notify[0]['States'][2])
        self.assertEqual(hex_new_public_key, notify[0]['States'][4])
        try:
            ont_id.send_add_public_key_transaction(identity, password, hex_new_public_key, acct, gas_limit, gas_price)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute' \
                  ' error!: [Invoke] Native serivce function execute error!: add key failed: already exists'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

        tx_hash = ont_id.send_remove_public_key_transaction(identity, password, hex_new_public_key, acct, gas_limit,
                                                            gas_price)
        time.sleep(6)
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify']
        self.assertEqual('PublicKey', notify[0]['States'][0])
        self.assertEqual('remove', notify[0]['States'][1])
        self.assertEqual(identity.ont_id, notify[0]['States'][2])
        self.assertEqual(hex_new_public_key, notify[0]['States'][4])
        try:
            ont_id.send_remove_public_key_transaction(identity, password, hex_new_public_key, acct, gas_limit,
                                                      gas_price)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute ' \
                  'error!: [Invoke] Native serivce function execute error!: remove key failed: ' \
                  'public key has already been revoked'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

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
        tx = sdk.sign_transaction(tx, acct)
        try:
            sdk.rpc.send_raw_transaction(tx)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] service execute ' \
                  'error!: [Invoke] Native serivce function execute error!: add recovery failed: already ' \
                  'set recovery'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

    def test_send_add_recovery_transaction(self):
        ont_id = sdk.native_vm.ont_id()
        label = 'label'
        password = 'password'
        private_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        try:
            identity = sdk.wallet_manager.create_identity_from_private_key(label, password, private_key)
        except SDKException as e:
            self.assertIn('Wallet identity exists', e.args[1])
            return
        rand_private_key = utils.get_random_bytes(32).hex()
        recovery = Account(rand_private_key, SignatureScheme.SHA256withECDSA)
        b58_recovery_address = recovery.get_address_base58()
        password = 'password'
        gas_limit = 20000
        gas_price = 500
        try:
            ont_id.send_add_recovery_transaction(identity, password, b58_recovery_address, acct, gas_limit, gas_price)
        except SDKException as e:
            msg = 'Other Error, [NeoVmService] service system call error!: [SystemCall] ' \
                  'service execute error!: [Invoke] Native serivce function execute error!: ' \
                  'add recovery failed: already set recovery'
            self.assertEqual(59000, e.args[0])
            self.assertEqual(msg, e.args[1])

    # TODO
    # def test_send_add_public_key_by_recovery(self):
    #     ont_id = sdk.native_vm.ont_id()


if __name__ == '__main__':
    unittest.main()
