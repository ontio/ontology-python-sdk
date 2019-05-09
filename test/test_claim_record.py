#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
from time import time, sleep

from ontology.exception.exception import SDKException
from test import sdk, identity1, identity2, identity2_ctrl_acct, acct1, not_panic_exception


class TestClaimRecord(unittest.TestCase):
    def setUp(self):
        self.gas_price = 500
        self.gas_limit = 20000

    def generate_claim(self):
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
        return claim

    def query_commit_event_create_test_case(self, tx_hash: str, claim_id: str):
        event = sdk.neo_vm.claim_record().query_commit_event(tx_hash)
        self.assertEqual('Push', event['States'][0])
        self.assertEqual(identity2_ctrl_acct.get_address_base58(), event['States'][1])
        self.assertEqual(' create new claim: ', event['States'][2])
        self.assertEqual(claim_id, event['States'][3])

    def query_commit_event_exist_test_case(self, tx_hash: str, claim_id: str):
        event = sdk.neo_vm.claim_record().query_commit_event(tx_hash)
        self.assertEqual('ErrorMsg', event['States'][0])
        self.assertEqual(claim_id, event['States'][1])
        self.assertEqual(' existed!', event['States'][2])

    def query_revoke_event_test_case(self, tx_hash: str, claim_id: str):
        event = sdk.neo_vm.claim_record().query_revoke_event(tx_hash)
        self.assertEqual('Push', event['States'][0])
        self.assertEqual(identity2_ctrl_acct.get_address_base58(), event['States'][1])
        self.assertEqual(' revoke claim: ', event['States'][2])
        self.assertEqual(claim_id, event['States'][3])

    @not_panic_exception
    def test_claim_record(self):
        claim = self.generate_claim()
        status = sdk.neo_vm.claim_record().get_status(claim.claim_id)
        self.assertFalse(status)
        record = sdk.neo_vm.claim_record()

        tx_hash = record.commit(claim.claim_id, identity2_ctrl_acct, identity1.ont_id, acct1, self.gas_price,
                                self.gas_limit)
        sleep(12)
        self.query_commit_event_create_test_case(tx_hash, claim.claim_id)

        status = record.get_status(claim.claim_id)
        self.assertTrue(status)

        tx_hash = record.commit(claim.claim_id, identity2_ctrl_acct, identity1.ont_id, acct1, self.gas_price,
                                self.gas_limit)
        sleep(12)
        self.query_commit_event_exist_test_case(tx_hash, claim.claim_id)

        tx_hash = record.revoke(claim.claim_id, identity2_ctrl_acct, acct1, self.gas_price, self.gas_limit)
        sleep(12)
        self.query_revoke_event_test_case(tx_hash, claim.claim_id)

        status = record.get_status(claim.claim_id)
        self.assertFalse(status)


if __name__ == '__main__':
    unittest.main()
