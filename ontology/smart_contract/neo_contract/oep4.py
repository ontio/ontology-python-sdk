#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import binascii

from ontology.account.account import Account
from ontology.common.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams


class Oep4(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__contract_address = bytearray()
        self.__oep4_abi = {"hash": "0x678259ca02f319d43095ceb243697e36c111e8ab", "entrypoint": "Main",
                           "functions": [{"name": "Name", "parameters": [], "returntype": "String"},
                                         {"name": "Symbol", "parameters": [], "returntype": "String"},
                                         {"name": "Decimal", "parameters": [], "returntype": "Integer"},
                                         {"name": "Main", "parameters": [{"name": "operation", "type": "String"},
                                                                         {"name": "args", "type": "Array"}],
                                          "returntype": "Any"},
                                         {"name": "Init", "parameters": [], "returntype": "Boolean"},
                                         {"name": "Transfer", "parameters": [{"name": "from", "type": "ByteArray"},
                                                                             {"name": "to", "type": "ByteArray"},
                                                                             {"name": "value", "type": "Integer"}],
                                          "returntype": "Boolean"},
                                         {"name": "TransferMulti", "parameters": [{"name": "args", "type": "Array"}],
                                          "returntype": "Boolean"},
                                         {"name": "BalanceOf", "parameters": [{"name": "address", "type": "ByteArray"}],
                                          "returntype": "Integer"},
                                         {"name": "TotalSupply", "parameters": [], "returntype": "Integer"},
                                         {"name": "Approve", "parameters": [{"name": "owner", "type": "ByteArray"},
                                                                            {"name": "spender", "type": "ByteArray"},
                                                                            {"name": "amount", "type": "Integer"}],
                                          "returntype": "Boolean"}, {"name": "TransferFrom", "parameters": [
                                   {"name": "spender", "type": "ByteArray"}, {"name": "from", "type": "ByteArray"},
                                   {"name": "to", "type": "ByteArray"}, {"name": "amount", "type": "Integer"}],
                                                                     "returntype": "Boolean"}, {"name": "Allowance",
                                                                                                "parameters": [
                                                                                                    {"name": "owner",
                                                                                                     "type": "ByteArray"},
                                                                                                    {"name": "spender",
                                                                                                     "type": "ByteArray"}],
                                                                                                "returntype": "Integer"}],
                           "events": [{"name": "transfer", "parameters": [{"name": "from", "type": "ByteArray"},
                                                                          {"name": "to", "type": "ByteArray"},
                                                                          {"name": "value", "type": "Integer"}],
                                       "returntype": "Void"}, {"name": "approval",
                                                               "parameters": [{"name": "onwer", "type": "ByteArray"},
                                                                              {"name": "spender", "type": "ByteArray"},
                                                                              {"name": "value", "type": "Integer"}],
                                                               "returntype": "Void"}]}
        self.__update_abi_info()

    def set_contract_address(self, contract_address: str or bytearray or bytes):
        if len(contract_address) == 20:
            if isinstance(contract_address, bytes):
                self.__contract_address = bytearray(contract_address)
            elif isinstance(contract_address, bytearray):
                self.__contract_address = contract_address
            else:
                raise SDKException(ErrorCode.param_err('the data type of the contract address unsupported.'))
        elif isinstance(contract_address, str) and len(contract_address) == 40:
            self.__contract_address = bytearray(binascii.a2b_hex(contract_address))
        else:
            raise SDKException(ErrorCode.param_err('the length of contract address should be 20 bytes.'))

    def __update_abi_info(self):
        try:
            nep4_hash = self.__oep4_abi['hash']
        except KeyError:
            nep4_hash = self.get_contract_address(is_hex=True)
        try:
            entry_point = self.__oep4_abi['entrypoint']
        except KeyError:
            entry_point = ''
        functions = self.__oep4_abi['functions']
        try:
            events = self.__oep4_abi['events']
        except KeyError:
            events = list()
        self.__abi_info = AbiInfo(nep4_hash, entry_point, functions, events)

    def __get_token_setting(self, func_name: str) -> str:
        func = self.__abi_info.get_function(func_name)
        res = self.__sdk.neo_vm().send_transaction(self.__contract_address, None, None, 0, 0, func, True)
        return res

    def get_contract_address(self, is_hex: bool = True) -> str or bytearray:
        if is_hex:
            array_address = self.__contract_address
            array_address.reverse()
            return binascii.b2a_hex(array_address)
        else:
            return self.__contract_address

    def get_abi(self) -> dict:
        return self.__oep4_abi

    def get_name(self) -> str:
        name = self.__get_token_setting('Name')
        return bytes.fromhex(name).decode()

    def get_symbol(self) -> str:
        get_symbol = self.__get_token_setting('Symbol')
        return bytes.fromhex(get_symbol).decode()

    def get_decimal(self) -> int:
        decimals = self.__get_token_setting('Decimal')
        return int(decimals)

    def init(self, acct: Account, payer_acct: Account, gas_limit: int, gas_price: int) -> str:
        func = self.__abi_info.get_function('Init')
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address, acct, payer_acct, gas_limit, gas_price,
                                                       func, False)
        return tx_hash

    def get_total_supply(self) -> int:
        total_supply = self.__get_token_setting('TotalSupply')
        array = bytearray(binascii.a2b_hex(total_supply.encode('ascii')))
        array.reverse()
        try:
            supply = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            supply = 0
        return supply

    def balance_of(self, address: str):
        func = self.__abi_info.get_function('BalanceOf')
        if len(address) == 40:
            address = binascii.a2b_hex(address)
        elif len(address) == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('the address is mistake.'))
        func.set_params_value((address,))
        balance = self.__sdk.neo_vm().send_transaction(self.__contract_address, None, None, 0, 0, func, True)
        array = bytearray(binascii.a2b_hex(balance.encode('ascii')))
        array.reverse()
        try:
            balance = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            balance = 0
        return balance

    def transfer(self, acct: Account, payer_acct: Account, gas_limit: int, gas_price: int, from_address: str,
                 to_address: str, value: int):
        from_address_len = len(from_address)
        if from_address_len == 40:
            from_address = binascii.a2b_hex(from_address)
        elif from_address_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('from address is mistake.'))
        to_address_len = len(to_address)
        if to_address_len == 40:
            to_address = binascii.a2b_hex(to_address)
        elif to_address_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('to address is mistake.'))
        if isinstance(value, int):
            params = (from_address, to_address, value)
        else:
            raise SDKException(ErrorCode.param_err('the type of value is mistake.'))
        func = self.__abi_info.get_function('Transfer')
        func.set_params_value(params)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address, acct, payer_acct, gas_limit, gas_price,
                                                       func,
                                                       False)
        return tx_hash

    def transfer_multi(self, payer: Account, signers: list, gas_limit: int, gas_price: int, args: list):
        func = self.__abi_info.get_function('TransferMulti')
        func.set_params_value((args,))
        params = BuildParams.serialize_abi_function(func)
        unix_time_now = int(time.time())
        params.append(0x67)
        for i in self.__contract_address:
            params.append(i)
        signers_len = len(signers)
        if signers_len == 0:
            raise SDKException(ErrorCode.param_err('payer account is None.'))
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), params,
                         bytearray(), [], bytearray())
        for index in range(signers_len):
            self.__sdk.add_sign_transaction(tx, signers[index])
        tx_hash = self.__sdk.rpc.send_raw_transaction(tx)
        return tx_hash

    def approve(self, acct: Account, payer_acct: Account, gas_limit: int, gas_price: int, owner, spender, amount):
        owner_len = len(owner)
        if owner_len == 40:
            owner = binascii.a2b_hex(owner)
        elif owner_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('owner address is mistake.'))
        spender_len = len(spender)
        if spender_len == 40:
            spender = binascii.a2b_hex(spender)
        elif spender_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('spender address is mistake.'))
        if isinstance(amount, int):
            params = (owner, spender, amount)
        else:
            raise SDKException(ErrorCode.param_err('the type of value is mistake.'))
        func = self.__abi_info.get_function('Approve')
        func.set_params_value(params)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address, acct, payer_acct, gas_limit, gas_price,
                                                       func, False)
        return tx_hash

    def allowance(self, owner, spender):
        owner_len = len(owner)
        if owner_len == 40:
            owner = binascii.a2b_hex(owner)
        elif owner_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('owner address is mistake.'))
        spender_len = len(spender)
        if spender_len == 40:
            spender = binascii.a2b_hex(spender)
        elif spender_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('spender address is mistake.'))
        func = self.__abi_info.get_function('Allowance')
        func.set_params_value((owner, spender))
        allowance = self.__sdk.neo_vm().send_transaction(self.__contract_address, None, None, 0, 0, func, True)
        array = bytearray(binascii.a2b_hex(allowance.encode('ascii')))
        array.reverse()
        try:
            allowance = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            allowance = 0
        return allowance

    def transfer_from(self, acct: Account, payer_acct: Account, gas_limit: int, gas_price: int,
                      spender_address: str, from_address: str, to_address: str, value: int):
        spender_address_len = len(spender_address)
        if spender_address_len == 40:
            spender_address = binascii.a2b_hex(spender_address)
        elif spender_address_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('spender address is mistake.'))

        from_address_len = len(from_address)
        if from_address_len == 40:
            from_address = binascii.a2b_hex(from_address)
        elif from_address_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('from address is mistake.'))

        to_address_len = len(to_address)
        if from_address_len == 40:
            to_address = binascii.a2b_hex(to_address)
        elif to_address_len == 20:
            pass
        else:
            raise SDKException(ErrorCode.param_err('to address is mistake.'))

        if isinstance(value, int):
            params = (spender_address, from_address, to_address, value)
        else:
            raise SDKException(ErrorCode.param_err('the type of value is mistake.'))
        func = self.__abi_info.get_function('TransferFrom')
        func.set_params_value(params)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address, acct, payer_acct, gas_limit, gas_price,
                                                       func, False)
        return tx_hash
