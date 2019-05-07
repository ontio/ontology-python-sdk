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

import json
import base64

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.merkle.merkle_verifier import MerkleVerifier


class BlockchainProof(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__blk_proof = dict()

    def __iter__(self):
        for key, value in self.__blk_proof.items():
            yield (key, value)

    def set_proof(self, tx_hash: str, hex_contract_address: str, crt_blk_height: int, merkle_root: str,
                  proof_node: list):
        self.__blk_proof = dict(Type='MerkleProof', TxnHash=tx_hash, ContractAddr=hex_contract_address,
                                BlockHeight=crt_blk_height, MerkleRoot=merkle_root, Nodes=proof_node)

    @property
    def proof(self):
        return self.__blk_proof

    @proof.setter
    def proof(self, args):
        blk_proof = args[0]
        try:
            is_big_endian = args[1]
        except IndexError:
            is_big_endian = False
        if not isinstance(blk_proof, dict):
            raise SDKException(ErrorCode.require_dict_params)
        if blk_proof.get('Type', '') != 'MerkleProof':
            raise SDKException(ErrorCode.invalid_blk_proof)
        try:
            self.set_proof(blk_proof['TxnHash'], blk_proof['ContractAddr'], blk_proof['BlockHeight'],
                           blk_proof['MerkleRoot'], blk_proof['Nodes'])
        except KeyError:
            raise SDKException(ErrorCode.invalid_blk_proof)
        if not self.validate_blk_proof(is_big_endian):
            raise SDKException(ErrorCode.invalid_blk_proof)
        self.__blk_proof = blk_proof

    @property
    def merkle_root(self):
        return self.__blk_proof.get('MerkleRoot', '')

    @merkle_root.setter
    def merkle_root(self, merkle_root: str):
        if not isinstance(merkle_root, str):
            raise SDKException(ErrorCode.require_str_params)
        if len(merkle_root) != 64:
            raise SDKException(ErrorCode.invalid_merkle_root)
        self.__blk_proof['MerkleRoot'] = merkle_root

    @property
    def proof_node(self):
        return self.__blk_proof.get('Nodes', list())

    @proof_node.setter
    def proof_node(self, proof_node: list):
        if not isinstance(proof_node, list):
            raise SDKException(ErrorCode.require_list_params)
        self.__blk_proof['Nodes'] = proof_node

    def validate_blk_proof(self, is_big_endian: bool = False) -> bool:
        if self.__blk_proof.get('Type', '') != 'MerkleProof':
            raise SDKException(ErrorCode.invalid_blk_proof)
        try:
            tx_hash = self.__blk_proof['TxnHash']
        except KeyError:
            raise SDKException(ErrorCode.invalid_blk_proof)
        proof_node = self.__blk_proof.get('Nodes', list())
        merkle_root = self.__blk_proof.get('MerkleRoot', '')
        try:
            blk_height = self.__blk_proof['BlockHeight']
        except KeyError:
            raise SDKException(ErrorCode.invalid_blk_proof)
        block = self.__sdk.default_network.get_block_by_height(blk_height)
        tx_list = block.get('Transactions', list())
        tx_exist = False
        for tx in tx_list:
            if tx.get('Hash', '') == tx_hash:
                tx_exist = True
                break
        if not tx_exist:
            return False
        blk_head = block.get('Header', dict())
        target_hash = blk_head.get('TransactionsRoot', '')
        try:
            result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root, is_big_endian)
        except SDKException:
            result = False
        return result

    def to_json(self) -> str:
        return json.dumps(self.__blk_proof)

    def from_json(self, json_blk_proof: str, is_big_endian: bool = False):
        if not isinstance(json_blk_proof, str):
            raise SDKException(ErrorCode.require_str_params)
        try:
            dict_blk_proof = json.loads(json_blk_proof)
        except json.decoder.JSONDecodeError:
            raise SDKException(ErrorCode.invalid_b64_claim_data)
        proof = BlockchainProof(self.__sdk)
        proof.proof = dict_blk_proof, is_big_endian
        return proof

    def to_bytes(self) -> bytes:
        json_proof = self.to_json()
        return json_proof.encode('utf-8')

    def to_base64(self) -> str:
        return base64.b64encode(self.to_bytes()).decode('ascii')

    def from_base64(self, b64_blk_proof: str, is_big_endian: bool = False):
        json_blk_proof = base64.b64decode(b64_blk_proof).decode('utf-8')
        return self.from_json(json_blk_proof, is_big_endian)
