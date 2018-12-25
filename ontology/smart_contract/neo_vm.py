#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import time

from ontology.common.address import Address
from ontology.common.define import ZERO_ADDRESS
from ontology.smart_contract.neo_contract.oep4 import Oep4
from ontology.core.deploy_transaction import DeployTransaction
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.smart_contract.neo_contract.claim_record import ClaimRecord


class NeoVm(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def oep4(self):
        return Oep4(self.__sdk)

    def claim_record(self):
        return ClaimRecord(self.__sdk)

    @staticmethod
    def avm_code_to_hex_contract_address(avm_code: str):
        hex_contract_address = Address.address_from_vm_code(avm_code).to_reverse_hex_str()
        return hex_contract_address

    @staticmethod
    def avm_code_to_bytes_contract_address(avm_code: str):
        bytes_contract_address = Address.address_from_vm_code(avm_code).to_bytes()
        return bytes_contract_address

    @staticmethod
    def avm_code_to_bytearray_contract_address(avm_code: str):
        bytearray_contract_address = Address.address_from_vm_code(avm_code).to_bytearray()
        return bytearray_contract_address

    @staticmethod
    def make_deploy_transaction(code_str: str, need_storage: bool, name: str, code_version: str, author: str,
                                email: str, desp: str, payer: str, gas_limit: int, gas_price: int):
        unix_time_now = int(time())
        deploy_tx = DeployTransaction()
        deploy_tx.payer = Address.b58decode(payer).to_bytes()
        deploy_tx.attributes = bytearray()
        deploy_tx.nonce = unix_time_now
        deploy_tx.code = bytearray.fromhex(code_str)
        deploy_tx.code_version = code_version
        deploy_tx.version = 0
        deploy_tx.need_storage = need_storage
        deploy_tx.name = name
        deploy_tx.author = author
        deploy_tx.email = email
        deploy_tx.gas_limit = gas_limit
        deploy_tx.gas_price = gas_price
        deploy_tx.description = desp
        return deploy_tx

    @staticmethod
    def make_invoke_transaction(code_address: bytearray, params: bytearray, payer: bytes, gas_limit: int,
                                gas_price: int):
        params += bytearray([0x67])
        params += code_address
        invoke_tx = InvokeTransaction()
        invoke_tx.version = 0
        invoke_tx.sigs = bytearray()
        invoke_tx.attributes = bytearray()
        unix_time_now = int(time())
        invoke_tx.nonce = unix_time_now
        invoke_tx.code = params
        invoke_tx.gas_limit = gas_limit
        invoke_tx.gas_price = gas_price
        if isinstance(payer, bytes) and payer != b'':
            invoke_tx.payer = payer
        else:
            invoke_tx.payer = Address(ZERO_ADDRESS).to_bytes()
        return invoke_tx
