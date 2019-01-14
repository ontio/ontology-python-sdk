#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from typing import List

from ontology.crypto.digest import Digest
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.contract_data_parser import ContractDataParser


class MerkleVerifier(object):
    @staticmethod
    def get_proof(tx_block_height: int, target_hash_list: List[str], current_block_height: int):
        proof_node = list()
        last_node = current_block_height
        pos = 0
        while last_node > 0:
            if tx_block_height % 2 == 1:
                dict_node = dict(Direction='Left', TargetHash=target_hash_list[pos])
                proof_node.append(dict_node)
                pos += 1
            elif tx_block_height < last_node:
                dict_node = dict(Direction='Right', TargetHash=target_hash_list[pos])
                proof_node.append(dict_node)
                pos += 1
            tx_block_height //= 2
            last_node //= 2
        return proof_node

    @staticmethod
    def validate_proof(proof: List[dict], hex_target_hash: str, hex_merkle_root: str):
        if len(proof) == 0:
            return hex_target_hash == hex_merkle_root
        else:
            hex_proof_hash = hex_target_hash
            for node in proof:
                sibling = node['TargetHash']
                try:
                    direction = node['Direction'].lower()
                except KeyError:
                    raise SDKException(ErrorCode.other_error('Invalid proof'))
                if direction == 'left':
                    value = binascii.a2b_hex('01' + sibling + hex_proof_hash)
                    hex_proof_hash = Digest.sha256(value, is_hex=True)
                elif direction == 'right':
                    value = binascii.a2b_hex('01' + hex_proof_hash + sibling)
                    hex_proof_hash = Digest.sha256(value, is_hex=True)
                else:
                    raise SDKException(ErrorCode.other_error('Invalid proof.'))
            return hex_proof_hash == hex_merkle_root
