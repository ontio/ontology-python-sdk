#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from test import sdk

from ontology.merkle.merkle_verifier import MerkleVerifier


class TestMerkleVerifier(unittest.TestCase):
    def test_validate_proof(self):
        proof_node = [
            {'TargetHash': 'fb2530764e458ef5b94147a687e85cbcf46ab575e1869730f792e57176d1a99b', 'Direction': 'Right'},
            {'TargetHash': '57f1a5a6d76804b8b78800101271f962e072e86c817b798012a087c149feb2dd', 'Direction': 'Right'},
            {'TargetHash': 'c67a1112f389a59c2d96c0d140c54947124741d8043b8283af89f38a9c127146', 'Direction': 'Right'},
            {'TargetHash': 'e7bc6dc7e96b579cebc3f50a36912ca579b7be19174de20b6fa1392a5b968b97', 'Direction': 'Right'},
            {'TargetHash': 'b29f69ef311ab8de9d7521d8342e625ca7e6a83b0ab744dd37d487eb04015f55', 'Direction': 'Right'},
            {'TargetHash': '158549153fb2e72890c18744ad71260c30815bb8be2018f6a67fc1bec5b9350e', 'Direction': 'Right'},
            {'TargetHash': '1e28f633ff0dd320feaa4e57a8c0b7da3bce3bff2d4ff6144df51b696a323160', 'Direction': 'Right'},
            {'TargetHash': 'e0138809da29afa741a03101dd783432b1e19063f618caae835f6be95b785803', 'Direction': 'Right'},
            {'TargetHash': 'cfb6a4d77bca71af28d693785e254941196ddf2d6076cdc9b0fa33b6f04cc981', 'Direction': 'Right'},
            {'TargetHash': '539e219f4c8c5a8380cade1d71c2aa793f3266bea2ffb81da4f540aa02a9e535', 'Direction': 'Right'},
            {'TargetHash': 'ec831558466cecde520b456a7c981d5e0eb9ab9bb4d6918a282449c6467515cd', 'Direction': 'Right'},
            {'TargetHash': '5f50b59f27ebeac7144e39a0ca3a90784d3194f488ee23c28af17cfe69ac07a6', 'Direction': 'Right'},
            {'TargetHash': 'efafc2f48bd0adbb9d1912ef5f09844c81c9bdd0ce8bfc1ad2e85f667c224395', 'Direction': 'Right'},
            {'TargetHash': '2470009a1c62bad043933e8e770100378dd361b38ee52d5b7b37104bb9b0d26b', 'Direction': 'Right'},
            {'TargetHash': '2f3a6afaa3b9b9df53b2fc24e3683362e5195e3610f2502cbae56aa35ae5b3a0', 'Direction': 'Right'},
            {'TargetHash': '1dfea4e74b4ba7651d73231f2f57cfba5450014448f55380fbb1d48b91d987db', 'Direction': 'Right'},
            {'TargetHash': '052716bc0151b2e707242d156ae2abd123a4bedab5c4e29706d6c5fb3a76f5c2', 'Direction': 'Right'},
            {'TargetHash': 'cab9edab2a49d832e5a0ea65f5ff7ee2634002ab4ee65799f8ef0bb3f569a598', 'Direction': 'Right'},
            {'TargetHash': '4e3274ea45d5a0572446835001b70de5d2103f24c30aa2826b7508b70ed4e50a', 'Direction': 'Right'},
            {'TargetHash': '8d52d736f0f84860a14e6f256156689347683a3609c80a03e264b4634e4e64ae', 'Direction': 'Right'}]
        target_hash = '39c225c72f9bd76cf2030ec96057531a403887b4ea2801d5137ac000e847cb4d'
        merkle_root = 'fb778e1195d335ad962dbbef4cae34ac620d6521f0a3751a79c6f3efd4ab04ca'
        result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root, True)
        self.assertEqual(True, result)

    def test_get_proof_local(self):
        tx_block_height = 2
        leaf_0 = 'c7ac8087b4ce292d654001b1ab1bfe5e68fa6f7b8492a5b2f83560f8ac28f5fa'
        leaf_1 = '5205a22b07c6072d60d28b41f1321ab993799d70693a3bb70bab7e58b49acc30'
        leaf_2 = 'c0de7f3035a7960450ec9a64e7835b958b0fec1ddb90cbeb0779073c0a9a8f53'
        target_hash_list = [leaf_0, leaf_1, leaf_2]
        current_block_height = 6
        proof_node = MerkleVerifier.get_proof(tx_block_height, target_hash_list, current_block_height)
        self.assertEqual(3, len(proof_node))
        self.assertEqual('Right', proof_node[0]['Direction'])
        self.assertEqual(leaf_0, proof_node[0]['TargetHash'])
        self.assertEqual('Left', proof_node[1]['Direction'])
        self.assertEqual(leaf_1, proof_node[1]['TargetHash'])
        self.assertEqual('Right', proof_node[2]['Direction'])
        self.assertEqual(leaf_2, proof_node[2]['TargetHash'])
        target_hash = '4b74e15973ce3964ba4a33ddaf92efbff922ea2225bca7676f62eab05829f11f'
        current_block_root = 'a5094c1daeeceab46319ce62b600c68a7accc806bd9fe2fdb869560bf66b5251'
        result = MerkleVerifier.validate_proof(proof_node, target_hash, current_block_root)
        self.assertTrue(result)

    def test_get_proof_test_net(self):
        tx_hash = 'bf74e9208c0a20ec417de458ab6c9d29c12c614e77fb943be4566c95fab61454'
        merkle_proof = sdk.rpc.get_merkle_proof(tx_hash)
        tx_block_height = merkle_proof['BlockHeight']
        current_block_height = merkle_proof['CurBlockHeight']
        target_hash_list = merkle_proof['TargetHashes']
        target_hash = merkle_proof['TransactionsRoot']
        merkle_root = merkle_proof['CurBlockRoot']
        proof_node = MerkleVerifier.get_proof(tx_block_height, target_hash_list, current_block_height)
        result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root, True)
        self.assertTrue(result)

    def test_get_proof_main_net(self):
        try:
            sdk.rpc.connect_to_main_net()
            tx_hash = 'c17e574dda17f268793757fab0c274d44427fa1b67d63113bd31e39b31d1a026'
            merkle_proof = sdk.rpc.get_merkle_proof(tx_hash)
            tx_block_height = merkle_proof['BlockHeight']
            current_block_height = merkle_proof['CurBlockHeight']
            target_hash_list = merkle_proof['TargetHashes']
            target_hash = merkle_proof['TransactionsRoot']
            merkle_root = merkle_proof['CurBlockRoot']
            proof_node = MerkleVerifier.get_proof(tx_block_height, target_hash_list, current_block_height)
            result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root, True)
            self.assertTrue(result)
            tx_hash = '7e8c19fdd4f9ba67f95659833e336eac37116f74ea8bf7be4541ada05b13503e'
            merkle_proof = sdk.rpc.get_merkle_proof(tx_hash)
            tx_block_height = merkle_proof['BlockHeight']
            current_block_height = merkle_proof['CurBlockHeight']
            target_hash_list = merkle_proof['TargetHashes']
            target_hash = merkle_proof['TransactionsRoot']
            merkle_root = merkle_proof['CurBlockRoot']
            proof_node = MerkleVerifier.get_proof(tx_block_height, target_hash_list, current_block_height)
            result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root, True)
            self.assertTrue(result)
        finally:
            sdk.rpc.connect_to_test_net()


if __name__ == '__main__':
    unittest.main()
