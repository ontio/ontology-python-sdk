"""
Copyright (C) 2018 The ontology Authors
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


class TestOnt(unittest.TestCase):
    def setUp(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        multi_address = Address.from_multi_pub_keys(2, pub_keys)
        self.address_list = [acct1.get_address_base58(), acct2.get_address_base58(), acct3.get_address_base58(),
                             acct4.get_address_base58(), multi_address.b58encode()]
        self.gas_price = 500
        self.gas_limit = 20000

    @not_panic_exception
    def test_get_asset_address(self):
        ont_address = '0100000000000000000000000000000000000000'
        self.assertEqual(ont_address, sdk.native_vm.ont().contract_address.hex())

    @not_panic_exception
    def test_query_name(self):
        token_name = sdk.native_vm.ont().name()
        self.assertEqual('ONT Token', token_name)

    @not_panic_exception
    def test_query_symbol(self):
        token_symbol = sdk.native_vm.ont().symbol()
        self.assertEqual('ONT', token_symbol)

    @not_panic_exception
    def test_query_decimals(self):
        decimals = sdk.native_vm.ont().decimals()
        self.assertEqual(0, decimals)

    def test_query_balance(self):
        for address in self.address_list:
            self.assertGreaterEqual(sdk.native_vm.ont().balance_of(address), 0)

    def test_query_allowance(self):
        allowance = sdk.native_vm.ont().allowance(acct1.get_address_base58(), acct2.get_address_base58())
        self.assertGreaterEqual(allowance, 0)

    @not_panic_exception
    def test_transfer(self):
        amount, gas_price, gas_limit = 1, 500, 20000
        ont = sdk.native_vm.ont()
        tx_hash = ont.transfer(acct1, acct2.get_address(), amount, acct4, gas_price, gas_limit)
        time.sleep(randint(14, 20))
        event = sdk.aio_rpc.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, ont.contract_address)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(acct1.get_address_base58(), notify['States'][1])
        self.assertEqual(acct2.get_address_base58(), notify['States'][2])
        self.assertEqual(amount, notify['States'][3])
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.aio_ong().contract_address)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(acct4.get_address_base58(), notify['States'][1])
        self.assertEqual(gas_price * gas_limit, notify['States'][3])

    @not_panic_exception
    def test_transfer_from_tx(self):
        acct2_b58_address = acct2.get_address_base58()
        tx_hash = sdk.native_vm.ont().transfer_from(acct2, acct1.get_address(), acct2_b58_address, 1, acct2,
                                                        500, 20000)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(14, 20))
        event = sdk.aio_rpc.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.ont().contract_address)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(acct1.get_address_base58(), notify['States'][1])
        self.assertEqual(acct2.get_address_base58(), notify['States'][2])
        self.assertEqual(1, notify['States'][3])

    @not_panic_exception
    def test_approve(self):
        tx_hash = sdk.native_vm.ont().approve(acct1, acct2.get_address(), 10, acct2, 500, 20000)
        self.assertEqual(64, len(tx_hash))

    @not_panic_exception
    def test_transfer_from(self):
        sdk.rpc.connect_to_test_net()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = acct2.get_address_base58()
        ont = sdk.native_vm.ont()
        amount = 1
        tx_hash = ont.transfer_from(acct2, b58_from_address, b58_recv_address, amount, acct2, self.gas_price,
                                    self.gas_limit)
        self.assertEqual(64, len(tx_hash))
        time.sleep(randint(10, 15))
        event = sdk.aio_rpc.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.ong().contract_address)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(b58_recv_address, notify['States'][1])
        self.assertEqual(self.gas_price * self.gas_limit, notify['States'][3])
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.ont().contract_address)
        self.assertEqual('transfer', notify['States'][0])
        self.assertEqual(b58_from_address, notify['States'][1])
        self.assertEqual(b58_recv_address, notify['States'][2])
        self.assertEqual(amount, notify['States'][3])


if __name__ == '__main__':
    unittest.main()
