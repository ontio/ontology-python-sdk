#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from ontology.claim.claim import Header, Payload


class TestClaim(unittest.TestCase):
    def test_head(self):
        claim_header = Header()
        claim_header_dict = dict(claim_header)
        self.assertTrue(isinstance(claim_header_dict, dict))
        self.assertEqual('ONT-ES256', claim_header_dict['alg'])

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
        claim_payload = Payload(ver, iss, sub, iat, exp, jti, context, clm, clm_rev)
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


if __name__ == '__main__':
    unittest.main()
