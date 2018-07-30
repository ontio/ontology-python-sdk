import base64
from unittest import TestCase
from ontology.wallet.wallet_manager import WalletManager
from ontology.utils import util


class TestWalletManager(TestCase):
    def test_open_wallet(self):
        wm = WalletManager()
        wm.open_wallet("./test.json")
        account = wm.get_account("AWWCY5ZB4VnUTaHqFmpdRdqPsdZnPaQKMy","1")
        print(account.get_address_base58())
        print(account)

    def test_create_from_privateKey(self):
        wm = WalletManager()
        wm.open_wallet("./test2.json")
        account = wm.create_account_from_prikey("myaccount","1",util.hex_to_bytes("75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"))
        wm.save()
        print(account)

    def test_create_random_account(self):
        wm = WalletManager()
        wm.open_wallet("./test.json")
        acc = wm.create_random_account("mywallet","1")
        wm.save()
        print(acc)

    def test_import_account(self):
        wm = WalletManager()
        wm.open_wallet("./test4.json")
        wm.import_account("label2","Yl1e9ugbVADd8a2SbAQ56UfUvr3e9hD2eNXAM9xNjhnefB+YuNXDFvUrIRaYth+L","1",
                          "AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve",base64.b64decode("pwLIUKAf2bAbTseH/WYrfQ=="))
        wm.save()

    def test_create_random_identity(self):
        wm = WalletManager()
        wm.open_wallet("./test5.json")
        wm.create_random_identity("ide", "1")
        wm.save()

    def test_create_identity_from_privateKey(self):
        wm = WalletManager()
        wm.open_wallet("./test6.json")
        wm.create_identity_from_prikey("ide","1",util.hex_to_bytes("75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"))

