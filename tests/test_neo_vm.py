#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from time import sleep

from ontology.utils.contract import Event, Data
from tests import sdk, acct1, acct2

from ontology.exception.exception import SDKException
from ontology.contract.neo.invoke_function import InvokeFunction


class TestNeoVm(unittest.TestCase):
    def test_big_int(self):
        num_dec = 135241956301000000
        bit_length = 57
        self.assertEqual(num_dec.bit_length(), bit_length)
        num_hex_str_little = '40cd0cbcd779e001'
        num_hex_str_big = '01e079d7bc0ccd40'
        self.assertEqual(num_hex_str_little, num_dec.to_bytes(8, 'little').hex())
        self.assertEqual(num_hex_str_big, num_dec.to_bytes(8, 'big').hex())

    def test_address_from_vm_code(self):
        avm_code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
                   '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
                   '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        contract_address = sdk.neo_vm.address_from_avm_code(avm_code)
        self.assertEqual('362cb5608b3eca61d4846591ebb49688900fedd0', contract_address.hex())

    def test_make_deploy_transaction(self):
        code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
               '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
               '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        tx = sdk.neo_vm.make_deploy_transaction(code, True, 'name', '1.0.0', 'author', 'email', 'description', 500,
                                                20000000, acct2.get_address_base58())
        tx.sign_transaction(acct2)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(1, result['State'])

    def test_invoke_transaction(self):
        """
        from ontology.interop.System.Runtime import Notify

        def main(operation, args):
            if operation == 'hello':
                return hello(args[0])
            return False


        def hello(msg):
            Notify(["hello", msg])
            return msg
        """
        avm_code = '51c56b6c58c56b6a00527ac46a51527ac46a52527ac46a51c30568656c6c6f7d9c7c756427' \
                   '00006a53527ac46a52c300c3516a53c3936a53527ac46a53c36a00c365f2006c7566620300' \
                   '006c75660111c56b6a00527ac46a51527ac46a51c300947600a0640c00c16a52527ac4620e' \
                   '007562030000c56a52527ac46a52c3c0517d9c7c75641c00006a53527ac46a52c300c36a54' \
                   '527ac4516a55527ac4625c006a52c3c0527d9c7c756421006a52c300c36a53527ac46a52c3' \
                   '51c36a54527ac4516a55527ac4616232006a52c3c0537d9c7c756424006a52c300c36a5352' \
                   '7ac46a52c351c36a54527ac46a52c352c36a55527ac462050000f100c176c96a56527ac46a' \
                   '53c36a57527ac46a57c36a54c37d9f7c756419006a56c36a57c3c86a57c36a55c3936a5752' \
                   '7ac462e0ff6a56c36c756656c56b6a00527ac46a51527ac46a52527ac46203000568656c6c' \
                   '6f6a52c352c176c9681553797374656d2e52756e74696d652e4e6f746966796a52c36c7566'
        contract_address = sdk.neo_vm.address_from_avm_code(avm_code).hex()
        self.assertEqual('f7b9970fd6def5229c1f30ad15372bd1c20bb260', contract_address)
        hello = InvokeFunction('hello')
        hello.set_params_value('ontology')
        tx = sdk.neo_vm.make_invoke_transaction(contract_address, hello, acct1.get_address_base58(), 500, 20000)
        response = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(1, response['State'])
        response['Result'] = Data.to_utf8_str(response['Result'])
        self.assertEqual('ontology', response['Result'])
        tx.sign_transaction(acct1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        sleep(10)
        for _ in range(5):
            try:
                event = sdk.rpc.get_contract_event_by_tx_hash(tx_hash)
                if isinstance(event, dict) and event.get('Notify', '') != '':
                    notify = Event.get_notify_by_contract_address(event, contract_address)
                    self.assertEqual(contract_address, notify['ContractAddress'])
                    self.assertEqual('hello', Data.to_utf8_str(notify['States'][0]))
                    self.assertEqual('ontology', Data.to_utf8_str(notify['States'][1]))
                    break
            except SDKException:
                continue
            sleep(2)


if __name__ == '__main__':
    unittest.main()
