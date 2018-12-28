#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import unittest

from ontology.ont_sdk import OntologySdk
from ontology.merkle.merkle_verifier import MerkleVerifier

sdk = OntologySdk()
sdk.rpc.connect_to_test_net()


class TestMerkleVerifier(unittest.TestCase):
    def test_validate_proof(self):
        proof = [{'right': '09096dbc49b7909917e13b795ebf289ace50b870440f10424af8845fb7761ea5'},
                 {'right': 'ed2456914e48c1e17b7bd922177291ef8b7f553edf1b1f66b6fc1a076524b22f'},
                 {'left': 'eac53dde9661daf47a428efea28c81a021c06d64f98eeabbdcff442d992153a8'}]
        target_hash = '36e0fd847d927d68475f32a94efff30812ee3ce87c7752973f4dd7476aa2e97e'
        merkle_root = 'b8b1f39aa2e3fc2dde37f3df04e829f514fb98369b522bfb35c663befa896766'
        result = MerkleVerifier.validate_proof(proof, target_hash, merkle_root)
        print(result)


if __name__ == '__main__':
    unittest.main()
