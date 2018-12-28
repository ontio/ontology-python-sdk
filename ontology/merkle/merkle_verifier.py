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
    def generate_blockchain_proof(tx_hash: str, hex_contract_address: str, block_height: int, merkle_root: str,
                                  proof: List[dict]):
        if len(tx_hash) != 64:
            raise SDKException(ErrorCode.other_error('Invalid TxHash.'))
        if len(hex_contract_address) != 40:
            raise SDKException(ErrorCode.other_error('Invalid contract address.'))
        if not isinstance(block_height, int):
            raise SDKException(ErrorCode.other_error('Invalid block height.'))
        if len(merkle_root) != 64:
            raise SDKException(ErrorCode.other_error('Invalid merkle root.'))
        blockchain_proof = dict(Type='MerkleProof', TxnHash=tx_hash, ContractAddr=hex_contract_address,
                                BlockHeight=block_height, MerkleRoot=merkle_root, Nodes=proof)
        return blockchain_proof

    @staticmethod
    def validate_proof(proof: List[dict], hex_target_hash: str, hex_merkle_root: str):
        hex_merkle_root = ContractDataParser.to_reserve_hex_str(hex_merkle_root)
        hex_target_hash = ContractDataParser.to_reserve_hex_str(hex_target_hash)
        if len(proof) == 0:
            return hex_target_hash == hex_merkle_root
        else:
            hex_proof_hash = hex_target_hash
            for node in proof:
                sibling = ContractDataParser.to_reserve_hex_str(node['TargetHash'])
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
