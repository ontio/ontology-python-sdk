#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from ontology.common.wallet_qr import WalletQR
from ontology.wallet.wallet_manager import WalletManager
from ontology.utils import util


class TestWalletQR(unittest.TestCase):
    def test_export_identity_qrcode(self):
        wm = WalletManager()
        pwd = "1"
        hex_private_key = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        identity = wm.create_identity_from_prikey("sss", pwd, hex_private_key)
        wqr = WalletQR()
        d = wqr.export_identity_qrcode(wm.wallet_file, identity)

        dstr = json.dumps(d, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)

        private_key = wqr.get_prikey_from_qrcode(dstr, pwd)
        self.assertEqual(private_key, hex_private_key)

if __name__ == '__main__':
    unittest.main()