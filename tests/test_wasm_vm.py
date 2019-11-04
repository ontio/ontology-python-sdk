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
from time import sleep

from ontology.vm.vm_type import VmType
from ontology.common.address import Address
from ontology.utils.wasm import WasmData
from ontology.contract.wasm.invoke_function import WasmInvokeFunction

from tests import sdk, acct1, acct2, acct3, acct4


class TestWasmVm(unittest.TestCase):
    def setUp(self):
        self.wasm_file_list = ['api.wasm', 'basic_test_case.wasm', 'hello_world.wasm', 'oep4.wasm', 'oep5.wasm',
                               'oep8.wasm']
        self.wasm_contract_address = ['6a293ecd91853111d7a63948cc254389028b356a',
                                      'bf8ee176c360f7a77b9c45b6faab213bc50eaf5d',
                                      '259eed30d30d7c473944760023fcc321b8966371',
                                      'c3304fc12dbc38aa5c8e308b9236552523ffae0f',
                                      '3b58a5270aaadd18320d374241dbb3db3e5c59b9',
                                      '8ecf3b91f891599b591e1cc1d49018eef3180abf']
        self.name = 'hello_world'
        self.code_version = '1.0'
        self.author = 'NashMiao'
        self.email = 'wdx7266@vip.qq.com'
        self.desc = 'wasm contract for python sdk test'
        self.gas_price = 500
        self.gas_limit = 25000000
        self.oep4_contract_address = 'c3304fc12dbc38aa5c8e308b9236552523ffae0f'
        self.basic_test_case_contract_address = 'bf8ee176c360f7a77b9c45b6faab213bc50eaf5d'

    @staticmethod
    def get_wasm_file_path(file_name):
        return path.join(path.dirname(__file__), 'wasm', file_name)

    def get_contract_code(self, file_name) -> str:
        wasm_file_path = self.get_wasm_file_path(file_name)
        return sdk.wasm_vm.open_wasm(wasm_file_path)

    def test_address_from_avm_code(self):
        for index, file in enumerate(self.wasm_file_list):
            code = self.get_contract_code(file)
            contract_address = sdk.wasm_vm.address_from_wasm_code(code)
            self.assertEqual(self.wasm_contract_address[index], contract_address.hex())

    def test_deploy_contract(self):
        for index, file in enumerate(self.wasm_file_list):
            code = self.get_contract_code(file)
            tx = sdk.wasm_vm.make_deploy_transaction(code, self.name, self.code_version, self.author, self.email,
                                                     self.desc, self.gas_price, self.gas_limit,
                                                     acct2.get_address_base58())
            tx.sign_transaction(acct2)
            sdk.rpc.connect_to_test_net()
            result = sdk.rpc.send_raw_transaction_pre_exec(tx)
            self.assertEqual(1, result['State'])

    def test_get_contract(self):
        contract = sdk.rpc.get_contract(self.basic_test_case_contract_address)
        self.assertEqual(self.name, contract.get('Name'))
        self.assertEqual(self.code_version, contract.get('CodeVersion'))
        self.assertEqual(self.author, contract.get('Author'))
        self.assertEqual(VmType.Wasm.value, contract.get('VmType'))

    def test_invoke_add_transaction(self):
        func = WasmInvokeFunction('add')
        func.set_params_value(-2, 3)
        tx = sdk.wasm_vm.make_invoke_transaction(self.basic_test_case_contract_address, func, acct3.get_address(),
                                                 self.gas_price, self.gas_limit)
        tx.sign_transaction(acct3)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx).get('Result', '')
        self.assertEqual('01000000000000000000000000000000', result)
        self.assertEqual(1, WasmData.to_int(result))
        func = WasmInvokeFunction('add')
        func.set_params_value(1, 2)
        tx = sdk.wasm_vm.make_invoke_transaction(self.basic_test_case_contract_address, func, acct3.get_address(),
                                                 self.gas_price, self.gas_limit)
        target_payload = '5daf0ec53b21abfab6459c7ba7f760c376e18ebf24036164640100000' \
                         '000000000000000000000000002000000000000000000000000000000'
        self.assertEqual(target_payload, tx.payload.hex())
        tx.sign_transaction(acct3)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx).get('Result', '')
        self.assertEqual('03000000000000000000000000000000', result)
        self.assertEqual(3, WasmData.to_int(result))
        func.set_params_value(2 ** 127 - 1, -2 ** 127)
        tx = sdk.wasm_vm.make_invoke_transaction(self.basic_test_case_contract_address, func, acct2.get_address(),
                                                 self.gas_price, self.gas_limit)
        target_payload = '5daf0ec53b21abfab6459c7ba7f760c376e18ebf2403616464fffffff' \
                         'fffffffffffffffffffffff7f00000000000000000000000000000080'
        self.assertEqual(target_payload, tx.payload.hex())
        tx.sign_transaction(acct2)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx).get('Result')
        self.assertEqual('ffffffffffffffffffffffffffffffff', result)
        self.assertEqual(-1, WasmData.to_int(result))

    def test_invoke_notify_transaction(self):
        func = WasmInvokeFunction('notify')
        tx = sdk.wasm_vm.make_invoke_transaction(self.basic_test_case_contract_address, func, acct3.get_address(),
                                                 self.gas_price, self.gas_limit)
        target_payload = '5daf0ec53b21abfab6459c7ba7f760c376e18ebf07066e6f74696679'
        self.assertEqual(target_payload, tx.payload.hex())
        tx.sign_transaction(acct3)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        notify = result.get('Notify')[0]
        self.assertEqual(self.basic_test_case_contract_address, notify.get('ContractAddress'))
        self.assertEqual('hello', notify.get('States')[0])

    def test_read_storage(self):
        func = WasmInvokeFunction('storage_read')
        func.set_params_value('key')
        tx = sdk.wasm_vm.make_invoke_transaction(self.basic_test_case_contract_address, func, acct3.get_address(),
                                                 self.gas_price, self.gas_limit)
        target_payload = '5daf0ec53b21abfab6459c7ba7f760c376e18ebf110c73746f726167655f72656164036b6579'
        self.assertEqual(target_payload, tx.payload.hex())
        tx.sign_transaction(acct3)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertTrue(isinstance(result, dict))
        result = result.get('Result', '')
        self.assertTrue(isinstance(result, str))

    def test_write_storage_transaction(self):
        func = WasmInvokeFunction('storage_write')
        func.set_params_value('key', 'value')
        tx = sdk.wasm_vm.make_invoke_transaction(self.basic_test_case_contract_address, func, acct1.get_address(),
                                                 self.gas_price, self.gas_limit)
        target_payload = '5daf0ec53b21abfab6459c7ba7f760c376e18ebf180d73746f726167655f7772697465036b65790576616c7565'
        self.assertEqual(target_payload, tx.payload.hex())
        tx.sign_transaction(acct1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))

    def test_balance_of_transaction(self):
        func = WasmInvokeFunction('balanceOf')
        func.set_params_value(Address.b58decode('ANDfjwrUroaVtvBguDtrWKRMyxFwvVwnZD'))
        tx = sdk.wasm_vm.make_invoke_transaction(self.oep4_contract_address, func, acct4.get_address(), self.gas_price,
                                                 self.gas_limit)
        target_payload = '0faeff23255536928b308e5caa38bc2dc14f30c31e0962616c6' \
                         '16e63654f6646b1a18af6b7c9f8a4602f9f73eeb3030f0c29b7'
        self.assertEqual(target_payload, tx.payload.hex())
        tx.sign_transaction(acct4)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(100_000_000_000, WasmData.to_int(result.get('Result')))

    def test_total_supply_tx(self):
        func = WasmInvokeFunction('totalSupply')
        tx = sdk.wasm_vm.make_invoke_transaction(self.oep4_contract_address, func, acct1.get_address(), self.gas_price,
                                                 self.gas_limit)
        payload = '0faeff23255536928b308e5caa38bc2dc14f30c30c0b746f74616c537570706c79'
        self.assertEqual(payload, tx.payload.hex())
        tx.sign_transaction(acct1)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(100_000_000_000, WasmData.to_int(result.get('Result')))
