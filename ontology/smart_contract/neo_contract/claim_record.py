#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser
from ontology.utils.contract_event import ContractEventParser
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class ClaimRecord(object):
    def __init__(self, sdk, hex_contract_address: str = ''):
        self.__sdk = sdk
        if isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            self.__hex_contract_address = hex_contract_address
        else:
            self.__hex_contract_address = '36bb5c053b6b839c8f6b923fe852f91239b9fccc'

    @property
    def hex_contract_address(self):
        return self.__hex_contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address):
        if isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            self.__hex_contract_address = hex_contract_address
        else:
            raise SDKException(ErrorCode.invalid_contract_address(hex_contract_address))

    def commit(self, claim_id: str, issuer_acct: Account, owner_ont_id: str, payer_acct: Account, gas_limit: int,
               gas_price: int):
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('Gas limit less than 0.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('Gas price less than 0.'))
        func = InvokeFunction('Commit')
        func.set_params_value(claim_id, issuer_acct.get_address_bytes(), owner_ont_id)
        tx_hash = self.__sdk.get_network().send_neo_vm_transaction(self.__hex_contract_address, issuer_acct, payer_acct,
                                                                   gas_limit, gas_price, func)
        return tx_hash

    def revoke(self, claim_id: str, issuer_acct: Account, payer_acct: Account, gas_limit: int, gas_price: int):
        if gas_limit < 0:
            raise SDKException(ErrorCode.other_error('Gas limit less than 0.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('Gas price less than 0.'))
        func = InvokeFunction('Revoke')
        func.set_params_value(claim_id, issuer_acct.get_address_bytes())
        tx_hash = self.__sdk.get_network().send_neo_vm_transaction(self.__hex_contract_address, issuer_acct, payer_acct,
                                                                   gas_limit, gas_price, func)
        return tx_hash

    def get_status(self, claim_id: str):
        func = InvokeFunction('GetStatus')
        func.set_params_value(claim_id)
        result = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        status = result['Result']
        if status == '':
            status = False
        else:
            status = ContractDataParser.to_dict(status)
            status = bool(status[3])
        return status

    def query_commit_event(self, tx_hash: str):
        event = self.__sdk.get_network().get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        if len(notify) == 0:
            return notify
        if len(notify['States']) == 4:
            notify['States'][0] = ContractDataParser.to_utf8_str(notify['States'][0])
            notify['States'][1] = ContractDataParser.to_b58_address(notify['States'][1])
            notify['States'][2] = ContractDataParser.to_utf8_str(notify['States'][2])
            notify['States'][3] = ContractDataParser.to_hex_str(notify['States'][3])
        if len(notify['States']) == 3:
            notify['States'][0] = ContractDataParser.to_utf8_str(notify['States'][0])
            notify['States'][1] = ContractDataParser.to_hex_str(notify['States'][1])
            notify['States'][2] = ContractDataParser.to_utf8_str(notify['States'][2])
        return notify

    def query_revoke_event(self, tx_hash: str):
        event = self.__sdk.get_network().get_smart_contract_event_by_tx_hash(tx_hash)
        notify = ContractEventParser.get_notify_list_by_contract_address(event, self.__hex_contract_address)
        if len(notify['States']) == 4:
            notify['States'][0] = ContractDataParser.to_utf8_str(notify['States'][0])
            notify['States'][1] = ContractDataParser.to_b58_address(notify['States'][1])
            notify['States'][2] = ContractDataParser.to_utf8_str(notify['States'][2])
            notify['States'][3] = ContractDataParser.to_hex_str(notify['States'][3])
        return notify
