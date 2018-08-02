#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import a2b_hex
from unittest import TestCase

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk

sdk = OntologySdk.get_instance()
rpc_address = "http://polaris3.ont.io:20336"
sdk.rpc.set_address(rpc_address)
private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
acc = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acc2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
acc3 = Account(a2b_hex(private_key3.encode()), SignatureScheme.SHA256withECDSA)
pubkeys = [acc.get_public_key(), acc2.get_public_key(), acc3.get_public_key()]
multi_addr = Address.address_from_multi_pubKeys(2, pubkeys)


class TestRpc(TestCase):
    def test_rpc_get_balance(self):
        address_balance = sdk.rpc.get_balance(acc.get_address_base58())
        try:
            address_balance['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            address_balance['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        multi_address_balance = sdk.rpc.get_balance(multi_addr.to_base58())
        try:
            multi_address_balance['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            multi_address_balance['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
