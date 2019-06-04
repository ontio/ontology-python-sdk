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

import time
import unittest

from Cryptodome.Random.random import randint

from ontology.utils.contract import Event
from ontology.common.address import Address

from tests import sdk, not_panic_exception, acct1, acct2, acct3, acct4


class TestOng(unittest.TestCase):
    def setUp(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        multi_address = Address.from_multi_pub_keys(2, pub_keys)
        self.address_list = [acct1.get_address_base58(), acct2.get_address_base58(), acct3.get_address_base58(),
                             acct4.get_address_base58(), multi_address.b58encode()]
        self.gas_price = 500
        self.gas_limit = 20000

    @not_panic_exception
    def test_get_asset_address(self):
        ong_address = '0200000000000000000000000000000000000000'
        self.assertEqual(ong_address, sdk.native_vm.ong().contract_address.hex())

    @not_panic_exception
    def test_query_name(self):
        token_name = sdk.native_vm.ong().name()
        self.assertEqual('ONG Token', token_name)

    @not_panic_exception
    def test_query_symbol(self):
        token_symbol = sdk.native_vm.ong().symbol()
        self.assertEqual('ONG', token_symbol)

    @not_panic_exception
    def test_query_decimals(self):
        decimals = sdk.native_vm.ong().decimals()
        self.assertEqual(9, decimals)

    @not_panic_exception
    def test_unbound_ong(self):
        for address in self.address_list:
            self.assertEqual(sdk.rpc.get_unbound_ong(address), sdk.native_vm.ong().unbound(address))

    @not_panic_exception
    def test_query_balance(self):
        for address in self.address_list:
            self.assertGreaterEqual(sdk.native_vm.ong().balance_of(address), 0)

    @not_panic_exception
    def test_query_allowance(self):
        allowance = sdk.native_vm.ong().allowance(acct1.get_address_base58(), acct2.get_address_base58())
        self.assertGreaterEqual(allowance, 0)

    @not_panic_exception
    def test_transfer(self):
        amount, gas_price, gas_limit = 1, 500, 20000
        tx_hash = sdk.native_vm.ong().transfer(acct1, acct2.get_address(), amount, acct4, gas_price,
                                               gas_limit)
        time.sleep(randint(14, 20))
        event = sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.ong().contract_address)
        self.assertEqual('transfer', notify[0]['States'][0])
        self.assertEqual(acct1.get_address_base58(), notify[0]['States'][1])
        self.assertEqual(acct2.get_address_base58(), notify[0]['States'][2])
        self.assertEqual(amount, notify[0]['States'][3])
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.ong().contract_address)
        self.assertEqual('transfer', notify[1]['States'][0])
        self.assertEqual(acct4.get_address_base58(), notify[1]['States'][1])
        self.assertEqual(gas_price * gas_limit, notify[1]['States'][3])

    @not_panic_exception
    def test_transfer_from_tx(self):
        acct2_b58_address = acct2.get_address_base58()
        tx_hash = sdk.native_vm.ong().transfer_from(acct2, acct1.get_address(), acct2_b58_address, 1,
                                                    acct2, self.gas_price, self.gas_limit)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(14, 20))
        event = sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify_list = Event.get_notify_by_contract_address(event, sdk.native_vm.ong().contract_address)
        self.assertEqual(2, len(notify_list))

    @not_panic_exception
    def test_withdraw_ong(self):
        amount = 1
        tx_hash = sdk.native_vm.ong().withdraw(acct1, acct1.get_address(), amount, acct2, self.gas_price,
                                               self.gas_limit)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(14, 20))
        event = sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.ong().contract_address)
        self.assertEqual('transfer', notify[0]['States'][0])
        self.assertEqual(acct1.get_address_base58(), notify[0]['States'][2])
        self.assertEqual(amount, notify[0]['States'][3])
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.ong().contract_address)
        self.assertEqual('transfer', notify[1]['States'][0])
        self.assertEqual(acct2.get_address_base58(), notify[1]['States'][1])
        self.assertEqual(self.gas_price * self.gas_limit, notify[1]['States'][3])

    @not_panic_exception
    def test_approve(self):
        tx_hash = sdk.native_vm.ong().approve(acct1, acct2.get_address(), 10, acct2, self.gas_price, self.gas_limit)
        self.assertEqual(64, len(tx_hash))

    @not_panic_exception
    def test_transfer_from(self):
        sdk.rpc.connect_to_test_net()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = acct2.get_address_base58()
        ong = sdk.native_vm.ong()
        tx_hash = ong.transfer_from(acct2, b58_from_address, b58_recv_address, 1, acct2, self.gas_price, self.gas_limit)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(14, 20))
        event = sdk.default_network.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, ong.contract_address)
        self.assertEqual(2, len(notify))


if __name__ == '__main__':
    unittest.main()
