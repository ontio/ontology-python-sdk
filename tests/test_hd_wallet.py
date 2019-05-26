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

from ontology.account.account import Account
from ontology.crypto.mnemonic import Mnemonic
from ontology.crypto.hd_public_key import HDPublicKey
from ontology.crypto.hd_private_key import HDPrivateKey
from ontology.crypto.signature_handler import SignatureHandler
from ontology.crypto.signature_scheme import SignatureScheme


class TestHDWallet(unittest.TestCase):
    def setUp(self):
        self.msg = b'Attack!'
        self.mnemonic = Mnemonic()
        self.strengths = [128, 160, 192, 224, 256]
        self.words = [12, 15, 18, 21, 24]
        self.mnemonic_lst = ['cargo cradle solid excuse rifle wrist forward orchard time athlete slab industry',
                             'wear snack remain farm jealous label space obey fault upon frown report shield garden student',
                             'blanket clarify twelve state mule sport below clog aspect myself neck dumb monkey spatial mobile admit season seminar',
                             'tomorrow stable casual write adult bean wisdom give duty sound blanket vanish grab junior crystal duck advice print tail purse orient',
                             'modify moon weird cloud crane grace cheap useless canoe fashion also cement zebra amount pink ocean saddle art fun jewel smooth upon abandon network']
        self.master_keys = list()
        for _, m in enumerate(self.mnemonic_lst):
            self.master_keys.append(HDPrivateKey.master_key_from_mnemonic(m))
        self.hex_master_keys = ['99c7b4ef1a126c4efd84decaa918c45d90f87f8eaba0d32bb113a7f3e4118162',
                                '652c39c190b87677211729c3cb73e9bb18867cd26145fb8a6088bd1c9b10b566',
                                'f006f6636cb57947a318e05e95f355e3f44f285d8f35f34389b6764f78accc3e',
                                'e020eeac158d3d51bcd525d35402664a6d8d756d1cd92a7f6a85d557b35a4592',
                                'dd7b20932f6e50ee28f9a930cb0d70cc57aa9a9634bf59f9687523ab7cebf42e']

    def test_generate_mnemonic(self):
        for index, strength in enumerate(self.strengths):
            code = self.mnemonic.generate(strength)
            self.assertEqual(self.words[index], len(code.split(' ')))

    def test_signature(self):
        for strength in self.strengths:
            master_key = HDPrivateKey.master_key_from_mnemonic(self.mnemonic.generate(strength))
            acct = Account(master_key.hex())
            signature = acct.generate_signature(self.msg)
            self.assertTrue(acct.verify_signature(self.msg, signature))
            root_sk = HDPrivateKey.from_path(master_key)[-1]
            root_pk = root_sk.public_key
            bip32_root_pk = root_pk.b58encode()
            for index in range(10):
                child_sk = HDPrivateKey.from_path(root_sk, f'0/{index}')[-1]
                child_pk = HDPublicKey.from_path(HDPublicKey.b58decode(bip32_root_pk), f'0/{index}')[-1]
                child_acct = Account(child_sk.hex())
                signature = child_acct.generate_signature(self.msg)
                handler = SignatureHandler(SignatureScheme.SHA256withECDSA)
                handler.verify_signature(child_pk.hex(), self.msg, signature)

    def test_from_mnemonic(self):
        for index, mnemonic in enumerate(self.mnemonic_lst):
            master_key = HDPrivateKey.master_key_from_mnemonic(mnemonic)
            self.assertEqual(self.hex_master_keys[index], master_key.hex())

    def test_bip32(self):
        for index, master_key in enumerate(self.master_keys):
            self.assertEqual('xprv', master_key.b58encode()[:4])
            self.assertEqual('xpub', master_key.public_key.b58encode()[:4])
            self.assertEqual(self.hex_master_keys[index], HDPrivateKey.b58decode(master_key.b58encode()).hex())

    def test_from_path(self):
        for master_key in self.master_keys:
            root_keys = HDPrivateKey.from_path(master_key)
            self.assertEqual(4, len(root_keys))
            root_sk = root_keys[-1]
            root_pk = root_sk.public_key
            bip32_root_sk = root_sk.b58encode()
            bip32_root_pk = root_pk.b58encode()
            for index in range(10):
                child_sks_from_root_key = HDPrivateKey.from_path(root_sk, f'0/{index}')
                child_sks_from_bip32_sk = HDPrivateKey.from_path(HDPrivateKey.b58decode(bip32_root_sk),
                                                                 f'0/{index}')
                for i, sk in enumerate(child_sks_from_root_key):
                    self.assertEqual(child_sks_from_bip32_sk[i].hex(), sk.hex())
                child_pks_from_root_key = HDPublicKey.from_path(root_pk, f'0/{index}')
                child_pks_from_bip32_pk = HDPublicKey.from_path(HDPublicKey.b58decode(bip32_root_pk), f'0/{index}')
                for i, pk in enumerate(child_pks_from_root_key):
                    self.assertEqual(child_pks_from_bip32_pk[i].hex(), pk.hex())
                    self.assertEqual(child_sks_from_bip32_sk[i].public_key.hex(), pk.hex())


if __name__ == '__main__':
    unittest.main()
