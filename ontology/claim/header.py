#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import base64

from enum import Enum

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class ClmAlg(Enum):
    ES224 = 'ES224'
    ES256 = 'ES256'
    ES384 = 'ES384'
    ES512 = 'ES512'
    ES3_224 = 'ES3-224'
    ES3_256 = 'ES3-256'
    ES3_384 = 'ES3-384'
    ES3_512 = 'ES3-512'
    ER160 = 'ER160'
    SM = 'SM'
    EDS512 = 'EDS512'


class ClmType(Enum):
    raw_claim = 'JWT'
    witness_claim = 'JWT-X'


class Header(object):
    def __init__(self, kid: str, alg: ClmAlg = ClmAlg.ES256, claim_type: ClmType = ClmType.witness_claim):
        if not isinstance(alg, ClmAlg):
            raise SDKException(ErrorCode.other_error('Invalid signature algorithm.'))
        self.__alg = alg
        if not isinstance(claim_type, ClmType):
            raise SDKException(ErrorCode.other_error('Invalid claim type.'))
        self.__type = claim_type
        self.__kid = kid

    def __iter__(self):
        header = dict(alg=self.__alg.value, typ=self.__type.value, kid=self.__kid)
        for key, value in header.items():
            yield (key, value)

    @property
    def alg(self) -> ClmAlg:
        return self.__alg

    @alg.setter
    def alg(self, alg: ClmAlg):
        if not isinstance(alg, ClmAlg):
            raise SDKException(ErrorCode.other_error('Invalid signature algorithm.'))
        self.__alg = alg

    @property
    def type(self) -> ClmType:
        return self.__type

    @type.setter
    def type(self, claim_type: ClmType):
        if not isinstance(claim_type, ClmType):
            raise SDKException(ErrorCode.other_error('Invalid claim type.'))
        self.__type = claim_type

    @property
    def kid(self):
        return self.__kid

    @kid.setter
    def kid(self, kid: str):
        if not isinstance(kid, str):
            raise SDKException(ErrorCode.other_error('Invalid kid type.'))
        if 'did:ont:' not in kid:
            raise SDKException(ErrorCode.other_error('Invalid kid, OntId is incomplete.'))
        if '#keys-' not in kid:
            raise SDKException(ErrorCode.other_error('Invalid kid, public key is empty.'))

    def to_json_str(self):
        return json.dumps(dict(self))

    def to_bytes(self):
        return self.to_json_str().encode('utf-8')

    def to_base64(self):
        return base64.b64encode(self.to_json_str())
