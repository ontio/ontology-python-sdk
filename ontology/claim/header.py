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

from enum import Enum

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class ClmAlg(Enum):
    ES224 = 'ONT-ES224'
    ES256 = 'ONT-ES256'
    ES384 = 'ONT-ES384'
    ES512 = 'ONT-ES512'
    ES3_224 = 'ONT-ES3-224'
    ES3_256 = 'ONT-ES3-256'
    ES3_384 = 'ONT-ES3-384'
    ES3_512 = 'ONT-ES3-512'
    ER160 = 'ONT-ER160'
    SM = 'ONT-SM'
    EDS512 = 'ONT-EDS512'

    @staticmethod
    def from_str_alg(str_alg: str):
        if not isinstance(str_alg, str):
            raise SDKException(ErrorCode.require_str_params)
        if str_alg == 'ES224' or str_alg == 'ONT-ES224':
            return ClmAlg.ES224
        elif str_alg == 'ES256' or str_alg == 'ONT-ES256':
            return ClmAlg.ES256
        elif str_alg == 'ES384' or str_alg == 'ONT-ES384':
            return ClmAlg.ES384
        elif str_alg == 'ES512' or str_alg == 'ONT-ES512':
            return ClmAlg.ES512
        elif str_alg == 'ES3-224' or str_alg == 'ONT-ES3-224':
            return ClmAlg.ES3_224
        elif str_alg == 'ES3-256' or str_alg == 'ONT-ES3-256':
            return ClmAlg.ES3_256
        elif str_alg == 'ES3-384' or str_alg == 'ONT-ES3-384':
            return ClmAlg.ES3_384
        elif str_alg == 'ER160' or str_alg == 'ONT-ER160':
            return ClmAlg.ER160
        elif str_alg == 'SM' or str_alg == 'ONT-SM':
            return ClmAlg.SM
        elif str_alg == 'EDS512' or str_alg == 'ONT-EDS512':
            return ClmAlg.EDS512
        else:
            raise SDKException(ErrorCode.invalid_claim_alg)


class ClmType(Enum):
    raw_claim = 'JWT'
    witness_claim = 'JWT-X'

    @staticmethod
    def from_str_type(str_type: str):
        if not isinstance(str_type, str):
            raise SDKException(ErrorCode.require_str_params)
        if str_type == 'JWT':
            return ClmType.raw_claim
        elif str_type == 'JWT-X':
            return ClmType.witness_claim
        else:
            raise SDKException(ErrorCode.invalid_claim_type)


class Header(object):
    def __init__(self, kid: str, alg: ClmAlg or str = ClmAlg.ES256, claim_type: ClmType = ClmType.witness_claim):
        if not isinstance(kid, str):
            raise SDKException(ErrorCode.require_str_params)
        if isinstance(claim_type, str):
            claim_type = ClmType.from_str_type(claim_type)
        if isinstance(alg, str):
            alg = ClmAlg.from_str_alg(alg)
        if not isinstance(alg, ClmAlg):
            raise SDKException(ErrorCode.invalid_claim_head_params)
        if not isinstance(claim_type, ClmType):
            raise SDKException(ErrorCode.invalid_claim_head_params)
        self.__alg = alg
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
            raise SDKException(ErrorCode.invalid_claim_head_params)
        self.__alg = alg

    @property
    def type(self) -> ClmType:
        return self.__type

    @type.setter
    def type(self, claim_type: ClmType):
        if not isinstance(claim_type, ClmType):
            raise SDKException(ErrorCode.invalid_claim_head_params)
        self.__type = claim_type

    @property
    def kid(self):
        return self.__kid

    @kid.setter
    def kid(self, kid: str):
        if not isinstance(kid, str):
            raise SDKException(ErrorCode.invalid_claim_head_params)
        if 'did:ont:' not in kid:
            raise SDKException(ErrorCode.invalid_claim_head_params)
        if '#keys-' not in kid:
            raise SDKException(ErrorCode.invalid_claim_head_params)
        self.__kid = kid

    def to_json(self):
        return json.dumps(dict(self))

    @staticmethod
    def from_json(json_head: str):
        if not isinstance(json_head, str):
            raise SDKException(ErrorCode.require_str_params)
        dict_head = json.loads(json_head)
        try:
            alg = ClmAlg.from_str_alg(dict_head['alg'])
            typ = ClmType.from_str_type(dict_head['typ'])
            head = Header(dict_head['kid'], alg, typ)
        except KeyError:
            raise SDKException(ErrorCode.invalid_b64_claim_data)
        return head

    def to_bytes(self):
        return self.to_json().encode('utf-8')

    @staticmethod
    def from_bytes(bytes_head: bytes):
        if not isinstance(bytes_head, bytes):
            raise SDKException(ErrorCode.require_bytes_params)
        return Header.from_json(bytes_head.decode('utf-8'))

    def to_base64(self):
        return base64.b64encode(self.to_bytes()).decode('ascii')

    @staticmethod
    def from_base64(b64_head: str):
        if not isinstance(b64_head, str):
            raise SDKException(ErrorCode.require_str_params)
        return Header.from_bytes(base64.b64decode(b64_head))
