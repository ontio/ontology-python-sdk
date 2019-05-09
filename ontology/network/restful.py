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

import json
import requests

from typing import List, Union

from Cryptodome.Random.random import randint

from ontology.account.account import Account
from ontology.contract.neo.vm import NeoVm
from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.transaction import ensure_bytearray_contract_address
from ontology.contract.neo.abi.abi_function import AbiFunction
from ontology.contract.neo.abi.build_params import BuildParams
from ontology.contract.neo.invoke_function import InvokeFunction

TEST_RESTFUL_ADDRESS = ['http://polaris1.ont.io:20334', 'http://polaris2.ont.io:20334', 'http://polaris3.ont.io:20334']
MAIN_RESTFUL_ADDRESS = ['http://dappnode1.ont.io:20334', 'http://dappnode2.ont.io:20334']


class RestfulMethod(object):
    @staticmethod
    def get_version(url: str):
        return f'{url}/api/v1/version'

    @staticmethod
    def get_network_id(url: str):
        return f'{url}/api/v1/networkid'

    @staticmethod
    def get_connection_count(url: str):
        return f'{url}/api/v1/node/connectioncount'

    @staticmethod
    def get_gas_price(url: str):
        return f'{url}/api/v1/gasprice'

    @staticmethod
    def get_block_by_height(url: str, height: int):
        return f'{url}/api/v1/block/details/height/{height}?raw=0'

    @staticmethod
    def get_block_height(url: str):
        return f'{url}/api/v1/block/height'

    @staticmethod
    def get_block_by_hash(url: str, block_hash: str):
        return f'{url}/api/v1/block/details/hash/{block_hash}?raw=0'

    @staticmethod
    def get_account_balance(url: str, b58_address: str):
        return f'{url}/api/v1/balance/{b58_address}'

    @staticmethod
    def get_allowance(url: str, asset: str, b58_from_address: str, b58_to_address: str) -> str:
        return f'{url}/api/v1/allowance/{asset}/{b58_from_address}/{b58_to_address}'

    @staticmethod
    def get_transaction(url: str, tx_hash: str):
        return f'{url}/api/v1/transaction/{tx_hash}'

    @staticmethod
    def send_transaction(url: str, ):
        return f'{url}/api/v1/transaction?preExec=0'

    @staticmethod
    def send_transaction_pre_exec(url: str, ):
        return f'{url}/api/v1/transaction?preExec=1'

    @staticmethod
    def get_generate_block_time(url: str):
        return f'{url}/api/v1/node/generateblocktime'

    @staticmethod
    def get_contract(url: str, contract_address: str):
        return f'{url}/api/v1/contract/{contract_address}'

    @staticmethod
    def get_contract_event_by_height(url: str, height: int):
        return f'{url}/api/v1/smartcode/event/transactions/{height}'

    @staticmethod
    def get_contract_event_by_tx_hash(url: str, tx_hash: str):
        return f'{url}/api/v1/smartcode/event/txhash/{tx_hash}'

    @staticmethod
    def get_block_height_by_tx_hash(url: str, tx_hash: str):
        return f'{url}/api/v1/block/height/txhash/{tx_hash}'

    @staticmethod
    def get_storage(url: str, hex_contract_address: str, hex_key: str):
        return f'{url}/api/v1/storage/{hex_contract_address}/{hex_key}'

    @staticmethod
    def get_merkle_proof(url: str, tx_hash: str):
        return f'{url}/api/v1/merkleproof/{tx_hash}'

    @staticmethod
    def get_mem_pool_tx_count(url: str):
        return f'{url}/api/v1/mempool/txcount'

    @staticmethod
    def get_mem_pool_tx_state(url: str, tx_hash: str):
        return f'{url}/api/v1/mempool/txstate/{tx_hash}'

    @staticmethod
    def get_grant_ong(url: str, b58_address: str):
        return f'{url}/api/v1/grantong/{b58_address}'


class Restful(object):
    def __init__(self, url: str = ''):
        self._url = url

    def set_address(self, url: str):
        self._url = url

    def get_address(self):
        return self._url

    def connect_to_localhost(self):
        self.set_address('http://localhost:20334')

    def connect_to_test_net(self, index: int = 0):
        if index == 0:
            index = randint(1, 5)
        restful_address = f'http://polaris{index}.ont.io:20334'
        self.set_address(restful_address)

    def connect_to_main_net(self, index: int = 0):
        if index == 0:
            index = randint(1, 3)
        restful_address = f'http://dappnode{index}.ont.io:20334'
        self.set_address(restful_address)

    def __post(self, url: str, data: str):
        try:
            response = requests.post(url, data=data, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0]))
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            raise SDKException(ErrorCode.connect_timeout(self._url)) from None
        if response.status_code != 200:
            raise SDKException(ErrorCode.other_error(response.content.decode('utf-8')))
        try:
            response = json.loads(response.content.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        if response['Error'] != 0:
            raise SDKException(ErrorCode.other_error(response['Result']))
        return response

    def __get(self, url: str):
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.MissingSchema as e:
            raise SDKException(ErrorCode.connect_err(e.args[0]))
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            raise SDKException(ErrorCode.connect_timeout(self._url)) from None
        if response.status_code != 200:
            raise SDKException(ErrorCode.other_error(response.content.decode('utf-8')))
        try:
            response = json.loads(response.content.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        if response['Error'] != 0:
            if response['Result'] != '':
                raise SDKException(ErrorCode.other_error(response['Result']))
            else:
                raise SDKException(ErrorCode.other_error(response['Desc']))
        return response

    def get_version(self, is_full: bool = False):
        url = RestfulMethod.get_version(self._url)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_connection_count(self, is_full: bool = False) -> int:
        url = RestfulMethod.get_connection_count(self._url)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_gas_price(self, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_gas_price(self._url)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']['gasprice']

    def get_network_id(self, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_network_id(self._url)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_block_height(self, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_block_height(self._url)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_block_height_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_block_height_by_tx_hash(self._url, tx_hash)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_block_count_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        response = self.get_block_height_by_tx_hash(tx_hash, is_full=True)
        response['Result'] += 1
        if is_full:
            return response
        return response['Result']

    def get_block_count(self, is_full: bool = False) -> int or dict:
        response = self.get_block_height(is_full=True)
        response['Result'] += 1
        if is_full:
            return response
        return response['Result']

    def get_block_by_hash(self, block_hash: str, is_full: bool = False) -> int or dict:
        url = RestfulMethod.get_block_by_hash(self._url, block_hash)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_block_by_height(self, height: int, is_full: bool = False):
        url = RestfulMethod.get_block_by_height(self._url, height)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_balance(self, b58_address: str, is_full: bool = False):
        url = RestfulMethod.get_account_balance(self._url, b58_address)
        response = self.__get(url)
        response['Result'] = dict((k.upper(), int(v)) for k, v in response.get('Result', dict()).items())
        if is_full:
            return response
        return response['Result']

    def get_grant_ong(self, b58_address: str, is_full: bool = False):
        url = RestfulMethod.get_grant_ong(self._url, b58_address)
        response = self.__get(url)
        if is_full:
            return response
        return int(response['Result'])

    def get_allowance(self, asset: str, b58_from_address: str, b58_to_address: str, is_full: bool = False):
        url = RestfulMethod.get_allowance(self._url, asset, b58_from_address, b58_to_address)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_contract(self, contract_address: str, is_full: bool = False):
        url = RestfulMethod.get_contract(self._url, contract_address)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_contract_event_by_height(self, height: int, is_full: bool = False) -> List[dict]:
        url = RestfulMethod.get_contract_event_by_height(self._url, height)
        response = self.__get(url)
        if is_full:
            return response
        result = response['Result']
        if result == '':
            result = list()
        return result

    def get_contract_event_by_count(self, count: int, is_full: bool = False) -> List[dict]:
        return self.get_contract_event_by_height(count - 1, is_full)

    def get_contract_event_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_contract_event_by_tx_hash(self._url, tx_hash)
        response = self.__get(url)
        if is_full:
            return response
        result = response['Result']
        return dict() if result is None or len(result) == 0 else result

    def get_storage(self, hex_contract_address: str, hex_key: str, is_full: bool = False) -> str or dict:
        url = RestfulMethod.get_storage(self._url, hex_contract_address, hex_key)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_transaction_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_transaction(self._url, tx_hash)
        response = self.__get(url)
        if is_full:
            return response
        result = response['Result']
        return dict() if result is None else result

    def send_raw_transaction(self, tx: Transaction, is_full: bool = False):
        hex_tx_data = tx.serialize(is_hex=True)
        data = f'{{"Action":"sendrawtransaction", "Version":"1.0.0","Data":"{hex_tx_data}"}}'
        url = RestfulMethod.send_transaction(self._url)
        response = self.__post(url, data)
        if is_full:
            return response
        return response['Result']

    def send_raw_transaction_pre_exec(self, tx: Transaction, is_full: bool = False):
        hex_tx_data = tx.serialize(is_hex=True)
        data = f'{{"Action":"sendrawtransaction", "Version":"1.0.0","Data":"{hex_tx_data}"}}'
        url = RestfulMethod.send_transaction_pre_exec(self._url)
        response = self.__post(url, data)
        if is_full:
            return response
        return response['Result']

    def get_merkle_proof(self, tx_hash: str, is_full: bool = False):
        url = RestfulMethod.get_merkle_proof(self._url, tx_hash)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_memory_pool_tx_count(self, is_full: bool = False):
        url = RestfulMethod.get_mem_pool_tx_count(self._url)
        response = self.__get(url)
        if is_full:
            return response
        return response['Result']

    def get_memory_pool_tx_state(self, tx_hash: str, is_full: bool = False) -> List[dict] or dict:
        url = RestfulMethod.get_mem_pool_tx_state(self._url, tx_hash)
        response = self.__get(url)
        if response.get('Result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if is_full:
            return response
        return response['Result']['State']

    def send_neo_vm_tx_pre_exec(self, contract_address: Union[str, bytes, bytearray],
                                func: Union[AbiFunction, InvokeFunction], signer: Account = None,
                                is_full: bool = False):
        contract_address = ensure_bytearray_contract_address(contract_address)
        tx = NeoVm.make_invoke_transaction(contract_address, func)
        if signer is not None:
            tx.sign_transaction(signer)
        return self.send_raw_transaction_pre_exec(tx, is_full)

    def send_neo_vm_transaction(self, contract_address: str or bytes or bytearray, signer: Account or None,
                                payer: Account or None, gas_limit: int, gas_price: int,
                                func: AbiFunction or InvokeFunction, is_full: bool = False):
        if isinstance(func, AbiFunction):
            params = BuildParams.serialize_abi_function(func)
        elif isinstance(func, InvokeFunction):
            params = func.create_invoke_code()
        else:
            raise SDKException(ErrorCode.other_error('the type of func is error.'))
        contract_address = ensure_bytearray_contract_address(contract_address)
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        if payer is None:
            raise SDKException(ErrorCode.param_err('payer account is None.'))
        tx = Transaction(0, 0xd1, gas_price, gas_limit, payer.get_address_bytes(), params)
        tx.sign_transaction(payer)
        if isinstance(signer, Account) and signer.get_address_base58() != payer.get_address_base58():
            tx.add_sign_transaction(signer)
        return self.send_raw_transaction(tx, is_full)
