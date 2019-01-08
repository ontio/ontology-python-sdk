#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest
from time import time, sleep

from ontology.claim.header import Header
from ontology.claim.payload import Payload
from ontology.merkle.merkle_verifier import MerkleVerifier
from ontology.utils.contract_data_parser import ContractDataParser
from ontology.utils.contract_event_parser import ContractEventParser
from test import acct1, password, identity1, acct4, sdk, identity2, identity2_ctrl_acct


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

    def test_generate_blockchain_proof(self):
        tx_hash = 'd7a81db41b2608f2c5da4a4d84b266a8e8f86c244781287c183ee1129e37a9cd'
        hex_contract_address = '8055b362904715fd84536e754868f4c8d27ca3f6'
        sdk.rpc.connect_to_main_net()
        merkle_proof = sdk.get_network().get_merkle_proof(tx_hash)
        current_block_height = merkle_proof['CurBlockHeight']
        target_hash = merkle_proof['TransactionsRoot']
        proof = sdk.service.claim().generate_blockchain_proof(tx_hash, hex_contract_address)
        self.assertEqual('MerkleProof', proof['Type'])
        self.assertEqual(tx_hash, proof['TxnHash'])
        self.assertEqual(hex_contract_address, proof['ContractAddr'])
        self.assertGreaterEqual(proof['BlockHeight'], current_block_height)
        proof_node = proof['Nodes']
        merkle_root = proof['MerkleRoot']
        result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root)
        self.assertEqual(True, result)

    def test_signature_info(self):
        pub_keys = sdk.native_vm.ont_id().get_public_keys(identity1.ont_id)
        pk = pub_keys[0]
        kid = pk['PubKeyId']
        iss_ont_id = identity2.ont_id
        sub_ont_id = identity1.ont_id
        exp = int(time())
        context = 'https://example.com/template/v1'
        clm = dict(Name='NashMiao', JobTitle='SoftwareEngineer', HireData=str(time()))
        clm_rev = dict(type='AttestContract', addr='8055b362904715fd84536e754868f4c8d27ca3f6')

        claim = sdk.service.claim()
        claim.set_claim(kid, iss_ont_id, sub_ont_id, exp, context, clm, clm_rev)
        claim.generate_signature(identity2_ctrl_acct)
        gas_limit = 20000
        gas_price = 500
        tx_hash = sdk.neo_vm.claim_record().commit(claim.claim_id, identity2_ctrl_acct, identity1.ont_id, acct1,
                                                   gas_limit, gas_price)
        sleep(6)
        event = sdk.neo_vm.claim_record().query_commit_event(tx_hash)
        self.assertEqual('Push', event['States'][0])
        self.assertEqual(identity2_ctrl_acct.get_address_base58(), event['States'][1])
        self.assertEqual(' create new claim: ', event['States'][2])
        self.assertEqual(claim.claim_id, event['States'][3])

    def test_claim_demo(self):
        pub_keys = sdk.native_vm.ont_id().get_public_keys(identity1.ont_id)
        pk = pub_keys[0]
        kid = pk['PubKeyId']
        iss_ont_id = identity2.ont_id
        sub_ont_id = identity1.ont_id
        exp = int(time())
        context = 'https://example.com/template/v1'
        clm = dict(Name='NashMiao', JobTitle='SoftwareEngineer', HireData=str(time()))
        clm_rev = dict(type='AttestContract', addr='8055b362904715fd84536e754868f4c8d27ca3f6')

        claim = sdk.service.claim()
        claim.set_claim(kid, iss_ont_id, sub_ont_id, exp, context, clm, clm_rev)
        claim.generate_signature(identity2_ctrl_acct)
        gas_limit = 20000
        gas_price = 500
        blockchain_proof = claim.generate_blockchain_proof(identity2_ctrl_acct, acct1, gas_limit, gas_price)
        self.assertTrue(claim.validate_blockchain_proof(blockchain_proof))
        if blockchain_proof['Nodes'][0]['Direction'] == 'Right':
            blockchain_proof['Nodes'][0]['Direction'] = 'Left'
        else:
            blockchain_proof['Nodes'][0]['Direction'] = 'Right'
        self.assertFalse(claim.validate_blockchain_proof(blockchain_proof))
        self.assertTrue(isinstance(claim.to_bytes_blockchain_proof(), bytes))
        self.assertTrue(isinstance(claim.to_str_blockchain_proof(), str))
        b64_claim = claim.generate_b64_claim()
        claim_list = b64_claim.split('.')
        self.assertEqual(4, len(claim_list))


if __name__ == '__main__':
    unittest.main()
