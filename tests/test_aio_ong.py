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

import sys
import asyncio
import unittest

from Cryptodome.Random.random import randint

from ontology.sdk import Ontology
from ontology.utils.event import Event

from tests import sdk, acct1, acct2, acct3, acct4, not_panic_exception


class TestAioOng(unittest.TestCase):
    def test_get_contract_address(self):
        ong_address = '0200000000000000000000000000000000000000'
        self.assertEqual(ong_address, sdk.native_vm.aio_ong().contract_address.hex())

    @not_panic_exception
    @Ontology.runner
    async def test_query_name(self):
        token_name = await sdk.native_vm.aio_ong().name()
        self.assertEqual('ONG Token', token_name)

    @not_panic_exception
    @Ontology.runner
    async def test_query_symbol(self):
        token_symbol = await sdk.native_vm.aio_ong().symbol()
        self.assertEqual('ONG', token_symbol)

    @not_panic_exception
    @Ontology.runner
    async def test_query_decimals(self):
        decimals = await sdk.native_vm.aio_ong().decimals()
        self.assertEqual(9, decimals)

    @not_panic_exception
    @Ontology.runner
    async def test_unbound_ong(self):
        address_list = [acct1.get_address_base58(), acct2.get_address_base58(), acct3.get_address_base58(),
                        acct4.get_address_base58()]
        for address in address_list:
            unbound_ong = await sdk.native_vm.aio_ong().unbound(address)
            self.assertGreaterEqual(unbound_ong, 0)

    @not_panic_exception
    @Ontology.runner
    async def test_balance_of(self):
        address_list = [acct1.get_address_base58(), acct2.get_address_base58(), acct3.get_address_base58(),
                        acct4.get_address_base58()]
        for address in address_list:
            balance = await sdk.native_vm.aio_ong().balance_of(address)
            self.assertTrue(isinstance(balance, int))
            self.assertGreaterEqual(balance, 0)

    @not_panic_exception
    @Ontology.runner
    async def test_query_allowance(self):
        ong = sdk.native_vm.aio_ong()
        if sys.version_info >= (3, 7):
            task_list = [asyncio.create_task(ong.allowance(acct1.get_address_base58(), acct2.get_address_base58())),
                         asyncio.create_task(ong.allowance(acct2.get_address_base58(), acct3.get_address_base58())),
                         asyncio.create_task(ong.allowance(acct3.get_address_base58(), acct4.get_address_base58())),
                         asyncio.create_task(ong.allowance(acct4.get_address_base58(), acct1.get_address_base58()))]
        else:
            task_list = [ong.allowance(acct1.get_address_base58(), acct2.get_address_base58()),
                         ong.allowance(acct2.get_address_base58(), acct3.get_address_base58()),
                         ong.allowance(acct3.get_address_base58(), acct4.get_address_base58()),
                         ong.allowance(acct4.get_address_base58(), acct1.get_address_base58())]
        for task in task_list:
            self.assertGreaterEqual(await task, 0)

    @not_panic_exception
    @Ontology.runner
    async def test_transfer(self):
        amount, gas_price, gas_limit = 1, 500, 20000
        tx_hash = await sdk.native_vm.aio_ong().transfer(acct1, acct2.get_address(), amount, acct4, gas_price,
                                                         gas_limit)
        await asyncio.sleep(randint(14, 20))
        event = await sdk.aio_rpc.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.aio_ong().contract_address)
        self.assertEqual('transfer', notify[0]['States'][0])
        self.assertEqual(acct1.get_address_base58(), notify[0]['States'][1])
        self.assertEqual(acct2.get_address_base58(), notify[0]['States'][2])
        self.assertEqual(amount, notify[0]['States'][3])
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.aio_ong().contract_address)
        self.assertEqual('transfer', notify[1]['States'][0])
        self.assertEqual(acct4.get_address_base58(), notify[1]['States'][1])
        self.assertEqual(gas_price * gas_limit, notify[1]['States'][3])

    @not_panic_exception
    @Ontology.runner
    async def test_transfer_from_tx(self):
        acct2_b58_address = acct2.get_address_base58()
        tx_hash = await sdk.native_vm.aio_ong().transfer_from(acct2, acct1.get_address(), acct2_b58_address, 1,
                                                              acct2, 500, 20000)
        self.assertEqual(64, len(tx_hash))
        await asyncio.sleep(randint(14, 20))
        event = await sdk.aio_rpc.get_contract_event_by_tx_hash(tx_hash)
        notify_list = Event.get_notify_by_contract_address(event, sdk.native_vm.aio_ong().contract_address)
        self.assertEqual(2, len(notify_list))

    @not_panic_exception
    @Ontology.runner
    async def test_withdraw_ong(self):
        amount, gas_price, gas_limit = 1, 500, 20000
        tx_hash = await sdk.native_vm.aio_ong().withdraw(acct1, acct1.get_address(), amount, acct2, gas_price,
                                                         gas_limit)
        self.assertEqual(64, len(tx_hash))
        await asyncio.sleep(randint(14, 20))
        event = await sdk.aio_rpc.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.aio_ong().contract_address)
        self.assertEqual('transfer', notify[0]['States'][0])
        self.assertEqual(acct1.get_address_base58(), notify[0]['States'][2])
        self.assertEqual(amount, notify[0]['States'][3])
        notify = Event.get_notify_by_contract_address(event, sdk.native_vm.aio_ong().contract_address)
        self.assertEqual('transfer', notify[1]['States'][0])
        self.assertEqual(acct2.get_address_base58(), notify[1]['States'][1])
        self.assertEqual(gas_price * gas_limit, notify[1]['States'][3])

    @not_panic_exception
    @Ontology.runner
    async def test_approve(self):
        tx_hash = await sdk.native_vm.aio_ong().approve(acct1, acct2.get_address(), 10, acct2, 500, 20000)
        self.assertEqual(64, len(tx_hash))

    @not_panic_exception
    @Ontology.runner
    async def test_transfer_from(self):
        sdk.rpc.connect_to_test_net()
        b58_from_address = acct1.get_address_base58()
        b58_recv_address = acct2.get_address_base58()
        ong = sdk.native_vm.aio_ong()
        tx_hash = await ong.transfer_from(acct2, b58_from_address, b58_recv_address, 1, acct2, 500, 20000)
        self.assertEqual(64, len(tx_hash))
        await asyncio.sleep(randint(14, 20))
        event = await sdk.aio_rpc.get_contract_event_by_tx_hash(tx_hash)
        notify = Event.get_notify_by_contract_address(event, ong.contract_address)
        self.assertEqual(2, len(notify))


if __name__ == '__main__':
    unittest.main()
