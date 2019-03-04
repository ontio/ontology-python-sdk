#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from time import time, sleep

from ontology.claim.claim import Claim
from ontology.claim.header import Header
from ontology.claim.payload import Payload
from ontology.claim.proof import BlockchainProof
from ontology.exception.exception import SDKException
from test import sdk, acct1, identity1, identity2, identity2_ctrl_acct

gas_limit = 20000
gas_price = 500


class TestClaim(unittest.TestCase):
    def test_head(self):
        kid = 'did:ont:TRAtosUZHNSiLhzBdHacyxMX4Bg3cjWy3r#keys-1'
        claim_header = Header(kid)
        claim_header_dict = dict(claim_header)
        self.assertEqual(kid, claim_header_dict['kid'])
        self.assertTrue(isinstance(claim_header_dict, dict))
        self.assertEqual('ONT-ES256', claim_header_dict['alg'])
        self.assertEqual(96, len(claim_header.to_json()))
        b64_head = claim_header.to_base64()
        claim_header_recv = Header.from_base64(b64_head)
        self.assertEqual(dict(claim_header), dict(claim_header_recv))

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
        self.assertEqual(64, len(claim_payload_dict['jti']))
        self.assertEqual(context, claim_payload_dict['@context'])
        self.assertEqual(clm, claim_payload_dict['clm'])
        self.assertEqual(clm_rev, claim_payload_dict['clm-rev'])
        b64_payload = claim_payload.to_base64()
        claim_payload_recv = Payload.from_base64(b64_payload)
        self.assertEqual(dict(claim_payload), dict(claim_payload_recv))

    def test_signature_info(self):
        try:
            pub_keys = sdk.native_vm.ont_id().get_public_keys(identity2.ont_id)
            pk = pub_keys[0]
            kid = pk['PubKeyId']
        except IndexError:
            kid = '03eca83d4e4a0ed1e96d87942f76275c49a2f61a6b1e0f33be5a65f9beae71cd3f#keys-1'
        iss_ont_id = identity2.ont_id
        sub_ont_id = identity1.ont_id
        exp = int(time()) + 100
        context = 'https://github.com/NashMiao'
        clm = dict(Name='NashMiao', Position='Mars', Birthday=str(time()))
        clm_rev = dict(type='AttestContract', addr='8055b362904715fd84536e754868f4c8d27ca3f6')
        claim = sdk.service.claim()
        claim.set_claim(kid, iss_ont_id, sub_ont_id, exp, context, clm, clm_rev)
        try:
            claim.generate_signature(identity2_ctrl_acct)
        except SDKException as e:
            msg = 'get key failed'
            self.assertTrue(msg in e.args[1])
            claim.generate_signature(identity2_ctrl_acct, verify_kid=False)
        b64_claim = claim.to_base64()
        try:
            self.assertTrue(claim.validate_signature(b64_claim))
        except SDKException as e:
            msg = 'invalid claim head parameter'
            self.assertTrue(msg in e.args[1])

    def test_claim_demo(self):
        pub_keys = sdk.native_vm.ont_id().get_public_keys(identity1.ont_id)
        try:
            pk = pub_keys[0]
            kid = pk['PubKeyId']
        except IndexError:
            kid = '03d0fdb54acba3f81db3a6e16fa02e7ea3678bd205eb4ed2f1cfa8ab5e5d45633e#keys-1'
        iss_ont_id = identity2.ont_id
        sub_ont_id = identity1.ont_id
        exp = int(time()) + 1000
        context = 'https://example.com/template/v1'
        clm = dict(Name='NashMiao', JobTitle='SoftwareEngineer', HireData=str(time()))
        clm_rev = dict(type='AttestContract', addr='8055b362904715fd84536e754868f4c8d27ca3f6')
        claim = sdk.service.claim()
        claim.set_claim(kid, iss_ont_id, sub_ont_id, exp, context, clm, clm_rev)
        try:
            claim.generate_signature(identity2_ctrl_acct)
        except SDKException as e:
            msg = 'get key failed'
            self.assertTrue(msg in e.args[1])
            claim.generate_signature(identity2_ctrl_acct, verify_kid=False)
        blockchain_proof = claim.generate_blk_proof(identity2_ctrl_acct, acct1, gas_limit, gas_price)
        self.assertTrue(claim.validate_blk_proof())
        b64_claim = claim.to_base64()
        claim_list = b64_claim.split('.')
        self.assertEqual(4, len(claim_list))
        claim_recv = sdk.service.claim()
        claim_recv.from_base64(b64_claim)
        self.assertEqual(dict(claim), dict(claim_recv))
        proof_node = blockchain_proof.proof_node
        if proof_node[0]['Direction'] == 'Right':
            proof_node[0]['Direction'] = 'Left'
        else:
            proof_node[0]['Direction'] = 'Right'
        claim.blk_proof.proof_node = proof_node
        self.assertFalse(claim.validate_blk_proof())

    def test_compatibility(self):
        b64_claim = ('eyJraWQiOiJkaWQ6b250OkFUWmhhVmlyZEVZa3BzSFFEbjlQTXQ1a0RDcTFWUEhjVHIja2V5cy0xIiwidHlwIjoiSldULVgiL'
                     'CJhbGciOiJPTlQtRVMyNTYifQ==.eyJjbG0tcmV2Ijp7InR5cCI6IkF0dGVzdENvbnRyYWN0IiwiYWRkciI6IjM2YmI1YzA1M'
                     '2I2YjgzOWM4ZjZiOTIzZmU4NTJmOTEyMzliOWZjY2MifSwic3ViIjoiZGlkOm9udDpBYmt3UjNENmQya3A0cUpTVDI5dDlHa3'
                     'JZVldVdmJFSERxIiwidmVyIjoidjEuMCIsImNsbSI6eyJOYXRpb25hbGl0eSI6IkNOIiwiTmFtZSI6IueCjuacsSIsIkJpcnR'
                     'oRGF5IjoiMTk4Mi0wMi0xMSIsIklzc3VlRGF0ZSI6IjIwMTYtMDYtMjgiLCJFeHBpcmF0aW9uRGF0ZSI6IjIwMzYtMDYtMjgi'
                     'LCJJRERvY051bWJlciI6IjMxMDEwNDE5ODIwMjExMzY1MyIsIklzc3Vlck5hbWUiOiJTaHVmdGlwcm8ifSwiaXNzIjoiZGlkO'
                     'm9udDpBVFpoYVZpcmRFWWtwc0hRRG45UE10NWtEQ3ExVlBIY1RyIiwiZXhwIjoxNTc3NTIyNzQwLCJpYXQiOjE1NDU5ODY3ND'
                     'AsIkBjb250ZXh0IjoiY2xhaW06c2ZwX2lkY2FyZF9hdXRoZW50aWNhdGlvbiIsImp0aSI6ImFkM2MzODFkZjRhNzg0MTVkMGU'
                     '0MGUxMTM0MDZmY2JkYmZkMzNhMTQzMDg0ZjM2ZTE4ODk2NDgwMGUxN2IzMGEifQ==.AWAvGV7YfP7wLh+1y9qq49ox8yxn5ZR'
                     '+U/p1UE6fDKlKzWN0ZZolimnyuuo2rssbAZt0deO3QMF4DMEfsAxrEPo=\.eyJUeXBlIjoiTWVya2xlUHJvb2YiLCJNZXJrbG'
                     'VSb290IjoiYjg0M2NhOGQxMjMwODdmODE4YjU1YjdkOTk4MThjM2UxOTVjYzU2NjRjOGZlYmFlZGU4NmZjZWNhODc3NGU1ZCI'
                     'sIlR4bkhhc2giOiJjMTdlNTc0ZGRhMTdmMjY4NzkzNzU3ZmFiMGMyNzRkNDQ0MjdmYTFiNjdkNjMxMTNiZDMxZTM5YjMxZDFh'
                     'MDI2IiwiQmxvY2tIZWlnaHQiOjE0NDUwNDQsIk5vZGVzIjpbeyJUYXJnZXRIYXNoIjoiNTYxZjg0ZmU4Y2M1ZjE0M2U4OTU5Z'
                     'WM5N2U4ZWMwZjFmY2Y3MmZjMGYwZTcwOWY5NTU3OTBiODAxYTc0ZjdiMSIsIkRpcmVjdGlvbiI6IlJpZ2h0In0seyJUYXJnZX'
                     'RIYXNoIjoiNzI2MjIwZDg0N2MyZTgyYjFjY2U1YzI0ZmE3MmQ0MzdmZDgwMWMyY2E5MGZjZjY2ZDBlNTYzOGIwZTU2OWQwNSI'
                     'sIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiI5OTc4MmUwOTVhM2YzZTc3Yjk0YTIxNjc1YmIzMmY0MDI2OGYz'
                     'MDAwZDdjOTU0YjVjZTBlMjhhODdhMTU1NjMxIiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6IjFkMGVlNmVmZ'
                     'GQwYTAzOTQ5NTE3NmRkNTljOTEwMTNjOGE5MTQ5MWIyMWQxN2RlYzg3NzRkY2RjN2E0OTZiYjYiLCJEaXJlY3Rpb24iOiJMZW'
                     'Z0In0seyJUYXJnZXRIYXNoIjoiZjQyOWE1NDY2NDUzMjczNjU5NWFhZjk1MjFmZmJjZDllMGM3NGJiMjVkODBjOGJiN2NhNzc'
                     'yY2VlOWIzODUwYSIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiJlYTk0NzgwZjQzZWE4NDJhMzNjMzY3MjQ4'
                     'NDQzNGQxNmZlMDI5ZjE4MWZiYTAzNDEwMWZkYzFkZDAxNzM2MGI0IiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFza'
                     'CI6IjkzOTgxNjAwMDViMDdlMDgyYzA0ZGU0ZDIzYmE5YjYxZDNhYzFiYjRlNzJiZWRhMmY2N2U5MWIwMGI3MzllOTkiLCJEaX'
                     'JlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiM2IyNmQxMzA4NDFmMTQyNGYwMjFlODI2MzI5ODI2YjVlYTQxOTMzMWI'
                     'yMjlhYmRjZjMwYmU2MmIzNDgyMTBhZCIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiIwNTU5NmIzYTY1Yjg1'
                     'NjU4YmEyZDFjODcxYzMzYjY1ZGY3NDVlODA3YzBmNWVjZTU5YTIyNTE4N2YxZDIxYzRmIiwiRGlyZWN0aW9uIjoiTGVmdCJ9L'
                     'HsiVGFyZ2V0SGFzaCI6ImRlMzE0YzgxMmU5NTVkZDBhNTczYzJkNGJjMzlmMmI3MGQxMTllNTBlNTZlMWRhMjVjYzMzOTM1N2'
                     'QwOTA4OTAiLCJEaXJlY3Rpb24iOiJMZWZ0In1dLCJDb250cmFjdEFkZHIiOiIzNmJiNWMwNTNiNmI4MzljOGY2YjkyM2ZlODU'
                     'yZjkxMjM5YjlmY2NjIn0=')
        try:
            sdk.rpc.connect_to_main_net()
            claim = sdk.service.claim()
            try:
                self.assertTrue(claim.validate_signature(b64_claim))
            except SDKException as e:
                msg = 'invalid claim head parameter'
                self.assertTrue(msg in e.args[1])
            claim.from_base64(b64_claim, True)
            self.assertTrue(claim.validate_blk_proof())
            self.assertTrue(isinstance(claim, Claim))
        finally:
            sdk.rpc.connect_to_test_net()


if __name__ == '__main__':
    unittest.main()
