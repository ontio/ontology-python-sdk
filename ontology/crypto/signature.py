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

from ecdsa import util, curves, SigningKey

from ontology.crypto.curve import Curve
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme


class Signature(object):
    def __init__(self, signature_scheme: SignatureScheme, signature_value):
        self.__scheme = signature_scheme
        self.__value = signature_value

    @staticmethod
    def ec_get_public_key_by_private_key(private_key: bytes, curve_name) -> bytes:
        if curve_name == Curve.P256:
            private_key = SigningKey.from_string(string=private_key, curve=curves.NIST256p)
            verifying_key = private_key.get_verifying_key()
            order = verifying_key.pubkey.order
            x_int = verifying_key.pubkey.point.x()
            y_int = verifying_key.pubkey.point.y()
            x_str = util.number_to_string(x_int, order)
            if y_int % 2 == 0:
                point_str = util.b('\x02') + x_str
            else:
                point_str = util.b('\x03') + x_str
        elif curve_name == Curve.P224:
            raise SDKException(ErrorCode.unsupported_key_type)
        elif curve_name == Curve.P384:
            raise SDKException(ErrorCode.unsupported_key_type)
        elif curve_name == Curve.P521:
            raise SDKException(ErrorCode.unsupported_key_type)
        else:
            raise SDKException(ErrorCode.unsupported_key_type)
        return point_str

    def to_bytes(self):
        if self.__scheme != SignatureScheme.SHA256withECDSA:
            raise SDKException(ErrorCode.unsupported_signature_scheme)
        return bytes.fromhex(self.__value)