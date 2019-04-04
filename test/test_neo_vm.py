#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from time import sleep

from ontology.common.address import Address
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.exception.exception import SDKException
from ontology.utils.contract_event import ContractEventParser
from test import sdk, acct1, acct2, acct4, acct3

from ontology.utils.contract_data import ContractDataParser
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class TestNeoVm(unittest.TestCase):
    def test_big_int(self):
        num_dec = 135241956301000000
        bit_length = 57
        self.assertEqual(num_dec.bit_length(), bit_length)
        num_hex_str_little = '40cd0cbcd779e001'
        num_hex_str_big = '01e079d7bc0ccd40'
        self.assertEqual(num_hex_str_little, num_dec.to_bytes(8, 'little').hex())
        self.assertEqual(num_hex_str_big, num_dec.to_bytes(8, 'big').hex())

    def test_get_balance(self):
        pub_keys = [acct1.get_public_key_bytes(), acct2.get_public_key_bytes(), acct3.get_public_key_bytes()]
        multi_address = Address.address_from_multi_pub_keys(2, pub_keys)
        address_list = [acct1.get_address_base58(), acct2.get_address_base58(), acct3.get_address_base58(),
                        acct4.get_address_base58(), multi_address.b58encode()]
        for address in address_list:
            balance = sdk.restful.get_balance(address)
            self.assertTrue(isinstance(balance, dict))
            self.assertGreaterEqual(balance['ONT'], 0)
            self.assertGreaterEqual(balance['ONG'], 0)

    def test_unbound_ong(self):
        acct1_unbound_ong = sdk.native_vm.asset().query_unbound_ong(acct1.get_address_base58())
        self.assertGreaterEqual(int(acct1_unbound_ong), 0)
        acct2_unbound_ong = sdk.native_vm.asset().query_unbound_ong(acct4.get_address_base58())
        self.assertGreaterEqual(int(acct2_unbound_ong), 0)
        acct3_unbound_ong = sdk.native_vm.asset().query_unbound_ong(acct4.get_address_base58())
        self.assertGreaterEqual(int(acct3_unbound_ong), 0)
        acct4_unbound_ong = sdk.native_vm.asset().query_unbound_ong(acct4.get_address_base58())
        self.assertGreaterEqual(int(acct4_unbound_ong), 0)

    def test_address_from_vm_code(self):
        avm_code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
                   '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
                   '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        contract_address = sdk.neo_vm.avm_code_to_hex_contract_address(avm_code)
        bytes_contract_address = sdk.neo_vm.avm_code_to_bytes_contract_address(avm_code)
        bytearray_contract_address = sdk.neo_vm.avm_code_to_bytearray_contract_address(avm_code)
        self.assertEqual('362cb5608b3eca61d4846591ebb49688900fedd0', contract_address)
        self.assertEqual(contract_address, bytes_contract_address.hex())
        self.assertEqual(contract_address, bytearray_contract_address.hex())

    def test_make_deploy_transaction(self):
        code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
               '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
               '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        tx = sdk.neo_vm.make_deploy_transaction(code, True, 'name', 'v1.0', 'author', 'email', 'desperation', 500,
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
        contract_address = sdk.neo_vm.avm_code_to_hex_contract_address(avm_code)
        self.assertEqual('f7b9970fd6def5229c1f30ad15372bd1c20bb260', contract_address)
        hello = InvokeFunction('hello')
        hello.set_params_value('ontology')
        tx = sdk.neo_vm.make_invoke_transaction(contract_address, hello, acct1.get_address_base58(), 500, 20000)
        response = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(1, response['State'])
        response['Result'] = ContractDataParser.to_utf8_str(response['Result'])
        self.assertEqual('ontology', response['Result'])
        tx.sign_transaction(acct1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        sleep(7)
        for _ in range(5):
            try:
                response = sdk.rpc.get_contract_event_by_tx_hash(tx_hash)
                if isinstance(response, dict) and response['Notify']:
                    break
            except SDKException:
                continue
            sleep(2)
        notify = ContractEventParser.get_event_from_event_list_by_contract_address(response['Notify'], contract_address)
        self.assertEqual(contract_address, notify[0]['ContractAddress'])
        self.assertEqual('hello', ContractDataParser.to_utf8_str(notify[0]['States'][0]))
        self.assertEqual('ontology', ContractDataParser.to_utf8_str(notify[0]['States'][1]))


if __name__ == '__main__':
    unittest.main()
