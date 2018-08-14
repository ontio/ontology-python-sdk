from unittest import TestCase
from ontology.wallet.wallet_manager import WalletManager
import base64
from ontology.utils.util import get_random_bytes
from ontology.account.account import Account
from binascii import a2b_hex
from ontology.utils import util

class TestWalletManager(TestCase):
    def test_open_wallet(self):
        wm = WalletManager()
        wm.open_wallet("./test.json")
        print(wm.__dict__)

    def test_import_identity(self):
        wm = WalletManager()
        wm.open_wallet("./test.json")
        salt = util.get_random_str(16)
        privete_key = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct = Account(a2b_hex(privete_key.encode()))
        enpri = acct.export_gcm_encrypted_private_key("1", salt, 16384)
        wm.import_identity("label2", enpri, "1", salt, acct.get_address_base58())

    def test_create_identity_from_prikey(self):
        wm = WalletManager()
        wm.open_wallet("./test6.json")
        ide = wm.create_identity_from_prikey("ide", "1", util.hex_to_bytes(
            "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"))
        print(ide)

    def test_create_random_account(self):
        wm = WalletManager()
        wm.open_wallet("./test.json")
        acc = wm.create_random_account("mywallet", "1")
        wm.save()
        print(acc)

    def test_import_account(self):
        wm = WalletManager()
        wm.open_wallet("./test.json")
        wm.import_account("label2", "Yl1e9ugbVADd8a2SbAQ56UfUvr3e9hD2eNXAM9xNjhnefB+YuNXDFvUrIRaYth+L", "1",
                          "AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve", base64.b64decode("pwLIUKAf2bAbTseH/WYrfQ=="))
        wm.save()

    def test_create_account_from_prikey(self):
        wm = WalletManager()
        wm.open_wallet("/Users/zhaoxavi/test.txt")
        account = wm.create_account_from_prikey("myaccount", "1", util.hex_to_bytes(
            "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"))
        wm.save()
        print(account)
