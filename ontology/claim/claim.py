#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64

from time import time
from typing import List

from ontology.claim.header import Header
from ontology.claim.payload import Payload
from ontology.account.account import Account
from ontology.crypto.digest import Digest
from ontology.crypto.key_type import KeyType
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.crypto.signature_handler import SignatureHandler


class Claim(object):
    def __init__(self, iss: Account, sub, kid: str, exp, jti, context, clm, clm_rev, ver: str = 'v1.0'):
        self.__head = Header(kid)
        self.__payload = Payload(ver, iss.get_ont_id(), sub, int(time()), exp, jti, context, clm, clm_rev)
        self.__signature = ''
        self.__blockchain_proof = ''

    def signature(self, iss: Account, scheme: SignatureScheme = SignatureScheme.SHA256withECDSA):
        str_head = self.__head.to_json_str()
        str_payload = self.__head.to_json_str()
        msg = f'{str_head}.{str_payload}'.encode('utf-8')
        handler = SignatureHandler(KeyType.from_signature_scheme(scheme), scheme)
        self.__signature = handler.generate_signature(iss.get_private_key_bytes(), msg)

    def to_b64_signature(self):
        return base64.b64encode(self.__signature)

    def to_bytes_signature(self):
        return self.__signature.encode('utf-8')

    def to_b64_blockchain_proof(self):
        return base64.b64encode(self.__blockchain_proof)

    def to_bytes_blockchain_proof(self):
        return self.__blockchain_proof.encode('utf-8')

    def get_claim_id(self):
        claim_str = self.generate_b64_claim()
        Digest.sha256(claim_str.encode('utf-8'))

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

    def generate_b64_claim(self):
        b64_head = self.__head.to_base64()
        b64_payload = self.__payload.to_base64()
        b64_signature = self.to_b64_signature()
        b64_blockchain_proof = self.to_b64_blockchain_proof()
        return f'{b64_head}.{b64_payload}.{b64_signature}.{b64_blockchain_proof}'
