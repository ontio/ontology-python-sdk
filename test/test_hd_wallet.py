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

from ontology.crypto.hd_private_key import HDPrivateKey
from ontology.crypto.hd_public_key import HDPublicKey


class TestHDWallet(unittest.TestCase):
    def setUp(self):
        mnemonic = 'obscure worry home pass museum toss else accuse limb hover denial alpha'
        self.master_key = HDPrivateKey.master_key_from_mnemonic(mnemonic)
        self.hex_master_key = 'ca4e4b66a17cb7100d841e814497f1301c3132a7e1be8eda0970279c74922d03'
        self.bip32_master_key = 'xprv9s21ZrQH143K35FjbVrmoa3vPpn7eWMt89YKvzj8a4n78dYhfpycujSdFierpu1wrKDCWy7zkS7JankWk5Dg1cnuhSjwJ1KeTxeRSuayTp5'
        self.hex_root_pk = '03faffcf6343265b1b4a835d3e84c46353fc4f008114e3f37c434f6147206cc397'
        self.hex_root_sk = 'f257af29ffc4cbd96899bdbb45210c417494f783b9be66ac69bd342c511d9e76'
        self.bip32_root_pk = 'xpub6CbjoChWbA9TdLQKghCH5GzRrvjPxTiz6kYkW3frXyyN6vfbR7wGkYqd9jyEqkpYRe33oe5sQbamndiWQjc9X3mr29HdKWqgjwb6G3xYXFo'
        self.bip32_root_sk = 'xprv9ycPPhAcknbAQrKraffGi93hJttuZ118jXd9hfGEyeSPE8LSsad2CkX9JSvv6eLWV3DZFfTAV3g1XxAVdKr69eoHhugTQscHt1XjdS4zuoj'

    def test_from_mnemonic(self):
        self.assertEqual(self.hex_master_key, self.master_key.hex())

    def test_bip32(self):
        self.assertEqual(self.bip32_master_key, self.master_key.b58encode())
        root_pk = HDPublicKey.b58decode(self.bip32_root_pk)
        root_sk = HDPrivateKey.b58decode(self.bip32_root_sk)
        self.assertEqual(self.hex_root_pk, root_pk.hex())
        self.assertEqual(self.hex_root_sk, root_sk.hex())

    def test_from_path(self):
        child_pub_keys = ['03a396e3676ee2d86345083915d05c024cad02cdad885df3d08a02c66301626a0c',
                          '0281bfed65dac125cacd98be68cf35602f63174c956e24408459b39b3ed8b4a095',
                          '02ebb7468da06b1cf2ef7e7560e2dfaeae41bf50248b9037fa945afdd6798ec09e',
                          '0344b62b833fdbba5a8ebd21ef6b7abab0bece5f9f6bfd77d1f7b8bf39a5e38c2c',
                          '027ea1d6eee9148d3bbd2eb9456f03a07ddfee6dd9f7d1979c46f1e691ade2058b',
                          '0395c57489f8353d308ff9c1c59d60a693ab9d3e805cd7325217c48438c3d876da',
                          '030a71d1f73c4a6701288faa13427bfce4bef9bf1b2e91ccc3a361204ebcdf4ec5',
                          '027897e5726cb27965da5a9b8e53c7ba07d2c0b0aafa57b14a741a2d66e63d3284',
                          '03d90387e9429e9b732b4979be9d9331ff58c7e123c6412a716f89839dbf330515',
                          '03e8f45af5351f97ebc01d5bacbf090317ca03f31df08d43a178f9292c02c550ab']
        root_keys = HDPrivateKey.from_path(self.master_key)
        self.assertEqual(4, len(root_keys))
        root_sk = root_keys[-1]
        root_pk = root_sk.public_key
        for i in range(10):
            child_sks = HDPrivateKey.from_path(root_sk, '{change}/{index}'.format(change=0, index=i))
            child_pks = HDPublicKey.from_path(root_pk, '{change}/{index}'.format(change=0, index=i))
            self.assertEqual(child_pub_keys[i], child_sks[-1].public_key.hex())
            self.assertEqual(child_pub_keys[i], child_pks[-1].hex())


if __name__ == '__main__':
    unittest.main()
