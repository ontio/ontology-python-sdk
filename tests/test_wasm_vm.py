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

import unittest

from os import path

from ontology.common.address import Address
from ontology.vm.vm_type import VmType

from tests import sdk, acct2


class TestWasmVm(unittest.TestCase):
    def setUp(self):
        wasm_file_path = path.join(path.dirname(__file__), 'hello_world.wasm')
        self.name = 'hello_world'
        self.code_version = '1.0'
        self.author = 'NashMiao'
        self.code = sdk.wasm_vm.open_wasm(wasm_file_path)
        self.contract_address = Address.from_avm_code(self.code)

    def test_deploy_contract(self):
        tx = sdk.wasm_vm.make_deploy_transaction(self.code, self.name, self.code_version, self.author, 'email', 'desc',
                                                 500, 25000000, acct2.get_address_base58())
        tx.sign_transaction(acct2)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(1, result['State'])

    def test_get_contract(self):
        contract = sdk.rpc.get_contract(self.contract_address.hex())
        self.assertEqual(self.code, contract.get('Code'))
        self.assertEqual(self.name, contract.get('Name'))
        self.assertEqual(self.code_version, contract.get('CodeVersion'))
        self.assertEqual(self.author, contract.get('Author'))
        self.assertEqual(VmType.Wasm.value, contract.get('VmType'))
