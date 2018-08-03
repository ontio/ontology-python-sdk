from binascii import a2b_hex
from unittest import TestCase
from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.native_contract.asset import Asset
import time
from ontology.utils.util import get_random_bytes

rpc_address = "http://polaris3.ont.io:20336"
sdk = OntologySdk()
private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
acc = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acc2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
acc3 = Account(a2b_hex(private_key3.encode()), SignatureScheme.SHA256withECDSA)


class TestAsset(TestCase):
    def test_tx(self):
        b = sdk.rpc.get_balance(acc.get_address_base58())
        b2 = sdk.rpc.get_balance(acc2.get_address_base58())
        print("acc:", b)
        print("acc2:", b2)
        tx = sdk.native_vm().asset().new_transfer_transaction("ont", acc.get_address().to_base58(),
                                                              acc2.get_address_base58(), 1, acc2.get_address_base58(),
                                                              20000, 500)
        tx = sdk.sign_transaction(tx, acc)
        tx = sdk.add_sign_transaction(tx, acc2)
        sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        b = sdk.rpc.get_balance(acc.get_address_base58())
        b2 = sdk.rpc.get_balance(acc2.get_address_base58())
        print("acc:", b)
        print("acc2:", b2)

    def test_new_transfer_transaction(self):
        tx = sdk.native_vm().asset().new_transfer_transaction("ont", acc.get_address().to_base58(),
                                                          acc2.get_address_base58(),
                                                          1, acc.get_address().to_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        b = sdk.rpc.get_balance(acc.get_address_base58())
        b2 = sdk.rpc.get_balance(acc2.get_address_base58())
        sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        bs = sdk.rpc.get_balance(acc.get_address_base58())
        b2s = sdk.rpc.get_balance(acc2.get_address_base58())
        assert int(b["ont"]) - int(bs["ont"]) == int(b2s["ont"]) - int(b2["ont"])
        aa = sdk.native_vm().asset().unboundong(sdk.rpc, acc.get_address_base58())
        if aa != "0":
            bb = int(aa)
            tx = sdk.native_vm().asset().new_withdraw_ong_transaction(acc.get_address_base58(), acc.get_address_base58(),
                                                                  bb, acc.get_address_base58(), 20000, 500)
            sdk.sign_transaction(tx, acc)
            sdk.rpc.send_raw_transaction(tx)
            time.sleep(6)
            aa2 = sdk.native_vm().asset().unboundong(sdk.rpc, acc.get_address_base58())
            assert aa2 == "0"

    def test_new_get_balance_transaction(self):
        result = sdk.native_vm().asset().query_balance("ont", acc.get_address_base58())
        assert int(result) >= 0
        result = sdk.native_vm().asset().query_name("ont")
        assert result != ""
        result = sdk.native_vm().asset().query_symbol("ont")
        assert result != ""
        result = sdk.native_vm().asset().query_decimals("ont")
        assert int(result) >= 0

    def test_send_approve(self):
        allowance = sdk.native_vm().asset().query_allowance("ont", acc.get_address_base58(),
                                                               acc2.get_address_base58())
        amount = 10
        tx2 = sdk.native_vm().asset().send_approve("ont", acc, acc2.get_address_base58(),
                                                          amount, acc, 20000, 500)

        time.sleep(6)
        allowance2 = sdk.native_vm().asset().query_allowance("ont", acc.get_address_base58(),
                                                               acc2.get_address_base58())

        if allowance == "":
            allowance = "0"
        # assert int(allowance2, 16) - int(allowance, 16) == amount
        tx2 = sdk.native_vm().asset().new_transfer_from("ont", acc2.get_address_base58(),
                                                                   acc.get_address_base58(), acc2.get_address_base58(),
                                                                   amount, acc2.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx2, acc2)
        sdk.rpc.send_raw_transaction(tx2)
        time.sleep(6)
        allowance3 = sdk.native_vm().asset().query_allowance("ont", acc.get_address_base58(),
                                                               acc2.get_address_base58())

        if allowance3 == "":
            allowance3 = "0"
        assert allowance == allowance3

    def test_query_balance(self):
        a = Asset(sdk)
        res = a.query_balance("ont", acc.get_address().to_base58())
        print(res)

    def test_query_allowance(self):
        a = Asset(sdk)
        res = a.query_allowance("ont", acc.get_address().to_base58(), acc2.get_address().to_base58())
        print(res)

    def test_query_name(self):
        a = Asset(sdk)
        res = a.query_name("ont")
        print(res)

    def test_query_symbol(self):
        a = Asset(sdk)
        res = a.query_symbol("ont")
        print(res)

    def test_query_decimals(self):
        a = Asset(sdk)
        res = a.query_decimals("ong")
        print(res)

    def test_send_withdraw_ong_transaction(self):
        a = Asset(sdk)
        res = a.send_withdraw_ong_transaction(acc, acc2.get_address_base58(), 1, acc3, 20000, 500)
        print(res)

    def test_send_approve2(self):
        a = Asset(sdk)
        res = a.send_approve("ont", acc, acc2.get_address_base58(), 1, acc3, 20000, 500)
        print(res)
