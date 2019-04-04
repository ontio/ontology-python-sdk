"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import List

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class ContractEventParser(object):
    @staticmethod
    def __check_event(event: dict):
        if not isinstance(event, dict):
            raise SDKException(ErrorCode.require_dict_params)

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
        if not isinstance(hex_contract_address, str):
            raise SDKException(ErrorCode.require_str_params)
        ContractEventParser.__check_event(event)
        notify_list = ContractEventParser.get_notify_list(event)
        specify_notify_list = list()
        for notify in notify_list:
            if notify['ContractAddress'] == hex_contract_address:
                specify_notify_list.append(notify)
        return specify_notify_list

    @staticmethod
    def get_event_from_event_list_by_contract_address(event_list: list, hex_contract_address: str) -> List[dict]:
        if not isinstance(hex_contract_address, str):
            raise SDKException(ErrorCode.require_str_params)
        specify_event_list = list()
        for event in event_list:
            if event['ContractAddress'] == hex_contract_address:
                specify_event_list.append(event)
        return specify_event_list

    @staticmethod
    def get_notify_list_by_contract_address(event: dict, hex_contract_address: str) -> list or dict:
        if not isinstance(hex_contract_address, str):
            raise SDKException(ErrorCode.require_str_params)
        ContractEventParser.__check_event(event)
        notify_list = ContractEventParser.get_notify_list(event)
        specify_notify_list = list()
        for notify in notify_list:
            if notify['ContractAddress'] == hex_contract_address:
                specify_notify_list.append(notify)
        if len(specify_notify_list) == 1:
            specify_notify_list = specify_notify_list[0]
        return specify_notify_list

    @staticmethod
    def get_states_by_contract_address(event: dict, hex_contract_address: str):
        if not isinstance(hex_contract_address, str):
            raise SDKException(ErrorCode.require_str_params)
        notify_list = ContractEventParser.__get_notify_list_by_contract_address(event, hex_contract_address)
        states_list = list()
        for notify in notify_list:
            states = notify.get('States', list())
            states_list.append(states)
        states_list.count(list)
        if len(states_list) == 1:
            states_list = states_list[0]
        return states_list
