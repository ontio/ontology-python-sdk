"""
Copyright (C) 2018-2019 The ontology Authors
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

from tests import sdk, acct1, acct2, not_panic_exception


class TestNativeVm(unittest.TestCase):
    @not_panic_exception
    def test_native_vm_transaction(self):
        amount = 1
        tx = sdk.native_vm.ont().new_transfer_tx(acct2.get_address_base58(), acct1.get_address_base58(), amount,
                                                 acct1.get_address_base58(), 500, 20000)
        tx.sign_transaction(acct1)
        tx.add_sign_transaction(acct2)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))
        tx = sdk.native_vm.ont().new_transfer_tx(acct1.get_address_base58(), acct2.get_address_base58(), amount,
                                                 acct1.get_address_base58(), 500, 20000)
        tx.sign_transaction(acct2)
        tx.add_sign_transaction(acct1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))

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
