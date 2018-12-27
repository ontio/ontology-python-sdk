#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

    def test_vv(self):
        import requests
        import json

        eos_main_net = 'https://mainnet.eos.dfuse.io'
        header = dict(
            Authorization='Bearer eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDcwODg4MjYsImp0aSI6IjU3MDM1NjVmLTI1YjUtNDkzNC05NWVmLWFjNDIzZDk0ZTc3MiIsImlhdCI6MTU0NDQ5NjgyNiwiaXNzIjoiZGZ1c2UuaW8iLCJzdWIiOiJDaVFBNmNieWU4ZzAyVTloYmdpMThGUk1MOXhXcW4vdHljeFl5QUdIVEF0SEI3WEhYcUVTT3dBL0NMUnRzOHdWd05xN0swVkZpTjd0dnZXREFvNXhRZmg2a1BrVUo0bTg5UFZsYTVBYTVwTE9yK1dKWDdlNVpzVzZKam9Od2ZQa2FXY0kiLCJ0aWVyIjoiYmV0YS12MSIsInYiOjF9.5cEPmu-9pg8IDmmVseaFNagX_I9VvzyoowwQxLv_Ie28L3lsYdNMF1J-R1-teVvJU6eOpNUBJCLi3ZdusChowg')
        method = 'search/transactions'
        url = f'{eos_main_net}/v0/{method}'
        payload = dict(start_block=34226134, block_count=2000, limit=100, sort='desc',
        q = 'wizznetwork1:eosio.token action:transfer')

        data = requests.get(url=url, params=json.dumps(payload), headers=header)
        print(data.content.decode('utf-8'))


def test_s(self):
    # print(ErrorCode.invalid_par)
    # print(ErrorCode.invalid_params)
    ErrorCode.a()


if __name__ == '__main__':
    unittest.main()
