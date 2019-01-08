#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import base64
import binascii

from time import time
from typing import List

from ontology.claim.header import Header
from ontology.crypto.digest import Digest
from ontology.claim.payload import Payload
from ontology.account.account import Account
from ontology.crypto.key_type import KeyType
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.crypto.signature_handler import SignatureHandler
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.merkle.merkle_verifier import MerkleVerifier


class Claim(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__head = None
        self.__payload = None
        self.__signature = ''
        self.__blockchain_proof = ''

    def __iter__(self):
        data = dict(Header=dict(self.__head), Payload=dict(self.__payload), Signature=self.__signature,
                    Proof=self.__blockchain_proof)
        for key, value in data.items():
            yield (key, value)

    def set_claim(self, kid: str, iss_ont_id: str, sub_ont_id: str, exp: int, context: str, clm: dict, clm_rev: dict,
                  jti: str = '', ver: str = 'v1.0'):
        if not isinstance(jti, str):
            raise SDKException(ErrorCode.require_str_params)
        if jti == '':
            jti = Digest.sha256(uuid.uuid1().bytes, is_hex=True)
        self.__head = Header(kid)
        self.__payload = Payload(ver, iss_ont_id, sub_ont_id, int(time()), exp, context, clm, clm_rev, jti)

    def generate_signature(self, iss: Account, scheme: SignatureScheme = SignatureScheme.SHA256withECDSA):
        if not isinstance(self.__head, Header) or not isinstance(self.__payload, Payload):
            raise SDKException(ErrorCode.other_error('Please set claim parameters first.'))
        key_index = int(self.__head.kid.split('-')[1])
        result = self.__sdk.native_vm.ont_id().verify_signature(iss.get_ont_id(), key_index, iss)
        if not result:
            raise SDKException(ErrorCode.other_error('Issuer account error.'))
        b64_head = self.__head.to_base64()
        b64_payload = self.__payload.to_base64()
        msg = f'{b64_head}.{b64_payload}'.encode('utf-8')
        handler = SignatureHandler(KeyType.from_signature_scheme(scheme), scheme)
        self.__signature = handler.generate_signature(iss.get_private_key_hex(), msg)

    @property
    def claim_id(self):
        if not isinstance(self.__payload, Payload):
            return ''
        return self.__payload.jti

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, kid: str):
        if not isinstance(kid, str):
            raise SDKException(ErrorCode.require_str_params)
        self.__head = Header(kid)

    @property
    def payload(self):
        return self.__payload

    @property
    def signature(self):
        return self.__signature

    @property
    def blockchain_proof(self):
        return self.__blockchain_proof

    def to_bytes_signature(self):
        return self.__signature.encode('utf-8')

    def to_b64_signature(self):
        return base64.b64encode(binascii.a2b_hex(self.__signature)).decode('ascii')

    def to_b64_blockchain_proof(self):
        return base64.b64encode(self.__blockchain_proof.encode('utf-8')).decode('ascii')

    def to_bytes_blockchain_proof(self):
        return self.__blockchain_proof.encode('utf-8')

    def generate_blockchain_proof(self, tx_hash: str, hex_contract_address: str):
        if len(tx_hash) != 64:
            raise SDKException(ErrorCode.other_error('Invalid TxHash.'))
        if len(hex_contract_address) != 40:
            raise SDKException(ErrorCode.other_error('Invalid contract address.'))
        merkle_proof = self.__sdk.get_network().get_merkle_proof(tx_hash)
        current_block_height = merkle_proof['CurBlockHeight']
        target_hash = merkle_proof['TransactionsRoot']
        merkle_root = merkle_proof['CurBlockRoot']
        tx_block_height = self.__sdk.get_network().get_block_height_by_tx_hash(tx_hash)
        target_hash_list = merkle_proof['TargetHashes']
        proof_node = MerkleVerifier.get_proof(tx_block_height, target_hash_list, current_block_height)
        result = MerkleVerifier.validate_proof(proof_node, target_hash, merkle_root)
        if not result:
            raise SDKException(ErrorCode.other_error('Invalid merkle proof'))
        blockchain_proof = dict(Type='MerkleProof', TxnHash=tx_hash, ContractAddr=hex_contract_address,
                                BlockHeight=current_block_height, MerkleRoot=merkle_root, Nodes=proof_node)
        return blockchain_proof

    def generate_b64_claim(self):
        b64_head = self.__head.to_base64()
        b64_payload = self.__payload.to_base64()
        b64_signature = self.to_b64_signature()
        b64_blockchain_proof = self.to_b64_blockchain_proof()
        return f'{b64_head}.{b64_payload}.{b64_signature}.{b64_blockchain_proof}'
