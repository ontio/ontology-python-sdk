#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import json
import os
import time
import unittest

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.exception.exception import SDKException
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.oep4 import Oep4
from ontology.wallet.wallet_manager import WalletManager

remote_rpc_address = "http://polaris3.ont.io:20336"
local_rpc_address = 'http://localhost:20336'


class TestOep4(unittest.TestCase):
    def test_set_abi(self):
        oep4_abi = '{"hash":"0x678259ca02f319d43095ceb243697e36c111e8ab","entrypoint":"Main","functions":[{"name":"Name","parameters":[],"returntype":"String"},{"name":"Symbol","parameters":[],"returntype":"String"},{"name":"Decimal","parameters":[],"returntype":"Integer"},{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args","type":"Array"}],"returntype":"Any"},{"name":"Init","parameters":[],"returntype":"Boolean"},{"name":"Transfer","parameters":[{"name":"from","type":"ByteArray"},{"name":"to","type":"ByteArray"},{"name":"value","type":"Integer"}],"returntype":"Boolean"},{"name":"TransferMulti","parameters":[{"name":"args","type":"Array"}],"returntype":"Boolean"},{"name":"BalanceOf","parameters":[{"name":"address","type":"ByteArray"}],"returntype":"Integer"},{"name":"TotalSupply","parameters":[],"returntype":"Integer"},{"name":"Approve","parameters":[{"name":"owner","type":"ByteArray"},{"name":"spender","type":"ByteArray"},{"name":"amount","type":"Integer"}],"returntype":"Boolean"},{"name":"TransferFrom","parameters":[{"name":"spender","type":"ByteArray"},{"name":"from","type":"ByteArray"},{"name":"to","type":"ByteArray"},{"name":"amount","type":"Integer"}],"returntype":"Boolean"},{"name":"Allowance","parameters":[{"name":"owner","type":"ByteArray"},{"name":"spender","type":"ByteArray"}],"returntype":"Integer"}],"events":[{"name":"transfer","parameters":[{"name":"from","type":"ByteArray"},{"name":"to","type":"ByteArray"},{"name":"value","type":"Integer"}],"returntype":"Void"},{"name":"approval","parameters":[{"name":"onwer","type":"ByteArray"},{"name":"spender","type":"ByteArray"},{"name":"value","type":"Integer"}],"returntype":"Void"}]}'
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep_4 = Oep4()
        oep_4.read_abi(path)
        self.assertEqual(json.loads(oep4_abi), oep_4.get_abi())
        oep_4.set_abi(oep4_abi)
        self.assertEqual(json.loads(oep4_abi), oep_4.get_abi())

    # def test_deploy_remote(self):
    #     private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
    #     acct = Account(private_key, SignatureScheme.SHA256withECDSA)
    #     sdk = OntologySdk()
    #     sdk.rpc.set_address(remote_rpc_address)
    #     print('private key:')
    #     print(binascii.b2a_hex(acct.serialize_private_key()).decode('utf-8'))
    #     print('b58_address:')
    #     b58_acct = acct.get_address_base58()
    #     print(b58_acct)
    #     print('balance: ')
    #     print(sdk.rpc.get_balance(b58_acct))
    #     with open('oep4.avm', 'r') as f:
    #         code = f.read()
    #         gas_limit = 21000000
    #         gas_price = 500
    #         tx = sdk.neo_vm().make_deploy_transaction(code, True, 'XIN', 'v1.0', 'DINGXIN', 'xin@mail.com',
    #                                                   'test oep4 token', b58_acct, gas_limit, gas_price)
    #         sdk.sign_transaction(tx, acct)
    #         res = sdk.rpc.send_raw_transaction(tx)
    #         print(res)
    #
    # def test_deploy_local(self):
    #     wm = WalletManager()
    #     path = os.path.join(os.getcwd(), 'oep4_wallet.dat')
    #     wm.open_wallet(path)
    #     password = '1'
    #     acct = wm.get_account(address='AevnsY2aGCdi61CLLFZoXMYuTeaYMC4DT1', pwd=password)
    #     sdk = OntologySdk()
    #     sdk.rpc.set_address(local_rpc_address)
    #     print('private key:')
    #     print(binascii.b2a_hex(acct.serialize_private_key()).decode('utf-8'))
    #     print('b58_address:')
    #     b58_acct = acct.get_address_base58()
    #     print(b58_acct)
    #     print('balance: ')
    #     print(sdk.rpc.get_balance(b58_acct))
    #     with open('oep4.avm', 'r') as f:
    #         code = f.read()
    #         gas_limit = 21000000
    #         gas_price = 0
    #         tx = sdk.neo_vm().make_deploy_transaction(code, True, 'XIN', 'v1.0', 'DINGXIN', 'xin@mail.com',
    #                                                   'test oep4 token', b58_acct, gas_limit, gas_price)
    #         sdk.sign_transaction(tx, acct)
    #         res = sdk.rpc.send_raw_transaction(tx)
    #         print(res)

    def test_get_name(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        self.assertEqual('DXToken', oep4.get_name())

    def test_get_symbol(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        self.assertEqual('DX', oep4.get_symbol())

    def test_get_decimal(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        self.assertEqual(8, oep4.get_decimal())

    def test_init(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.init(acct, acct, gas_limit, gas_price)
        self.assertEqual(len(tx_hash), 64)

    def test_get_total_supply(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        self.assertEqual(10000000000000, oep4.get_total_supply())

    def test_transfer(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        private_key1 = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        from_address = acct1.get_address_hex()
        to_address = acct2.get_address_hex()
        value = 10
        result = oep4.transfer(acct1, acct1, gas_limit, gas_price, from_address, to_address, value)
        self.assertEqual(len(result), 64)

    def test_balance_of(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        hex_address1 = acct1.get_address_hex()
        hex_address2 = acct2.get_address_hex()
        balance = oep4.balance_of(hex_address1)
        self.assertGreaterEqual(balance, 10)
        balance = oep4.balance_of(hex_address2)
        self.assertGreaterEqual(balance, 10)

    def test_transfer_multi(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
        args = list()

        from_address_list = list()
        array_from_address1 = acct1.get_address().to_array()
        array_from_address2 = acct2.get_address().to_array()
        hex_from_address1 = acct1.get_address_hex()
        hex_from_address2 = acct2.get_address_hex()
        from_address_list.append(hex_from_address1)
        from_address_list.append(hex_from_address2)

        to_address_list = list()
        array_to_address1 = acct2.get_address().to_array()
        array_to_address2 = acct3.get_address().to_array()
        hex_to_address1 = acct2.get_address_hex()
        hex_to_address2 = acct3.get_address_hex()
        to_address_list.append(hex_to_address1)
        to_address_list.append(hex_to_address2)

        value_list = [1, 2]

        transfer1 = [array_from_address1, array_to_address1, value_list[0]]
        transfer2 = [array_from_address2, array_to_address2, value_list[1]]
        payer_accounts = [acct1, acct2, acct3]
        args.append(transfer1)
        args.append(transfer2)

        gas_limit = 20000000
        gas_price = 500

        tx_hash = oep4.transfer_multi(payer_accounts, gas_limit, gas_price, args)
        self.assertEqual(64, len(tx_hash))
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        time.sleep(6)
        try:
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][:-1]
            self.assertEqual(len(args), len(notify))
            for index in range(len(notify)):
                self.assertEqual(from_address_list[index], notify[index]['States'][0])
                self.assertEqual(to_address_list[index], notify[index]['States'][1])
                self.assertEqual(value_list[index], int(notify[index]['States'][2]))
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_approve(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        hex_owner_address = acct1.get_address_hex()
        hex_spender_address = acct2.get_address_hex()
        amount = 100
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.approve(acct1, acct1, gas_limit, gas_price, hex_owner_address, hex_spender_address, amount)
        self.assertEqual(len(tx_hash), 64)
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        time.sleep(6)
        try:
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][0]
            self.assertEqual(hex_owner_address, notify['States'][0])
            self.assertEqual(hex_spender_address, notify['States'][1])
            self.assertEqual('64', notify['States'][2])
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_allowance(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        hex_owner_address = acct1.get_address_hex()
        hex_spender_address = acct2.get_address_hex()
        allowance = oep4.allowance(hex_owner_address, hex_spender_address)
        self.assertGreaterEqual(allowance, 0)

    def test_transfer_from(self):
        oep4 = Oep4(network=remote_rpc_address)
        path = os.path.join(os.getcwd(), 'oep4.avm')
        oep4.read_code(path)
        path = os.path.join(os.getcwd(), 'oep4.json')
        oep4.read_abi(path)
        private_key1 = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
        private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
        private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        spender_address = acct2.get_address_hex()
        from_address = acct1.get_address_hex()
        to_address = acct3.get_address_hex()
        value = 1
        tx_hash = oep4.transfer_from(acct2, acct1, gas_limit, gas_price, spender_address, from_address, to_address,
                                     value)
        self.assertEqual(64, len(tx_hash))
        sdk = OntologySdk()
        sdk.set_rpc(remote_rpc_address)
        time.sleep(6)
        try:
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][0]
            self.assertEqual(from_address, notify['States'][0])
            self.assertEqual(to_address, notify['States'][1])
            self.assertEqual('01', notify['States'][2])
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)


if __name__ == '__main__':
    unittest.main()
