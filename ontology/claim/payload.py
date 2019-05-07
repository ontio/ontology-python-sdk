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

from ontology.crypto.digest import Digest
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Payload(object):
    def __init__(self, ver: str, iss_ont_id: str, sub_ont_id: str, iat: int, exp: int, context: str, clm: dict,
                 clm_rev: dict, jti: str = ''):
        if not isinstance(ver, str):
            raise SDKException(ErrorCode.require_str_params)
        if not isinstance(iss_ont_id, str):
            raise SDKException(ErrorCode.require_str_params)
        if not isinstance(sub_ont_id, str):
            raise SDKException(ErrorCode.require_str_params)
        if not isinstance(iat, int):
            raise SDKException(ErrorCode.require_int_params)
        if not isinstance(clm, dict):
            raise SDKException(ErrorCode.require_dict_params)
        if not isinstance(clm_rev, dict):
            raise SDKException(ErrorCode.require_dict_params)
        if not isinstance(jti, str):
            raise SDKException(ErrorCode.require_str_params)
        self.__version = ver
        self.__issuer_ont_id = iss_ont_id
        self.__subject = sub_ont_id
        self.__issued_at = iat
        self.__exp = exp
        self.__context = context
        self.__claim = clm
        self.__claim_revoke = clm_rev
        self.__jwt_id = jti
        if self.__jwt_id == '':
            self.__jwt_id = Digest.sha256(json.dumps(dict(self)).encode('utf-8'), is_hex=True)

    def __iter__(self):
        payload = dict(ver=self.__version, iss=self.__issuer_ont_id, sub=self.__subject, iat=self.__issued_at,
                       exp=self.__exp, jti=self.__jwt_id)
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
        return self.__issuer_ont_id

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
        return base64.b64encode(self.to_bytes()).decode('ascii')

    @staticmethod
    def from_base64(b64_payload: str):
        json_payload = base64.b64decode(b64_payload).decode('utf-8')
        dict_payload = json.loads(json_payload)
        try:
            payload = Payload(dict_payload['ver'], dict_payload['iss'], dict_payload['sub'], dict_payload['iat'],
                              dict_payload['exp'], dict_payload['@context'], dict_payload['clm'],
                              dict_payload['clm-rev'], dict_payload['jti'])
        except KeyError:
            raise SDKException(ErrorCode.invalid_b64_claim_data)
        return payload
