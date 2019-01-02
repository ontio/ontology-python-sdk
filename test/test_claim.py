#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import unittest

from ontology.claim.claim import Claim
from ontology.claim.header import Header
from ontology.claim.payload import Payload
from ontology.crypto.curve import Curve
from ontology.crypto.signature import Signature
from ontology.exception.exception import SDKException
from ontology.ont_sdk import OntologySdk
from ontology.utils import utils
from ontology.utils.contract_event_parser import ContractEventParser
from test import acct1, password

sdk = OntologySdk()
sdk.rpc.connect_to_test_net()


class TestClaim(unittest.TestCase):
    def test_head(self):
        kid = 'did:ont:TRAtosUZHNSiLhzBdHacyxMX4Bg3cjWy3r#keys-1'
        claim_header = Header(kid)
        claim_header_dict = dict(claim_header)
        self.assertEqual(kid, claim_header_dict['kid'])
        self.assertTrue(isinstance(claim_header_dict, dict))
        self.assertEqual('ES256', claim_header_dict['alg'])
        self.assertEqual(92, len(claim_header.to_json_str()))

    def test_payload(self):
        ver = '0.7.0'
        iss = 'did:ont:TRAtosUZHNSiLhzBdHacyxMX4Bg3cjWy3r'
        sub = 'did:ont:SI59Js0zpNSiPOzBdB5cyxu80BO3cjGT70'
        iat = 1525465044
        exp = 1530735444
        jti = '4d9546fdf2eb94a364208fa65a9996b03ba0ca4ab2f56d106dac92e891b6f7fc'
        context = 'https://example.com/template/v1'
        clm = dict(Name='Bob Dylan', Age='22')
        clm_rev = dict(typ='AttestContract', addr='8055b362904715fd84536e754868f4c8d27ca3f6')
        claim_payload = Payload(ver, iss, sub, iat, exp, context, clm, clm_rev, jti)
        claim_payload_dict = dict(claim_payload)
        self.assertEqual(ver, claim_payload_dict['ver'])
        self.assertEqual(iss, claim_payload_dict['iss'])
        self.assertEqual(sub, claim_payload_dict['sub'])
        self.assertEqual(iat, claim_payload_dict['iat'])
        self.assertEqual(exp, claim_payload_dict['exp'])
        self.assertEqual(jti, claim_payload_dict['jti'])
        self.assertEqual(context, claim_payload_dict['@context'])
        self.assertEqual(clm, claim_payload_dict['clm'])
        self.assertEqual(clm_rev, claim_payload_dict['clm-rev'])
        claim_payload = Payload(ver, iss, sub, iat, exp, context, clm, clm_rev)
        self.assertEqual(415, len(claim_payload.to_json_str()))
        claim_payload_dict = dict(claim_payload)
        self.assertEqual(ver, claim_payload_dict['ver'])
        self.assertEqual(iss, claim_payload_dict['iss'])
        self.assertEqual(sub, claim_payload_dict['sub'])
        self.assertEqual(iat, claim_payload_dict['iat'])
        self.assertEqual(exp, claim_payload_dict['exp'])
        self.assertEqual(64, len(claim_payload_dict['jti']))
        self.assertEqual(context, claim_payload_dict['@context'])
        self.assertEqual(clm, claim_payload_dict['clm'])
        self.assertEqual(clm_rev, claim_payload_dict['clm-rev'])
        self.assertEqual(415, len(claim_payload.to_json_str()))

    def test_signature_info(self):
        pass

    def test_ont_id_register(self):
        private_key_hex = acct1.get_private_key_hex()
        print(private_key_hex)
        identity = sdk.wallet_manager.create_identity_from_private_key('NashMiao', password, private_key_hex)
        gas_limit = 20000
        gas_price = 500
        try:
            sdk.native_vm.ont_id().send_registry_ont_id_transaction(identity, password, acct1, gas_limit, gas_price)
        except SDKException as e:
            self.assertIn('already registered', e.args[1])
        tx_hash = '982aaa5c639a0a097373c8b585ebf1a69572c50a6a7c339cc45b3a1233f0600d'
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        hex_contract_address = '0300000000000000000000000000000000000000'
        notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
        self.assertIn('Register', notify['States'])
        self.assertIn(identity.ont_id, notify['States'])

    def test_add_public_key(self):
        private_key = utils.get_random_bytes(32)
        public_key = Signature.ec_get_public_key_by_private_key(private_key, Curve.P256)
        print(public_key.hex())
        sdk.native_vm.ont_id().send_add_public_key_transaction()

    def test_generate_blockchain_proof(self):
        tx_hash = 'd7a81db41b2608f2c5da4a4d84b266a8e8f86c244781287c183ee1129e37a9cd'
        hex_contract_address = '8055b362904715fd84536e754868f4c8d27ca3f6'
        merkle_proof = sdk.rpc.get_merkle_proof(tx_hash)
        print(json.dumps(merkle_proof, indent=4))
        current_block_height = merkle_proof['CurBlockHeight']
        merkle_root = merkle_proof['CurBlockRoot']
        proof = Claim.generate_blockchain_proof(tx_hash, hex_contract_address, current_block_height,
                                                merkle_root)
        print(proof)


if __name__ == '__main__':
    unittest.main()
