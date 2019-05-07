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

from typing import List

from ontology.utils.contract import Data
from ontology.crypto.digest import Digest
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


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
    def validate_proof(proof: List[dict], hex_target_hash: str, hex_merkle_root: str, is_big_endian: bool = False):
        if is_big_endian:
            hex_merkle_root = Data.to_reserve_hex_str(hex_merkle_root)
            hex_target_hash = Data.to_reserve_hex_str(hex_target_hash)
        if len(proof) == 0:
            return hex_target_hash == hex_merkle_root
        else:
            hex_proof_hash = hex_target_hash
            for node in proof:
                if is_big_endian:
                    sibling = Data.to_reserve_hex_str(node['TargetHash'])
                else:
                    sibling = node['TargetHash']
                try:
                    direction = node['Direction'].lower()
                except KeyError:
                    raise SDKException(ErrorCode.other_error('Invalid proof'))
                if direction == 'left':
                    value = bytes.fromhex('01' + sibling + hex_proof_hash)
                    hex_proof_hash = Digest.sha256(value, is_hex=True)
                elif direction == 'right':
                    value = bytes.fromhex('01' + hex_proof_hash + sibling)
                    hex_proof_hash = Digest.sha256(value, is_hex=True)
                else:
                    raise SDKException(ErrorCode.other_error('Invalid proof.'))
            return hex_proof_hash == hex_merkle_root
