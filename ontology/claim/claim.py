#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import base64

from time import time

from ontology.claim.header import Header
from ontology.claim.payload import Payload
from ontology.account.account import Account
from ontology.claim.signature import SignatureInfo
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
        self.__merkle_proof = ''

    def signature(self, iss: Account, scheme: SignatureScheme = SignatureScheme.SHA256withECDSA):
        str_head = self.__head.to_json_str()
        str_payload = self.__head.to_json_str()
        msg = f'{str_head}.{str_payload}'.encode('utf-8')
        handler = SignatureHandler(KeyType.from_signature_scheme(scheme), scheme)
        self.__signature = handler.generate_signature(iss.get_private_key_bytes(), msg)

    def b64_signature_info(self):
        return base64.b64encode(self.__signature)

    def generate_claim_str(self):
        b64_head = self.__head.b64encode()
        b64_payload = self.__payload.b64encode()
        b64_signature = self.b64_signature_info()
        return f'{b64_head}.{b64_payload}.{b64_signature}'
