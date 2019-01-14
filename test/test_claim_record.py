#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from time import time, sleep

from ontology.exception.exception import SDKException
from test import sdk, identity1, identity2, identity2_ctrl_acct, acct1

gas_limit = 20000
gas_price = 500


class TestClaimRecord(unittest.TestCase):
    def test_commit(self):
        pub_keys = sdk.native_vm.ont_id().get_public_keys(identity1.ont_id)
        try:
            pk = pub_keys[0]
            kid = pk['PubKeyId']
        except IndexError:
            kid = '03d0fdb54acba3f81db3a6e16fa02e7ea3678bd205eb4ed2f1cfa8ab5e5d45633e#keys-1'
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
        tx_hash = sdk.neo_vm.claim_record().commit(claim.claim_id, identity2_ctrl_acct, identity1.ont_id, acct1,
                                                   gas_limit, gas_price)
        sleep(6)
        event = sdk.neo_vm.claim_record().query_commit_event(tx_hash)
        self.assertEqual('Push', event['States'][0])
        self.assertEqual(identity2_ctrl_acct.get_address_base58(), event['States'][1])
        self.assertEqual(' create new claim: ', event['States'][2])
        self.assertEqual(claim.claim_id, event['States'][3])


if __name__ == '__main__':
    unittest.main()
