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


class AccountData(object):
    def __init__(self, b58_address: str = '', enc_alg: str = 'aes-256-gcm', key: str = '', algorithm: str = 'ECDSA',
                 salt: str = '', param: dict = None, label: str = "", public_key: str = '',
                 sig_scheme: str = 'SHA256withECDSA', is_default: bool = True, lock: bool = False):
        if param is None:
            param = dict(curve='P-256')
        self.__b58_address = b58_address
        self.__algorithm = algorithm
        self.__enc_alg = enc_alg
        self.__is_default = is_default
        self.__key = key
        self.__label = label
        self.__lock = lock
        self.__parameters = param
        self.__salt = salt
        self.__public_key = public_key
        self.__signature_scheme = sig_scheme

    def __iter__(self):
        data = dict()
        data['address'] = self.__b58_address
        data['algorithm'] = self.__algorithm
        data['enc-alg'] = self.__enc_alg
        data['isDefault'] = self.__is_default
        data['key'] = self.__key
        data['label'] = self.__label
        data['lock'] = self.__lock
        data['parameters'] = self.__parameters
        data['salt'] = self.__salt
        data['publicKey'] = self.__public_key
        data['signatureScheme'] = self.__signature_scheme
        for key, value in data.items():
            yield (key, value)

    @property
    def b58_address(self):
        return self.__b58_address

    @b58_address.setter
    def b58_address(self, b58_address: str):
        if not isinstance(b58_address, str):
            raise SDKException(ErrorCode.other_error('Invalid base58 encode address.'))
        self.__b58_address = b58_address

    @property
    def algorithm(self):
        return self.__algorithm

    @algorithm.setter
    def algorithm(self, alg):
        self.__algorithm = alg

    @property
    def enc_alg(self):
        return self.__enc_alg

    @enc_alg.setter
    def enc_alg(self, enc_alg: str):
        if not isinstance(enc_alg, str):
            raise SDKException(ErrorCode.other_error('Invalid encryption algorithm.'))
        self.__enc_alg = enc_alg

    @property
    def is_default(self):
        return self.__is_default

    @is_default.setter
    def is_default(self, is_default: bool):
        if not isinstance(is_default, bool):
            raise SDKException(ErrorCode.other_error('Invalid default account state.'))
        self.__is_default = is_default

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):
        if not isinstance(key, str):
            raise SDKException(ErrorCode.other_error('Invalid key type.'))
        self.__key = key

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, label: str):
        if not isinstance(label, str):
            raise SDKException(ErrorCode.other_error('Invalid label.'))
        self.__label = label

    @property
    def lock(self):
        return self.__lock

    @lock.setter
    def lock(self, lock: bool):
        if not isinstance(lock, bool):
            raise SDKException(ErrorCode.other_error('Invalid lock state.'))
        self.__lock = lock

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, param: dict):
        if not isinstance(param, dict):
            raise SDKException(ErrorCode.other_error('Invalid parameters type.'))
        self.__parameters = param

    @property
    def salt(self):
        return self.__salt

    @salt.setter
    def salt(self, salt: str):
        if not isinstance(salt, str):
            raise SDKException(ErrorCode.other_error('Invalid salt.'))
        self.__salt = salt

    @property
    def public_key(self):
        return self.__public_key

    @public_key.setter
    def public_key(self, pub_key: str):
        if not isinstance(pub_key, str):
            raise SDKException(ErrorCode.other_error('Invalid public key.'))
        self.__public_key = pub_key

    @property
    def signature_scheme(self):
        return self.__signature_scheme

    @signature_scheme.setter
    def signature_scheme(self, sig_scheme: str):
        if not isinstance(sig_scheme, str):
            raise SDKException(ErrorCode.other_error('Invalid signature scheme.'))
        self.__signature_scheme = sig_scheme
