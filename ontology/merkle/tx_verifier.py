#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

from ontology.merkle.merkle_verifier import MerkleVerifier


class TxVerifier(object):
    _instance_lock = threading.Lock()

    def __init__(self, sdk):
        self.__sdk = sdk

    def __new__(cls, *args, **kwargs):
        if not hasattr(TxVerifier, '_instance'):
            with TxVerifier._instance_lock:
                if not hasattr(TxVerifier, '_instance'):
                    TxVerifier._instance = object.__new__(cls)
        return TxVerifier._instance

    def verify_by_tx_hash(self, tx_hash: str):
        merkle_proof = self.__sdk.get_network().get_merkle_proof(tx_hash)
        tx_block_height = merkle_proof['BlockHeight']
        current_block_height = merkle_proof['CurBlockHeight']
        target_hash_list = merkle_proof['TargetHashes']
        target_hash = merkle_proof['TransactionsRoot']
        merkle_root = merkle_proof['CurBlockRoot']
        proof_node = MerkleVerifier.get_proof(tx_block_height, target_hash_list, current_block_height)
        result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root, True)
        return result
