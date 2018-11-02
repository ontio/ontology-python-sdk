#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import json
import time
import unittest

from ontology.common.address import Address
from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme

remote_rpc_address = 'http://polaris3.ont.io:20336'
local_rpc_address = 'http://localhost:20336'


class TestOep4(unittest.TestCase):
    def test_get_abi(self):
        oep4_abi = '{"contractHash":"85848b5ec3b15617e396bdd62cb49575738dd413","abi":{"functions":[{"name":"Main","parameters":[{"name":"operation","type":""},{"name":"args","type":""}],"returntype":""},{"name":"init","parameters":[{"name":"","type":""}],"returntype":""},{"name":"name","parameters":[{"name":"","type":""}],"returntype":""},{"name":"symbol","parameters":[{"name":"","type":""}],"returntype":""},{"name":"decimals","parameters":[{"name":"","type":""}],"returntype":""},{"name":"totalSupply","parameters":[{"name":"","type":""}],"returntype":""},{"name":"balanceOf","parameters":[{"name":"account","type":""}],"returntype":""},{"name":"transfer","parameters":[{"name":"from_acct","type":""},{"name":"to_acct","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"transferMulti","parameters":[{"name":"args","type":""}],"returntype":""},{"name":"approve","parameters":[{"name":"owner","type":""},{"name":"spender","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"transferFrom","parameters":[{"name":"spender","type":""},{"name":"from_acct","type":""},{"name":"to_acct","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"allowance","parameters":[{"name":"owner","type":""},{"name":"spender","type":""}],"returntype":""}]}}'
        sdk = OntologySdk()
        self.assertEqual(json.loads(oep4_abi), sdk.neo_vm().oep4().get_abi())

    def test_set_contract_address(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '85848b5ec3b15617e396bdd62cb49575738dd413'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        self.assertEqual(contract_address, oep4.get_contract_address(is_hex=True))

    def test_get_name(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = 'd7b6a47966770c1545bf74c16426b26c0a238b16'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        self.assertEqual('DXToken', oep4.get_name())

    def test_get_symbol(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = 'd7b6a47966770c1545bf74c16426b26c0a238b16'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        self.assertEqual('DX', oep4.get_symbol())

    def test_get_decimal(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address1 = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address1)
        self.assertEqual(10, oep4.get_decimal())
        contract_address2 = '165b1227311d47c22cd073ef8f285d3bddc858ca'
        oep4.set_contract_address(contract_address2)
        self.assertEqual(32, oep4.get_decimal())
        contract_address3 = '8fecd2740b10a7410026774cc1f99fe14860873b'
        oep4.set_contract_address(contract_address3)
        self.assertEqual(255, oep4.get_decimal())

    def test_init(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.init(acct, acct, gas_limit, gas_price)
        self.assertEqual(len(tx_hash), 64)
        time.sleep(6)
        notify = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)['Notify'][0]
        self.assertEqual('Already initialized!', bytes.fromhex(notify['States']).decode())

    def test_get_total_supply(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        self.assertEqual(1000000000, oep4.get_total_supply())

    def test_transfer(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        from_acct = Account(private_key1, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        b58_to_address = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        value = 10
        tx_hash = oep4.transfer(from_acct, b58_to_address, value, from_acct, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))

    def test_balance_of(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        b58_address1 = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6'
        b58_address2 = 'AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve'
        balance = oep4.balance_of(b58_address1)
        self.assertGreaterEqual(balance, 10)
        balance = oep4.balance_of(b58_address2)
        self.assertGreaterEqual(balance, 1)

    def test_transfer_multi(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
        args = list()

        b58_from_address1 = acct1.get_address_base58()
        b58_from_address2 = acct2.get_address_base58()
        hex_from_address1 = acct1.get_address_hex()
        hex_from_address2 = acct2.get_address_hex()
        from_address_list = [hex_from_address1, hex_from_address2]

        b58_to_address1 = acct2.get_address_base58()
        b58_to_address2 = acct3.get_address_base58()
        hex_to_address1 = acct2.get_address_hex()
        hex_to_address2 = acct3.get_address_hex()
        to_address_list = [hex_to_address1, hex_to_address2]

        value_list = [1.1, 2.2]

        transfer1 = [b58_from_address1, b58_to_address1, value_list[0]]
        transfer2 = [b58_from_address2, b58_to_address2, value_list[1]]

        signers = [acct1, acct2, acct3]
        args.append(transfer1)
        args.append(transfer2)

        gas_limit = 20000000
        gas_price = 500

        tx_hash = oep4.transfer_multi(args, signers[0], signers, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        time.sleep(6)
        try:
            decimal = oep4.get_decimal()
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][:-1]
            self.assertEqual(len(args), len(notify))
            for index in range(len(notify)):
                self.assertEqual('transfer', bytes.fromhex(notify[index]['States'][0]).decode())
                self.assertEqual(from_address_list[index], notify[index]['States'][1])
                self.assertEqual(to_address_list[index], notify[index]['States'][2])
                array = bytearray(binascii.a2b_hex(notify[index]['States'][3].encode('ascii')))
                array.reverse()
                notify_value = int(binascii.b2a_hex(array).decode('ascii'), 16)
                self.assertEqual((10 ** decimal) * value_list[index], notify_value)
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_approve(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        owner_acct = Account(private_key1, SignatureScheme.SHA256withECDSA)
        hex_owner_address = owner_acct.get_address_hex()
        spender = Account(private_key2, SignatureScheme.SHA256withECDSA)
        b58_spender_address = spender.get_address_base58()
        hex_spender_address = spender.get_address_hex()
        amount = 100
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.approve(owner_acct, b58_spender_address, amount, owner_acct, gas_limit, gas_price)
        self.assertEqual(len(tx_hash), 64)
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        time.sleep(6)
        try:
            decimal = oep4.get_decimal()
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][0]
            states = notify['States']
            self.assertEqual('approval', bytes.fromhex(states[0]).decode())
            self.assertEqual(hex_owner_address, states[1])
            self.assertEqual(hex_spender_address, states[2])
            array = bytearray(binascii.a2b_hex(states[3].encode('ascii')))
            array.reverse()
            notify_value = int(binascii.b2a_hex(array).decode('ascii'), 16)
            self.assertEqual((10 ** decimal) * amount, notify_value)
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_allowance(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        b58_owner_address = acct1.get_address_base58()
        b58_spender_address = acct2.get_address_base58()
        allowance = oep4.allowance(b58_owner_address, b58_spender_address)
        self.assertGreaterEqual(allowance, 50)

    def test_transfer_from(self):
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        contract_address = '1ddbb682743e9d9e2b71ff419e97a9358c5c4ee9'
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
        private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
        spender_acct = Account(private_key2, SignatureScheme.SHA256withECDSA)

        from_acct = Account(private_key1, SignatureScheme.SHA256withECDSA)
        b58_from_address = from_acct.get_address_base58()
        hex_from_address = from_acct.get_address_hex()

        to_acct = Account(private_key3, SignatureScheme.SHA256withECDSA)
        b58_to_address = to_acct.get_address_base58()
        hex_to_address = to_acct.get_address_hex()

        gas_limit = 20000000
        gas_price = 500
        value = 1
        tx_hash = oep4.transfer_from(spender_acct, b58_from_address, b58_to_address, value, from_acct, gas_limit,
                                     gas_price)
        self.assertEqual(64, len(tx_hash))
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        time.sleep(6)
        try:
            decimal = oep4.get_decimal()
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][0]
            self.assertEqual(2, len(notify))
            self.assertEqual('transfer', bytes.fromhex(notify['States'][0]).decode())
            self.assertEqual(hex_from_address, notify['States'][1])
            self.assertEqual(hex_to_address, notify['States'][2])
            array = bytearray(binascii.a2b_hex(notify['States'][3].encode('ascii')))
            array.reverse()
            notify_value = int(binascii.b2a_hex(array).decode('ascii'), 16)
            self.assertEqual((10 ** decimal) * value, notify_value)
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)


if __name__ == '__main__':
    unittest.main()