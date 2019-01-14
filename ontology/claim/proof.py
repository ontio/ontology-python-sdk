#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.merkle.merkle_verifier import MerkleVerifier


class BlockchainProof(object):
    def __init__(self, tx_hash: str = '', hex_contract_address: str = '', crt_blk_height: int = 0,
                 merkle_root: str = '', proof_node: list = None):
        if proof_node is None:
            proof_node = list()
        self.__blk_proof = dict(Type='MerkleProof', TxnHash=tx_hash, ContractAddr=hex_contract_address,
                                BlockHeight=crt_blk_height, MerkleRoot=merkle_root, Nodes=proof_node)

    def __iter__(self):
        for key, value in self.__blk_proof.items():
            yield (key, value)

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
            proof = BlockchainProof(blk_proof['TxnHash'], blk_proof['ContractAddr'], blk_proof['BlockHeight'],
                                    blk_proof['MerkleRoot'], blk_proof['Nodes'])
        except KeyError:
            raise SDKException(ErrorCode.invalid_blk_proof)
        if not proof.validate_blk_proof(is_big_endian):
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
            return False
        try:
            tx_hash = self.__blk_proof['TxnHash']
        except KeyError:
            return False
        proof_node = self.__blk_proof.get('Nodes', list())
        merkle_root = self.__blk_proof.get('MerkleRoot', '')
        import json
        print(json.dumps(dict(self.__blk_proof), indent=4))
        try:
            result = MerkleVerifier.validate_proof(proof_node, tx_hash, merkle_root, is_big_endian)
        except SDKException:
            result = False
        return result

    def to_json(self) -> str:
        return json.dumps(self.__blk_proof)

    @staticmethod
    def from_json(json_blk_proof: str, is_big_endian: bool = False):
        if not isinstance(json_blk_proof, str):
            raise SDKException(ErrorCode.require_str_params)
        try:
            dict_blk_proof = json.loads(json_blk_proof)
        except json.decoder.JSONDecodeError:
            raise SDKException(ErrorCode.invalid_b64_claim_data)
        proof = BlockchainProof()
        proof.proof = dict_blk_proof, is_big_endian
        return proof

    def to_bytes(self) -> bytes:
        json_proof = self.to_json()
        return json_proof.encode('utf-8')

    def to_base64(self) -> str:
        return base64.b64encode(self.to_bytes()).decode('ascii')

    @staticmethod
    def from_base64(b64_blk_proof: str, is_big_endian: bool = False):
        json_blk_proof = base64.b64decode(b64_blk_proof).decode('utf-8')
        return BlockchainProof.from_json(json_blk_proof, is_big_endian)
