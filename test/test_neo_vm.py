#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from time import sleep

from test import acct1, acct2, acct3, acct4

from ontology.ont_sdk import OntologySdk
from ontology.utils.contract_data_parser import ContractDataParser
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction

sdk = OntologySdk()
sdk.rpc.connect_to_test_net()


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
        acct_balance = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        acct_balance_2 = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance_2['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance_2['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        acct_balance_3 = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance_3['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance_3['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        acct_balance_4 = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance_4['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance_4['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

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
        hex_contract_address = sdk.neo_vm.avm_code_to_hex_contract_address(avm_code)
        self.assertEqual('362cb5608b3eca61d4846591ebb49688900fedd0', hex_contract_address)

    def test_make_deploy_transaction(self):
        code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
               '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
               '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        payer = acct2
        b58_payer = payer.get_address_base58()
        gas_limit = 20000000
        gas_price = 500
        tx = sdk.neo_vm.make_deploy_transaction(code, True, 'name', 'v1.0', 'author', 'email', 'desp', b58_payer,
                                                gas_limit, gas_price)
        tx.sign_transaction(payer)
        result = sdk.rpc.send_raw_transaction_pre_exec(tx)
        self.assertEqual(1, result['State'])

    def test_invoke_transaction(self):
        avm_code = '58c56b6a00527ac46a51527ac46a00c30548656c6c6f9c6416006a51c300c36a52527ac46a52c3650b006c756' \
                   '661006c756655c56b6a00527ac46a00c3681553797374656d2e52756e74696d652e4e6f7469667961516c7566'
        hex_contract_address = sdk.neo_vm.avm_code_to_hex_contract_address(avm_code)
        self.assertEqual('39f3fb644842c808828817bd73da0946d99f237f', hex_contract_address)
        hello = InvokeFunction('Hello')
        hello.set_params_value('Ontology')
        response = sdk.rpc.send_neo_vm_transaction(hex_contract_address, None, None, 0, 0, hello, True)
        self.assertEqual(1, response['State'])
        result = response['Result']
        result = ContractDataParser.to_bool(result)
        self.assertEqual(True, result)
        gas_limit = 20000
        gas_price = 500
        tx_hash = sdk.rpc.send_neo_vm_transaction(hex_contract_address, None, acct1, gas_limit, gas_price, hello, False)
        sleep(6)
        response = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        notify = response['Notify'][0]
        self.assertEqual(hex_contract_address, notify['ContractAddress'])
        notify['States'] = ContractDataParser.to_utf8_str(notify['States'])
        self.assertEqual('Ontology', notify['States'])


if __name__ == '__main__':
    unittest.main()
