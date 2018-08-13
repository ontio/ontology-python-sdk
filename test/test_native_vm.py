#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import a2b_hex
import unittest

from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk

rpc_address = "http://polaris3.ont.io:20336"
# rpc_address = "http://127.0.0.1:20336"
sdk = OntologySdk()

private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
private_key4 = "f9d2d30ffb22dffdf4f14ad6f1303460efc633ea8a3014f638eaa19c259bada1"
acct1 = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acct2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
acct3 = Account(a2b_hex(private_key3.encode()), SignatureScheme.SHA256withECDSA)
acct4 = Account(a2b_hex(private_key4.encode()), SignatureScheme.SHA256withECDSA)


class TestNativeVm(unittest.TestCase):
    def test_native_vm_transaction(self):
        sdk.set_rpc(rpc_address)
        tx = sdk.native_vm().asset().new_transfer_transaction("ont", acct2.get_address_base58(),
                                                              acct1.get_address_base58(), 120,
                                                              acct1.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx, acct1)
        sdk.add_sign_transaction(tx, acct2)
        res = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(len(res), 64)

    def test_native_vm_withdraw_ong(self):
        sdk.set_rpc(rpc_address)
        tx = sdk.native_vm().asset().new_withdraw_ong_transaction(acct4.get_address_base58(),
                                                                  acct4.get_address_base58(), 1352419563015000,
                                                                  acct4.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx, acct4)
        hex_address = acct4.get_address_hex()
        res = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(res[11:51], hex_address)


if __name__ == '__main__':
    unittest.main()
