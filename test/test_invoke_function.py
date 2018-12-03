#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import time
import unittest

from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction
from ontology.utils.contract_data_parser import ContractDataParser
from ontology.utils.contract_event_parser import ContractEventParser
from ontology.utils.utils import deserialize_stack_item, deserialize_hex

sdk = OntologySdk()
remote_rpc_address = 'http://polaris3.ont.io:20336'
local_rpc_address = 'http://localhost:20336'
sdk.rpc.set_address(remote_rpc_address)
gas_limit = 20000000
gas_price = 500

private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'

acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)


class TestWalletManager(unittest.TestCase):
    def test_oep4_name(self):
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        bytearray_contract_address = bytearray(binascii.a2b_hex(contract_address))
        bytearray_contract_address.reverse()
        func = InvokeFunction('name')
        name = sdk.neo_vm().send_transaction(bytearray_contract_address, None, None, 0, 0, func, True)
        name = ContractDataParser.to_utf8_str(name)
        self.assertEqual('DXToken', name)

    def test_oep4_symbol(self):
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        func = InvokeFunction('symbol')
        symbol = sdk.neo_vm().send_transaction(hex_contract_address, None, None, 0, 0, func, True)
        symbol = ContractDataParser.to_utf8_str(symbol)
        self.assertEqual('DX', symbol)

    def test_oep4_decimal(self):
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        func = InvokeFunction('decimals')
        decimals = sdk.neo_vm().send_transaction(hex_contract_address, None, None, 0, 0, func, True)
        decimals = ContractDataParser.to_int(decimals)
        self.assertEqual(10, decimals)

    def test_oep4_total_supply(self):
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        func = InvokeFunction('totalSupply')
        total_supply = sdk.neo_vm().send_transaction(hex_contract_address, None, None, 0, 0, func, True)
        total_supply = ContractDataParser.to_int(total_supply)
        self.assertEqual(10000000000000000000, total_supply)

    def test_oep4_balance_of(self):
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        func = InvokeFunction('balanceOf')
        bytes_address = acct1.get_address().to_bytes()
        func.set_params_value(bytes_address)
        balance = sdk.neo_vm().send_transaction(hex_contract_address, None, None, 0, 0, func, True)
        balance = ContractDataParser.to_int(balance)
        self.assertGreater(balance, 100)

    def test_oep4_transfer(self):
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        func = InvokeFunction('transfer')
        bytes_from_address = acct1.get_address().to_bytes()
        bytes_to_address = acct2.get_address().to_bytes()
        value = 1
        func.set_params_value(bytes_from_address, bytes_to_address, value)
        tx_hash = sdk.neo_vm().send_transaction(hex_contract_address, acct1, acct2, gas_limit, gas_price, func, False)
        time.sleep(6)
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        states_list = ContractEventParser.get_states_by_contract_address(event, hex_contract_address)
        states = states_list[0]
        states[0] = ContractDataParser.to_utf8_str(states[0])
        self.assertEqual('transfer', states[0])
        states[1] = ContractDataParser.to_b58_address(states[1])
        self.assertEqual(acct1.get_address().b58encode(), states[1])
        states[2] = ContractDataParser.to_b58_address(states[2])
        self.assertEqual(acct2.get_address().b58encode(), states[2])
        states[3] = ContractDataParser.to_int(states[3])
        self.assertEqual(value, states[3])

    def test_oep4_transfer_multi(self):
        hex_contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        bytes_from_address1 = acct1.get_address().to_bytes()
        bytes_to_address1 = acct2.get_address().to_bytes()
        value1 = 2
        transfer1 = [bytes_from_address1, bytes_to_address1, value1]
        bytes_from_address2 = acct2.get_address().to_bytes()
        bytes_to_address2 = acct3.get_address().to_bytes()
        value2 = 1
        transfer2 = [bytes_from_address2, bytes_to_address2, value2]
        func = InvokeFunction('transferMulti')
        func.set_params_value(transfer1, transfer2)
        tx_hash = sdk.neo_vm().send_transaction(hex_contract_address, acct1, acct2, gas_limit, gas_price, func, False)
        time.sleep(6)
        event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        states_list = ContractEventParser.get_states_by_contract_address(event, hex_contract_address)
        states_list[0][0] = ContractDataParser.to_utf8_str(states_list[0][0])
        self.assertEqual('transfer', states_list[0][0])
        states_list[0][1] = ContractDataParser.to_b58_address(states_list[0][1])
        self.assertEqual(acct1.get_address().b58encode(), states_list[0][1])
        states_list[0][2] = ContractDataParser.to_b58_address(states_list[0][2])
        self.assertEqual(acct2.get_address().b58encode(), states_list[0][2])
        states_list[0][3] = ContractDataParser.to_int(states_list[0][3])
        self.assertEqual(value1, states_list[0][3])

        states_list[1][0] = ContractDataParser.to_utf8_str(states_list[1][0])
        self.assertEqual('transfer', states_list[1][0])
        states_list[1][1] = ContractDataParser.to_b58_address(states_list[1][1])
        self.assertEqual(acct2.get_address().b58encode(), states_list[1][1])
        states_list[1][2] = ContractDataParser.to_b58_address(states_list[1][2])
        self.assertEqual(acct3.get_address().b58encode(), states_list[1][2])
        states_list[1][3] = ContractDataParser.to_int(states_list[1][3])
        self.assertEqual(value2, states_list[1][3])

if __name__ == '__main__':
    unittest.main()
