#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from ontology.common.error_code import ErrorCode
from ontology.exception.exception import SDKException


class ContractEventParser(object):
    @staticmethod
    def __check_event(event: dict):
        if not isinstance(event, dict):
            raise SDKException(ErrorCode.other_error('The type of event should be dict'))

    @staticmethod
    def get_tx_hash(event: dict):
        ContractEventParser.__check_event(event)
        try:
            return event['TxHash']
        except KeyError:
            raise SDKException(ErrorCode.other_error('TxHash not found in event'))

    @staticmethod
    def get_state(event: dict):
        ContractEventParser.__check_event(event)
        try:
            return event['State']
        except KeyError:
            raise SDKException(ErrorCode.other_error('State not found in event'))

    @staticmethod
    def get_gas_consumed(event: dict):
        ContractEventParser.__check_event(event)
        try:
            return event['GasConsumed']
        except KeyError:
            raise SDKException(ErrorCode.other_error('Gas consumed not found in event'))

    @staticmethod
    def get_notify_list(event: dict):
        ContractEventParser.__check_event(event)
        try:
            return event['Notify']
        except KeyError:
            raise SDKException(ErrorCode.other_error('Notify not found in event'))

    @staticmethod
    def get_ong_contract_notify(event: dict) -> dict:
        ContractEventParser.__check_event(event)
        notify_list = ContractEventParser.get_notify_list(event)
        for notify in notify_list:
            if notify['ContractAddress'] == '0200000000000000000000000000000000000000':
                return notify
        return dict()

    @staticmethod
    def __get_notify_list_by_contract_address(event: dict, hex_contract_address: str) -> list:
        ContractEventParser.__check_event(event)
        notify_list = ContractEventParser.get_notify_list(event)
        specify_notify_list = list()
        for notify in notify_list:
            if notify['ContractAddress'] == hex_contract_address:
                specify_notify_list.append(notify)
        return specify_notify_list

    @staticmethod
    def get_event_from_event_list_by_contract_address(event_list: list, hex_contract_address: str) -> List[dict]:
        specify_event_list = list()
        for event in event_list:
            if event['ContractAddress'] == hex_contract_address:
                specify_event_list.append(event)
        return specify_event_list

    @staticmethod
    def get_notify_list_by_contract_address(event: dict, hex_contract_address: str) -> list:
        ContractEventParser.__check_event(event)
        notify_list = ContractEventParser.get_notify_list(event)
        specify_notify_list = list()
        for notify in notify_list:
            if notify['ContractAddress'] == hex_contract_address:
                specify_notify_list.append(notify)
        if len(specify_notify_list) == 1:
            specify_notify_list = notify_list[0]
        return specify_notify_list

    @staticmethod
    def get_states_by_contract_address(event: dict, hex_contract_address: str):
        notify_list = ContractEventParser.__get_notify_list_by_contract_address(event, hex_contract_address)
        states_list = list()
        for notify in notify_list:
            states = notify.get('States', list())
            states_list.append(states)
        states_list.count(list)
        if len(states_list) == 1:
            states_list = states_list[0]
        return states_list
