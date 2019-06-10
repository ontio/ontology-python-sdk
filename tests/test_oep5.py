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

from tests import sdk, not_panic_exception


class TestOep5(unittest.TestCase):
    def setUp(self):
        sdk.default_network = sdk.rpc
        self.networks = [sdk.rpc, sdk.restful]
        self.contract_address = '48a27da37954437481d915f636419b88e5bac50c'

    def test_set_contract_address(self):
        oep4 = sdk.neo_vm.oep5(self.contract_address)
        self.assertEqual(self.contract_address, oep4.hex_contract_address)

    @not_panic_exception
    def test_query_name(self):
        for network in self.networks:
            sdk.default_network = network
            oep5 = sdk.neo_vm.oep5(self.contract_address)
            self.assertEqual('CryptoKitties', oep5.name())

    @not_panic_exception
    def test_get_symbol(self):
        for network in self.networks:
            sdk.default_network = network
            oep5 = sdk.neo_vm.oep5(self.contract_address)
            self.assertEqual('CK', oep5.symbol())

    @not_panic_exception
    def test_balance_of(self):
        for network in self.networks:
            sdk.default_network = network
            oep5 = sdk.neo_vm.oep5(self.contract_address)
            self.assertGreaterEqual(oep5.balance_of('ANDfjwrUroaVtvBguDtrWKRMyxFwvVwnZD'), 0)
