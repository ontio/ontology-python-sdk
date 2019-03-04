#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from ontology.common.address import Address
from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser
from ontology.utils.contract_event import ContractEventParser
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class Oep4(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__hex_contract_address = ''

    @property
    def hex_contract_address(self):
        return self.__hex_contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address: str):
        if not isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            raise SDKException(ErrorCode.require_str_params)
        self.__hex_contract_address = hex_contract_address

    def __get_token_setting(self, func_name: str) -> str:
        func = InvokeFunction(func_name)
        res = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        return res.get('Result', '')

    @staticmethod
    def __b58_address_check(b58_address):
        if not isinstance(b58_address, str):
            raise SDKException(ErrorCode.param_err('the data type of base58 encode address should be the string.'))
        if len(b58_address) != 34:
            raise SDKException(ErrorCode.param_err('the length of base58 encode address should be 34 bytes.'))

    def get_name(self) -> str:
        """
        This interface is used to call the Name method in ope4
        that return the name of an oep4 token.

        :return: the string name of the oep4 token.
        """
        name = self.__get_token_setting('name')
        return ContractDataParser.to_utf8_str(name)

    def get_symbol(self) -> str:
        """
        This interface is used to call the Symbol method in ope4
        that return the symbol of an oep4 token.

        :return: a short string symbol of the oep4 token
        """
        symbol = self.__get_token_setting('symbol')
        return ContractDataParser.to_utf8_str(symbol)

    def get_decimal(self) -> int:
        """
        This interface is used to call the Decimal method in ope4
        that return the number of decimals used by the oep4 token.

        :return: the number of decimals used by the oep4 token.
        """
        decimals = self.__get_token_setting('decimals')
        return ContractDataParser.to_int(decimals)

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
        func = InvokeFunction('init')
        tx_hash = self.__sdk.get_network().send_neo_vm_transaction(self.__hex_contract_address, acct, payer_acct,
                                                                   gas_limit, gas_price, func)
        return tx_hash

    def get_total_supply(self) -> int:
        """
        This interface is used to call the TotalSupply method in ope4
        that return the total supply of the oep4 token.

        :return: the total supply of the oep4 token.
        """
        func = InvokeFunction('totalSupply')
        response = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        try:
            total_supply = ContractDataParser.to_int(response['Result'])
        except SDKException:
            total_supply = 0
        return total_supply

    def balance_of(self, b58_address: str) -> int:
        """
        This interface is used to call the BalanceOf method in ope4
        that query the ope4 token balance of the given base58 encode address.

        :param b58_address: the base58 encode address.
        :return: the oep4 token balance of the base58 encode address.
        """
        func = InvokeFunction('balanceOf')
        Oep4.__b58_address_check(b58_address)
        address = Address.b58decode(b58_address).to_bytes()
        func.set_params_value(address)
        result = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        try:
            balance = ContractDataParser.to_int(result['Result'])
        except SDKException:
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
        func = InvokeFunction('transfer')
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
        tx_hash = self.__sdk.get_network().send_neo_vm_transaction(self.__hex_contract_address, from_acct, payer_acct,
                                                                   gas_limit, gas_price, func, False)
        return tx_hash

    def query_transfer_event(self, tx_hash: str):
        event = self.__sdk.get_network().get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        notify = ContractDataParser.parse_addr_addr_int_notify(notify)
        return notify

    def query_multi_transfer_event(self, tx_hash: str) -> list:
        event = self.__sdk.get_network().get_smart_contract_event_by_tx_hash(tx_hash)
        notify_list = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        for index, notify in enumerate(notify_list):
            if notify.get('ContractAddress', '') == self.__hex_contract_address:
                notify_list[index]['States'][0] = ContractDataParser.to_utf8_str(notify['States'][0])
                notify_list[index]['States'][1] = ContractDataParser.to_b58_address(notify['States'][1])
                notify_list[index]['States'][2] = ContractDataParser.to_b58_address(notify['States'][2])
                notify_list[index]['States'][3] = ContractDataParser.to_int(notify['States'][3])
        return notify_list

    def query_approve_event(self, tx_hash: str):
        event = self.__sdk.get_network().get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        notify = ContractDataParser.parse_addr_addr_int_notify(notify)
        return notify

    def transfer_multi(self, transfer_list: list, payer_acct: Account, signers: list, gas_limit: int, gas_price: int):
        """
        This interface is used to call the TransferMulti method in ope4
        that allow transfer amount of token from multiple from-account to multiple to-account multiple times.

        :param transfer_list: a parameter list with each item contains three sub-items:
                base58 encode transaction sender address,
                base58 encode transaction receiver address,
                amount of token in transaction.
        :param payer_acct: an Account class that used to pay for the transaction.
        :param signers: a signer list used to sign this transaction which should contained all sender in args.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: the hexadecimal transaction hash value.
        """
        func = InvokeFunction('transferMulti')
        for index, item in enumerate(transfer_list):
            Oep4.__b58_address_check(item[0])
            Oep4.__b58_address_check(item[1])
            if not isinstance(item[2], int):
                raise SDKException(ErrorCode.param_err('the data type of value should be int.'))
            if item[2] < 0:
                raise SDKException(ErrorCode.param_err('the value should be equal or great than 0.'))
            from_address_array = Address.b58decode(item[0]).to_bytes()
            to_address_array = Address.b58decode(item[1]).to_bytes()
            transfer_list[index] = [from_address_array, to_address_array, item[2]]
        for item in transfer_list:
            func.add_params_value(item)
        params = func.create_invoke_code()
        unix_time_now = int(time.time())
        params.append(0x67)
        bytearray_contract_address = bytearray.fromhex(self.__hex_contract_address)
        bytearray_contract_address.reverse()
        for i in bytearray_contract_address:
            params.append(i)
        if len(signers) == 0:
            raise SDKException(ErrorCode.param_err('payer account is None.'))
        payer_address = payer_acct.get_address().to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_address, params,
                         bytearray(), [])
        for signer in signers:
            tx.add_sign_transaction(signer)
        tx_hash = self.__sdk.get_network().send_raw_transaction(tx)
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
        func = InvokeFunction('approve')
        if not isinstance(amount, int):
            raise SDKException(ErrorCode.param_err('the data type of amount should be int.'))
        if amount < 0:
            raise SDKException(ErrorCode.param_err('the amount should be equal or great than 0.'))
        owner_address = owner_acct.get_address().to_bytes()
        Oep4.__b58_address_check(b58_spender_address)
        spender_address = Address.b58decode(b58_spender_address).to_bytes()
        func.set_params_value(owner_address, spender_address, amount)
        tx_hash = self.__sdk.get_network().send_neo_vm_transaction(self.__hex_contract_address, owner_acct, payer_acct,
                                                                   gas_limit, gas_price, func)
        return tx_hash

    def allowance(self, b58_owner_address: str, b58_spender_address: str):
        """
        This interface is used to call the Allowance method in ope4
        that query the amount of spender still allowed to withdraw from owner account.

        :param b58_owner_address: a base58 encode address that represent owner's account.
        :param b58_spender_address: a base58 encode address that represent spender's account.
        :return: the amount of oep4 token that owner allow spender to transfer from the owner account.
        """
        func = InvokeFunction('allowance')
        Oep4.__b58_address_check(b58_owner_address)
        owner = Address.b58decode(b58_owner_address).to_bytes()
        Oep4.__b58_address_check(b58_spender_address)
        spender = Address.b58decode(b58_spender_address).to_bytes()
        func.set_params_value(owner, spender)
        result = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        try:
            allowance = ContractDataParser.to_int(result['Result'])
        except SDKException:
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
        func = InvokeFunction('transferFrom')
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
        params = func.create_invoke_code()
        unix_time_now = int(time.time())
        params.append(0x67)
        bytearray_contract_address = bytearray.fromhex(self.__hex_contract_address)
        bytearray_contract_address.reverse()
        for i in bytearray_contract_address:
            params.append(i)
        if payer_acct is None:
            raise SDKException(ErrorCode.param_err('payer account is None.'))
        payer_address_array = payer_acct.get_address().to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_address_array, params,
                         bytearray(), [])

        tx.sign_transaction(spender_acct)
        if spender_acct.get_address_base58() != payer_acct.get_address_base58():
            tx.add_sign_transaction(payer_acct)
        tx_hash = self.__sdk.get_network().send_raw_transaction(tx)
        return tx_hash
