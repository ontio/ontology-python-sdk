#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme

rpc_address = 'http://polaris3.ont.io:20336'
# rpc_address = "http://127.0.0.1:20336"
sdk = OntologySdk()

private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
private_key4 = "f9d2d30ffb22dffdf4f14ad6f1303460efc633ea8a3014f638eaa19c259bada1"
acct1 = Account(private_key, SignatureScheme.SHA256withECDSA)
acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
acct4 = Account(private_key4, SignatureScheme.SHA256withECDSA)


class TestNativeVm(unittest.TestCase):
    def test_native_vm_transaction(self):
        sdk.set_rpc(rpc_address)
        asset = sdk.native_vm().asset()
        amount = 1
        tx = asset.new_transfer_transaction('ont', acct2.get_address_base58(), acct1.get_address_base58(), amount,
                                            acct1.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx, acct1)
        sdk.add_sign_transaction(tx, acct2)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('[Transfer] balance insufficient', e.args[1])
        tx = asset.new_transfer_transaction('ont', acct1.get_address_base58(), acct2.get_address_base58(), amount,
                                            acct1.get_address_base58(), 20000, 500)
        sdk.sign_transaction(tx, acct2)
        sdk.add_sign_transaction(tx, acct1)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('[Transfer] balance insufficient', e.args[1])

    def test_native_vm_withdraw_ong(self):
        sdk.set_rpc(rpc_address)
        payer = acct2
        b58_payer_address = payer.get_address_base58()
        amount = 1
        asset = sdk.native_vm().asset()
        tx = asset.new_withdraw_ong_transaction(b58_payer_address, b58_payer_address, amount, b58_payer_address, 20000,
                                                500)
        sdk.sign_transaction(tx, payer)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))


if __name__ == '__main__':
    unittest.main()
