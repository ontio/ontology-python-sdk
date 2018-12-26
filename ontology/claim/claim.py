#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
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
    def __init__(self, alg: ClmAlg = ClmAlg.ES256, claim_type: ClmType = ClmType.witness_claim, kid=''):
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


class Payload(object):
    def __init__(self, ver: str, iss: str, sub: str, iat: int, exp: int, jti: str, context: str, clm: dict,
                 clm_rev: dict):
        self.__version = ver
        self.__issuer = iss
        self.__subject = sub
        self.__issued_at = iat
        self.__exp = exp
        self.__jwt_id = jti
        self.__context = context
        self.__claim = clm
        self.__claim_revoke = clm_rev

    def __iter__(self):
        payload = dict(ver=self.__version, iss=self.__issuer, sub=self.__subject, iat=self.__issued_at, exp=self.__exp,
                       jti=self.__jwt_id)
        payload['@context'] = self.__context
        payload['clm'] = self.__claim
        payload['clm-rev'] = self.__claim_revoke
        for value, key in payload.items():
            yield (value, key)

    @property
    def ver(self):
        return self.__version

    @property
    def iss(self):
        return self.__issuer

    @property
    def sub(self):
        return self.__subject

    @property
    def iat(self):
        return self.__issued_at

    @property
    def exp(self):
        return self.__exp

    @property
    def jti(self):
        return self.__jwt_id

    @property
    def context(self):
        return self.__context

    @property
    def clm(self):
        return self.__claim

    @property
    def clm_rev(self):
        return self.__claim_revoke


class ClmSigFmt(Enum):
    pgp = 'pgp'


class SignatureInfo(object):
    def __init__(self, val: str, key_id: str, alg: ClmAlg = ClmAlg.ES256, fmt: ClmSigFmt = ClmSigFmt.pgp):
        if not isinstance(alg, ClmAlg):
            raise SDKException(ErrorCode.other_error('Invalid signature algorithm.'))
        if not isinstance(fmt, ClmSigFmt):
            raise SDKException(ErrorCode.other_error('Invalid signature format.'))
        self.__format = fmt
        self.__value = val
        self.__pub_key_id = key_id

    def __iter__(self):
        info = dict(Format=self.__format, Algorithm=self.__format, Value=self.__value, PublicKeyId=self.__pub_key_id)
        for value, key in info.items():
            yield (value, key)


class Claim(object):
    def __init__(self):
        self.__head = Header()
        self.__payload = Payload()
        self.__signature = SignatureInfo()
