#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


@unique
class SignatureScheme(Enum):
    SHA224withECDSA = 0
    SHA256withECDSA = 1
    SHA384withECDSA = 2
    SHA512withECDSA = 3
    SHA3_224withECDSA = 4
    SHA3_256withECDSA = 5
    SHA3_384withECDSA = 6
    SHA3_512withECDSA = 7
    RIPEMD160withECDSA = 8
    SM3withSM2 = 9
    EDDSAwithSHA256 = 10

    @staticmethod
    def from_claim_alg(alg: str):
        if not isinstance(alg, str):
            raise SDKException(ErrorCode.require_str_params)
        if alg == 'ES224' or alg == 'ONT-ES224':
            return SignatureScheme.SHA224withECDSA
        elif alg == 'ES256' or alg == 'ONT-ES256':
            return SignatureScheme.SHA256withECDSA
        elif alg == 'ES384' or alg == 'ONT-ES384':
            return SignatureScheme.SHA384withECDSA
        elif alg == 'ES512' or alg == 'ONT-ES512':
            return SignatureScheme.SHA512withECDSA
        elif alg == 'ES3-224' or alg == 'ONT-ES3-224':
            return SignatureScheme.SHA3_224withECDSA
        elif alg == 'ES3-256' or alg == 'ONT-ES3-256':
            return SignatureScheme.SHA3_256withECDSA
        elif alg == 'ES3-384' or alg == 'ONT-ES3-384':
            return SignatureScheme.SHA3_384withECDSA
        elif alg == 'ER160' or alg == 'ONT-ER160':
            return SignatureScheme.RIPEMD160withECDSA
        elif alg == 'SM' or alg == 'ONT-SM':
            return SignatureScheme.SM3withSM2
        elif alg == 'EDS512' or alg == 'ONT-EDS512':
            return SignatureScheme.EDDSAwithSHA256
        else:
            raise SDKException(ErrorCode.unknown_asymmetric_key_type)
