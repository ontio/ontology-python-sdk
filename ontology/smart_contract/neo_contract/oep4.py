#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import binascii

from ontology.common.address import Address
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
        self.__oep4_abi = {"contractHash": "85848b5ec3b15617e396bdd62cb49575738dd413", "abi": {"functions": [
            {"name": "Main", "parameters": [{"name": "operation", "type": ""}, {"name": "args", "type": ""}],
             "returntype": ""}, {"name": "init", "parameters": [{"name": "", "type": ""}], "returntype": ""},
            {"name": "name", "parameters": [{"name": "", "type": ""}], "returntype": ""},
            {"name": "symbol", "parameters": [{"name": "", "type": ""}], "returntype": ""},
            {"name": "decimals", "parameters": [{"name": "", "type": ""}], "returntype": ""},
            {"name": "totalSupply", "parameters": [{"name": "", "type": ""}], "returntype": ""},
            {"name": "balanceOf", "parameters": [{"name": "account", "type": ""}], "returntype": ""},
            {"name": "transfer", "parameters": [{"name": "from_acct", "type": ""}, {"name": "to_acct", "type": ""},
                                                {"name": "amount", "type": ""}], "returntype": ""},
            {"name": "transferMulti", "parameters": [{"name": "args", "type": ""}], "returntype": ""},
            {"name": "approve", "parameters": [{"name": "owner", "type": ""}, {"name": "spender", "type": ""},
                                               {"name": "amount", "type": ""}], "returntype": ""},
            {"name": "transferFrom", "parameters": [{"name": "spender", "type": ""}, {"name": "from_acct", "type": ""},
                                                    {"name": "to_acct", "type": ""}, {"name": "amount", "type": ""}],
             "returntype": ""},
            {"name": "allowance", "parameters": [{"name": "owner", "type": ""}, {"name": "spender", "type": ""}],
             "returntype": ""}]}}

        self.__update_abi_info()

    def set_contract_address(self, contract_address: str or bytearray or bytes):
        if len(contract_address) == 20:
            if isinstance(contract_address, bytes):
                self.__contract_address = bytearray(contract_address)
                self.__update_abi_info()
            elif isinstance(contract_address, bytearray):
                self.__contract_address = contract_address
                self.__update_abi_info()
            else:
                raise SDKException(ErrorCode.param_err('the data type of the contract address unsupported.'))
        elif isinstance(contract_address, str) and len(contract_address) == 40:
            self.__contract_address = bytearray(binascii.a2b_hex(contract_address))
            self.__contract_address.reverse()
            self.__update_abi_info()
        else:
            raise SDKException(ErrorCode.param_err('the length of contract address should be 20 bytes.'))

    def __update_abi_info(self):
        entry_point = self.__oep4_abi.get('entrypoint', '')
        functions = self.__oep4_abi['abi']['functions']
        events = self.__oep4_abi.get('events', list())
        self.__abi_info = AbiInfo(self.get_contract_address(is_hex=True), entry_point, functions, events)

    def __get_token_setting(self, func_name: str) -> str:
        func = self.__abi_info.get_function(func_name)
        res = self.__sdk.neo_vm().send_transaction(self.__contract_address, None, None, 0, 0, func, True)
        return res

    @staticmethod
    def __b58_address_check(b58_address):
        if not isinstance(b58_address, str):
            raise SDKException(ErrorCode.param_err('the data type of base58 encode address should be the string.'))
        if len(b58_address) != 34:
            raise SDKException(ErrorCode.param_err('the length of base58 encode address should be 34 bytes.'))

    def get_contract_address(self, is_hex: bool = True) -> str or bytearray:
        if is_hex:
            array_address = self.__contract_address.copy()
            array_address.reverse()
            return binascii.b2a_hex(array_address).decode('ascii')
        else:
            return self.__contract_address

    def get_abi(self) -> dict:
        return self.__oep4_abi

    def get_name(self) -> str:
        """
        This interface is used to call the Name method in ope4
        that return the name of an oep4 token.

        :return: the string name of the oep4 token.
        """
        name = self.__get_token_setting('name')
        return bytes.fromhex(name).decode()

    def get_symbol(self) -> str:
        """
        This interface is used to call the Symbol method in ope4
        that return the symbol of an oep4 token.

        :return: a short string symbol of the oep4 token
        """
        get_symbol = self.__get_token_setting('symbol')
        return bytes.fromhex(get_symbol).decode()

    def get_decimal(self) -> int:
        """
        This interface is used to call the Decimal method in ope4
        that return the number of decimals used by the oep4 token.

        :return: the number of decimals used by the oep4 token.
        """
        decimals = self.__get_token_setting('decimals')
        return int(decimals[:2], 16)

    def init(self, acct: Account, payer_acct: Account, gas_limit: int, gas_price: int) -> str:
        """
        This interface is used to call the TotalSupply method in ope4
        that initialize smart contract parameter.

        :param acct: an Account class that used to sign the transaction.
        :param payer_acct: an Account class that used to pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: the hexadecimal transaction hash value.
        """
        func = self.__abi_info.get_function('init')
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address, acct, payer_acct, gas_limit, gas_price,
                                                       func, False)
        return tx_hash

    def get_total_supply(self) -> int:
        """
        This interface is used to call the TotalSupply method in ope4
        that return the total supply of the oep4 token.

        :return: the total supply of the oep4 token.
        """
        total_supply = self.__get_token_setting('totalSupply')
        array = bytearray(binascii.a2b_hex(total_supply.encode('ascii')))
        array.reverse()
        try:
            supply = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            supply = 0
        return supply

    def balance_of(self, b58_address: str) -> int:
        """
        This interface is used to call the BalanceOf method in ope4
        that query the ope4 token balance of the given base58 encode address.

        :param b58_address: the base58 encode address.
        :return: the oep4 token balance of the base58 encode address.
        """
        func = self.__abi_info.get_function('balanceOf')
        Oep4.__b58_address_check(b58_address)
        address = Address.b58decode(b58_address).to_bytes()
        func.set_params_value(address)
        balance = self.__sdk.neo_vm().send_transaction(self.__contract_address, None, None, 0, 0, func, True)
        array = bytearray(binascii.a2b_hex(balance.encode('ascii')))
        array.reverse()
        try:
            balance = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            balance = 0
        return balance

    def transfer(self, from_acct: Account, b58_to_address: str, value: int, payer_acct: Account, gas_limit: int,
                 gas_price: int) -> str:
        """
        This interface is used to call the Transfer method in ope4
        that transfer an amount of tokens from one account to another account.

        :param from_acct: an Account class that send the oep4 token.
        :param b58_to_address: a base58 encode address that receive the oep4 token.
        :param value: an int value that indicate the amount oep4 token that will be transferred in this transaction.
        :param payer_acct: an Account class that used to pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: the hexadecimal transaction hash value.
        """
        func = self.__abi_info.get_function('transfer')
        if not isinstance(value, int):
            raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
        if value < 0:
            raise SDKException(ErrorCode.param_err('the value should be equal or great than 0.'))
        if not isinstance(from_acct, Account):
            raise SDKException(ErrorCode.param_err('the data type of from_acct should be Account.'))
        Oep4.__b58_address_check(b58_to_address)
        from_address = from_acct.get_address().to_bytes()
        to_address = Address.b58decode(b58_to_address).to_bytes()
        func.set_params_value(from_address, to_address, value)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address, from_acct, payer_acct, gas_limit,
                                                       gas_price, func, False)
        return tx_hash

    def transfer_multi(self, args: list, payer_acct: Account, signers: list, gas_limit: int, gas_price: int):
        """
        This interface is used to call the TransferMulti method in ope4
        that allow transfer amount of token from multiple from-account to multiple to-account multiple times.

        :param args: a parameter list with each item contains three sub-items:
                base58 encode transaction sender address,
                base58 encode transaction receiver address,
                amount of token in transaction.
        :param payer_acct: an Account class that used to pay for the transaction.
        :param signers: a signer list used to sign this transaction which should contained all sender in args.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: the hexadecimal transaction hash value.
        """
        func = self.__abi_info.get_function('transferMulti')
        for index in range(len(args)):
            item = args[index]
            Oep4.__b58_address_check(item[0])
            Oep4.__b58_address_check(item[1])
            if not isinstance(item[2], int):
                raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
            if item[2] < 0:
                raise SDKException(ErrorCode.param_err('the value should be equal or great than 0.'))
            from_address_array = Address.b58decode(item[0]).to_bytes()
            to_address_array = Address.b58decode(item[1]).to_bytes()
            args[index] = [from_address_array, to_address_array, item[2]]
        func.set_params_value(args)
        params = BuildParams.serialize_abi_function(func)
        unix_time_now = int(time.time())
        params.append(0x67)
        for i in self.__contract_address:
            params.append(i)
        signers_len = len(signers)
        if signers_len == 0:
            raise SDKException(ErrorCode.param_err('payer account is None.'))
        payer_address = payer_acct.get_address().to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_address, params,
                         bytearray(), [], bytearray())
        for index in range(signers_len):
            self.__sdk.add_sign_transaction(tx, signers[index])
        tx_hash = self.__sdk.rpc.send_raw_transaction(tx)
        return tx_hash

    def approve(self, owner_acct: Account, b58_spender_address: str, amount: int, payer_acct: Account, gas_limit: int,
                gas_price: int):
        """
        This interface is used to call the Approve method in ope4
        that allows spender to withdraw a certain amount of oep4 token from owner account multiple times.

        If this function is called again, it will overwrite the current allowance with new value.

        :param owner_acct: an Account class that indicate the owner.
        :param b58_spender_address: a base58 encode address that be allowed to spend the oep4 token in owner's account.
        :param amount: an int value that indicate the amount oep4 token that will be transferred in this transaction.
        :param payer_acct: an Account class that used to pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: the hexadecimal transaction hash value.
        """
        func = self.__abi_info.get_function('approve')
        if not isinstance(amount, int):
            raise SDKException(ErrorCode.param_err('the data type of amount should be int.'))
        if amount < 0:
            raise SDKException(ErrorCode.param_err('the amount should be equal or great than 0.'))
        owner_address = owner_acct.get_address().to_bytes()
        Oep4.__b58_address_check(b58_spender_address)
        spender_address = Address.b58decode(b58_spender_address).to_bytes()
        func.set_params_value(owner_address, spender_address, amount)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address, owner_acct, payer_acct, gas_limit,
                                                       gas_price, func, False)
        return tx_hash

    def allowance(self, b58_owner_address: str, b58_spender_address: str):
        """
        This interface is used to call the Allowance method in ope4
        that query the amount of spender still allowed to withdraw from owner account.

        :param b58_owner_address: a base58 encode address that represent owner's account.
        :param b58_spender_address: a base58 encode address that represent spender's account.
        :return: the amount of oep4 token that owner allow spender to transfer from the owner account.
        """
        func = self.__abi_info.get_function('allowance')
        Oep4.__b58_address_check(b58_owner_address)
        owner = Address.b58decode(b58_owner_address).to_bytes()
        Oep4.__b58_address_check(b58_spender_address)
        spender = Address.b58decode(b58_spender_address).to_bytes()
        func.set_params_value(owner, spender)
        allowance = self.__sdk.neo_vm().send_transaction(self.__contract_address, None, None, 0, 0, func, True)
        array = bytearray(binascii.a2b_hex(allowance.encode('ascii')))
        array.reverse()
        try:
            allowance = int(binascii.b2a_hex(array).decode('ascii'), 16)
        except ValueError:
            allowance = 0
        return allowance

    def transfer_from(self, spender_acct: Account, b58_from_address: str, b58_to_address: str, value: int,
                      payer_acct: Account, gas_limit: int, gas_price: int):
        """
        This interface is used to call the Allowance method in ope4
        that allow spender to withdraw amount of oep4 token from from-account to to-account.

        :param spender_acct: an Account class that actually spend oep4 token.
        :param b58_from_address: an base58 encode address that actually pay oep4 token for the spender's spending.
        :param b58_to_address: a base58 encode address that receive the oep4 token.
        :param value: the amount of ope4 token in this transaction.
        :param payer_acct: an Account class that used to pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: the hexadecimal transaction hash value.
        """
        func = self.__abi_info.get_function('transferFrom')
        Oep4.__b58_address_check(b58_from_address)
        Oep4.__b58_address_check(b58_to_address)
        if not isinstance(spender_acct, Account):
            raise SDKException(ErrorCode.param_err('the data type of spender_acct should be Account.'))
        spender_address_array = spender_acct.get_address().to_bytes()
        from_address_array = Address.b58decode(b58_from_address).to_bytes()
        to_address_array = Address.b58decode(b58_to_address).to_bytes()
        if not isinstance(value, int):
            raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
        func.set_params_value(spender_address_array, from_address_array, to_address_array, value)
        params = BuildParams.serialize_abi_function(func)
        unix_time_now = int(time.time())
        params.append(0x67)
        for i in self.__contract_address:
            params.append(i)
        if payer_acct is None:
            raise SDKException(ErrorCode.param_err('payer account is None.'))
        payer_address_array = payer_acct.get_address().to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_address_array, params,
                         bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, spender_acct)
        if spender_acct.get_address_base58() != payer_acct.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer_acct)
        tx_hash = self.__sdk.rpc.send_raw_transaction(tx)
        return tx_hash
