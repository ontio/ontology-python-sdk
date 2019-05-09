#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from test import sdk, acct1, acct2, not_panic_exception

from ontology.exception.exception import SDKException


class TestNativeVm(unittest.TestCase):
    @not_panic_exception
    def test_native_vm_transaction(self):
        amount = 1
        tx = sdk.native_vm.ont().new_transfer_tx(acct2.get_address_base58(), acct1.get_address_base58(), amount,
                                                 acct1.get_address_base58(), 500, 20000)
        tx.sign_transaction(acct1)
        tx.add_sign_transaction(acct2)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('[Transfer] balance insufficient', e.args[1])
        tx = sdk.native_vm.ont().new_transfer_tx(acct1.get_address_base58(), acct2.get_address_base58(), amount,
                                                 acct1.get_address_base58(), 500, 20000)
        tx.sign_transaction(acct2)
        tx.add_sign_transaction(acct1)
        try:
            tx_hash = sdk.rpc.send_raw_transaction(tx)
            self.assertEqual(64, len(tx_hash))
        except SDKException as e:
            self.assertIn('[Transfer] balance insufficient', e.args[1])

    @not_panic_exception
    def test_native_vm_withdraw_ong(self):
        payer = acct2
        b58_payer_address = payer.get_address_base58()
        amount = 1
        tx = sdk.native_vm.ong().new_withdraw_tx(b58_payer_address, b58_payer_address, amount, b58_payer_address, 500,
                                                 20000)
        tx.sign_transaction(payer)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))


if __name__ == '__main__':
    unittest.main()
