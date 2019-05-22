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

import unittest

from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme


class SignatureSchemeTest(unittest.TestCase):
    def test_from_claim_alg(self):
        self.assertRaises(SDKException, SignatureScheme.from_claim_alg, '')
        alg_lst = ['ES224', 'ES256', 'ES384', 'ES512', 'ES3-224', 'ES3-256', 'ES3-384', 'ER160', 'SM', 'EDS512',
                   'ONT-ES224', 'ONT-ES256', 'ONT-ES384', 'ONT-ES512', 'ONT-ES3-224', 'ONT-ES3-256', 'ONT-ES3-384',
                   'ONT-ER160', 'ONT-SM', 'ONT-EDS512']
        scheme_lst = [SignatureScheme.SHA224withECDSA, SignatureScheme.SHA256withECDSA, SignatureScheme.SHA384withECDSA,
                      SignatureScheme.SHA512withECDSA, SignatureScheme.SHA3_224withECDSA,
                      SignatureScheme.SHA3_256withECDSA, SignatureScheme.SHA3_384withECDSA,
                      SignatureScheme.RIPEMD160withECDSA, SignatureScheme.SM3withSM2, SignatureScheme.EDDSAwithSHA256]
        p = len(scheme_lst)
        for index, alg in enumerate(alg_lst):
            self.assertEqual(scheme_lst[index % p], SignatureScheme.from_claim_alg(alg))


if __name__ == '__main__':
    unittest.main()
