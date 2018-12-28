#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from typing import List

from ontology.crypto.digest import Digest


class MerkleVerifier(object):
    @staticmethod
    def validate_proof(proof: List[dict], target_hash: str, merkle_root: str):
        merkle_root = binascii.a2b_hex(merkle_root)
        target_hash = binascii.a2b_hex(target_hash)
        if len(proof) == 0:
            return target_hash == merkle_root
        else:
            proof_hash = target_hash
            for node in proof:
                try:
                    sibling = binascii.a2b_hex(node['left'])
                    proof_hash = Digest.sha256(sibling + proof_hash)
                except KeyError:
                    sibling = binascii.a2b_hex(node['right'])
                    proof_hash = Digest.sha256(sibling + proof_hash)
            return proof_hash == merkle_root
