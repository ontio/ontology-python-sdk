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

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Control(object):
    def __init__(self, kid: str = '', address='', enc_alg="aes-256-gcm", key='', algorithm='ECDSA', salt='', param=None,
                 hash_value='sha256', public_key=''):
        if param is None:
            param = dict(curve='P-256')
        if not isinstance(kid, str):
            raise SDKException(ErrorCode.require_str_params)
        self.__address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.hash = hash_value
        self.__kid = kid
        self.__key = key
        self.parameters = param
        self.__salt = salt
        self.__public_key = public_key

    def __iter__(self):
        data = dict()
        data['address'] = self.__address
        data['algorithm'] = self.algorithm
        data['enc-alg'] = self.enc_alg
        data['hash'] = self.hash
        data['id'] = self.__kid
        data['key'] = self.key
        data['parameters'] = self.parameters
        data['salt'] = self.__salt
        data['publicKey'] = self.__public_key
        for key, value in data.items():
            yield (key, value)

    @property
    def kid(self):
        return self.__kid

    @kid.setter
    def kid(self, kid: str):
        if not isinstance(kid, str):
            raise SDKException(ErrorCode.require_str_params)
        self.__kid = kid

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):
        if not isinstance(key, str):
            raise SDKException(ErrorCode.require_str_params)
        self.__key = key

    @property
    def b58_address(self):
        return self.__address

    @b58_address.setter
    def b58_address(self, b58_address: str):
        if not isinstance(b58_address, str):
            raise SDKException(ErrorCode.require_str_params)
        self.__address = b58_address

    @property
    def public_key(self):
        return self.__public_key

    @public_key.setter
    def public_key(self, b64_pub_key: str):
        if not isinstance(b64_pub_key, str):
            raise SDKException(ErrorCode.other_error('Invalid public key.'))
        self.__public_key = b64_pub_key

    @property
    def salt(self):
        return self.__salt

    @salt.setter
    def salt(self, salt: str):
        if not isinstance(salt, str):
            raise SDKException(ErrorCode.require_str_params)
        self.__salt = salt
