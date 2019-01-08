#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique

from ontology.crypto.signature_scheme import SignatureScheme
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


@unique
class KeyType(Enum):
    ECDSA = b'\x12'
    SM2 = b'\x13'
    EDDSA = b'\x14'

    def __init__(self, b: int):
        self.label = b

    def get_label(self):
        return self.label

    @staticmethod
    def from_label(label: int):
        label = bytes([label])
        if KeyType.ECDSA.value == label:
            return KeyType.ECDSA
        elif KeyType.SM2.value == label:
            return KeyType.SM2
        elif KeyType.EDDSA.value == label:
            return KeyType.EDDSA

    @staticmethod
    def from_pubkey(pubkey: bytes):
        if len(pubkey) == 33:
            return KeyType.ECDSA
        else:
            return KeyType.from_label(pubkey[0])

    @staticmethod
    def from_str_type(str_type: str):
        if not isinstance(str_type, str):
            raise SDKException(ErrorCode.require_str_params)
        if str_type == 'ECDSA':
            return KeyType.ECDSA
        elif str_type == 'SM2':
            return KeyType.SM2
        elif str_type == 'EDDSA':
            return KeyType.ECDSA
        else:
            raise SDKException(ErrorCode.unknown_asymmetric_key_type)

    @staticmethod
    def from_signature_scheme(scheme: SignatureScheme):
        if scheme == SignatureScheme.SHA224withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA256withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA384withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA384withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA512withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_224withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_256withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_384withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_512withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.RIPEMD160withECDSA:
            return KeyType.ECDSA
        elif scheme == SignatureScheme.SM3withSM2:
            return KeyType.SM2
        else:
            raise SDKException(ErrorCode.other_error('invalid signature scheme.'))
