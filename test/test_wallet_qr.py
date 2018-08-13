#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from unittest import TestCase

from ontology.common.wallet_qr import WalletQR
from ontology.wallet.wallet_manager import WalletManager
from ontology.utils import util


class TestWalletQR(TestCase):
    def test_export_identity_qrcode(self):
        wm = WalletManager()
        pwd = "1"
        identity = wm.create_identity_from_prikey("sss", pwd, util.hex_to_bytes(
            "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"))
        # account = wm.create_random_account("sss2", pwd)
        wqr = WalletQR()
        d = wqr.export_identity_qrcode(wm.wallet_file, identity)

        dstr = json.dumps(d, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)

        privatekey = wqr.get_prikey_from_qrcode(dstr, pwd)
        print(privatekey.hex())
