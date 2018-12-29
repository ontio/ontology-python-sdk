#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import base64

from ontology.crypto.digest import Digest
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Payload(object):
    def __init__(self, ver: str, iss: str, sub: str, iat: int, exp: int, context: str, clm: dict,
                 clm_rev: dict, jti: str = ''):
        if not isinstance(jti, str):
            raise (SDKException(ErrorCode.other_error('Invalid jti')))
        self.__version = ver
        self.__issuer = iss
        self.__subject = sub
        self.__issued_at = iat
        self.__exp = exp
        self.__context = context
        self.__claim = clm
        self.__claim_revoke = clm_rev
        self.__jwt_id = jti
        if self.__jwt_id == '':
            self.__jwt_id = Digest.sha256(json.dumps(dict(self)).encode('utf-8'), is_hex=True)

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

    def to_json_str(self):
        return json.dumps(dict(self))

    def to_bytes(self):
        return self.to_json_str().encode('utf-8')

    def to_base64(self):
        return base64.b64encode(self.to_json_str())
