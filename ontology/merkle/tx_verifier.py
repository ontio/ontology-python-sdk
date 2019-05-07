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
        merkle_proof = self.__sdk.default_network.get_merkle_proof(tx_hash)
        tx_block_height = merkle_proof['BlockHeight']
        current_block_height = merkle_proof['CurBlockHeight']
        target_hash_list = merkle_proof['TargetHashes']
        target_hash = merkle_proof['TransactionsRoot']
        merkle_root = merkle_proof['CurBlockRoot']
        proof_node = MerkleVerifier.get_proof(tx_block_height, target_hash_list, current_block_height)
        result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root, True)
        return result
