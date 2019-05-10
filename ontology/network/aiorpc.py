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
import asyncio

from typing import List, Union

from aiohttp import client_exceptions
from aiohttp.client import ClientSession

from ontology.contract.neo.vm import NeoVm
from ontology.account.account import Account
from ontology.network.rpc import Rpc, RpcMethod
from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.transaction import ensure_bytearray_contract_address
from ontology.contract.neo.abi.abi_function import AbiFunction
from ontology.contract.neo.abi.build_params import BuildParams
from ontology.contract.neo.invoke_function import InvokeFunction


class AioRpc(Rpc):
    def __init__(self, url: str = '', qid: int = 0, session: ClientSession = None):
        super().__init__(url, qid)
        self._session = session

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session: ClientSession):
        if not isinstance(session, ClientSession):
            raise SDKException(ErrorCode.param_error)
        self._session = session

    async def __post(self, payload):
        header = {'Content-type': 'application/json'}
        try:
            if self._session is None:
                async with ClientSession() as session:
                    async with session.post(self._url, json=payload, headers=header, timeout=10) as response:
                        res = json.loads(await response.content.read(-1))
            else:
                async with self._session.post(self._url, json=payload, headers=header, timeout=10) as response:
                    res = json.loads(await response.content.read(-1))
            if res['error'] != 0:
                if res['result'] != '':
                    raise SDKException(ErrorCode.other_error(res['result']))
                else:
                    raise SDKException(ErrorCode.other_error(res['desc']))
        except (asyncio.TimeoutError, client_exceptions.ClientConnectorError):
            raise SDKException(ErrorCode.connect_timeout(self._url)) from None
        return res

    async def get_version(self, is_full: bool = False):
        """
        This interface is used to get the version information of the connected node in current network.

        Return:
            the version information of the connected node.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_VERSION)
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_connection_count(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the current number of connections for the node in current network.

        Return:
            the number of connections.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_NODE_COUNT)
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_gas_price(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the gas price in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_GAS_PRICE)
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']['gasprice']

    async def get_network_id(self, is_full: bool = False) -> int:
        """
        This interface is used to get the network id of current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_NETWORK_ID)
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_block_by_hash(self, block_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK, [block_hash, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_block_by_height(self, height: int, is_full: bool = False) -> dict:
        """
        This interface is used to get the block information by block height in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK, [height, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_block_count(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the decimal block number in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_COUNT)
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_block_height(self, is_full: bool = False) -> int or dict:
        """
        This interface is used to get the decimal block height in current network.
        """
        response = await self.get_block_count(is_full=True)
        response['result'] -= 1
        if is_full:
            return response
        return response['result']

    async def get_block_height_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_HEIGHT_BY_HASH, [tx_hash])
        response = await self.__post(payload)
        if response.get('result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if is_full:
            return response
        return response['result']

    async def get_block_count_by_tx_hash(self, tx_hash: str, is_full: bool = False):
        response = await self.get_block_height_by_tx_hash(tx_hash, is_full=True)
        response['result'] += 1
        if is_full:
            return response
        return response['result']

    async def get_current_block_hash(self, is_full: bool = False) -> str:
        """
        This interface is used to get the hexadecimal hash value of the highest block in current network.

        Return:
            the hexadecimal hash value of the highest block in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_CURRENT_BLOCK_HASH)
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_block_hash_by_height(self, height: int, is_full: bool = False) -> str:
        """
        This interface is used to get the hexadecimal hash value of specified block height in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BLOCK_HASH, [height, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_balance(self, b58_address: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the account balance of specified base58 encoded address in current network.

        :param b58_address: a base58 encoded account address.
        :param is_full:
        :return: the value of account balance in dictionary form.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_BALANCE, [b58_address, 1])
        response = await self.__post(payload)
        response['result'] = dict((k.upper(), int(v)) for k, v in response.get('result', dict()).items())
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def get_grant_ong(self, b58_address: str, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_GRANT_ONG, [b58_address])
        response = await self.__post(payload)
        if is_full:
            return response
        return int(response['result'])

    async def get_allowance(self, asset_name: str, from_address: str, to_address: str, is_full: bool = False) -> str:
        """
        This interface is used to get the the allowance
        from transfer-from account to transfer-to account in current network.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_ALLOWANCE, [asset_name, from_address, to_address])
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def get_storage(self, hex_contract_address: str, hex_key: str,
                          is_full: bool = False) -> str:
        """
        This interface is used to get the corresponding stored value
        based on hexadecimal contract address and stored key.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_STORAGE, [hex_contract_address, hex_key, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def get_contract_event_by_tx_hash(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [tx_hash, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def get_contract_event_by_height(self, height: int, is_full: bool = False) -> List[dict]:
        """
        This interface is used to get the corresponding smart contract event based on the height of block.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT_EVENT, [height, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        event_list = response['result']
        if event_list is None:
            event_list = list()
        return event_list

    async def get_contract_event_by_count(self, count: int, is_full: bool = False) -> List[dict]:
        event_list = await self.get_contract_event_by_height(count - 1, is_full)
        return event_list

    async def get_transaction_by_tx_hash(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding transaction information based on the specified hash value.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_TRANSACTION, [tx_hash, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def get_contract(self, hex_contract_address: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the information of smart contract based on the specified hexadecimal hash value.
        """
        if not isinstance(hex_contract_address, str):
            raise SDKException(ErrorCode.param_err('a hexadecimal contract address is required.'))
        if len(hex_contract_address) != 40:
            raise SDKException(ErrorCode.param_err('the length of the contract address should be 40 bytes.'))
        payload = self.generate_json_rpc_payload(RpcMethod.GET_SMART_CONTRACT, [hex_contract_address, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def get_merkle_proof(self, tx_hash: str, is_full: bool = False) -> dict:
        """
        This interface is used to get the corresponding merkle proof based on the specified hexadecimal hash value.
        """
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MERKLE_PROOF, [tx_hash, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def get_memory_pool_tx_count(self, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MEM_POOL_TX_COUNT)
        response = await self.__post(payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def get_memory_pool_tx_state(self, tx_hash: str, is_full: bool = False):
        payload = self.generate_json_rpc_payload(RpcMethod.GET_MEM_POOL_TX_STATE, [tx_hash])
        response = await self.__post(payload)
        if response.get('result', '') == '':
            raise SDKException(ErrorCode.invalid_tx_hash(tx_hash))
        if response.get('error', -1) != 0:
            raise SDKException(ErrorCode.other_error(response.get('result', '')))
        if is_full:
            return response
        return response['result']['State']

    async def send_raw_transaction(self, tx: Transaction, is_full: bool = False) -> str:
        """
        This interface is used to send the transaction into the network.
        """
        tx_data = tx.serialize(is_hex=True)
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data])
        response = await self.__post(payload)
        if is_full:
            return response
        result = response['result']
        return dict() if result is None else result

    async def send_raw_transaction_pre_exec(self, tx: Transaction, is_full: bool = False):
        """
        This interface is used to send the transaction that is prepare to execute.
        """
        tx_data = tx.serialize(is_hex=True)
        payload = self.generate_json_rpc_payload(RpcMethod.SEND_TRANSACTION, [tx_data, 1])
        response = await self.__post(payload)
        if is_full:
            return response
        return response['result']

    async def send_neo_vm_tx_pre_exec(self, contract_address: Union[str, bytes, bytearray],
                                      func: Union[AbiFunction, InvokeFunction],
                                      signer: Account = None,
                                      is_full: bool = False):
        contract_address = ensure_bytearray_contract_address(contract_address)
        tx = NeoVm.make_invoke_transaction(contract_address, func)
        if signer is not None:
            tx.sign_transaction(signer)
        return await self.send_raw_transaction_pre_exec(tx, is_full)

    async def send_neo_vm_transaction(self, contract_address: Union[str, bytes, bytearray],
                                      signer: Union[Account, None],
                                      payer: Union[Account, None],
                                      gas_price: int,
                                      gas_limit: int,
                                      func: Union[AbiFunction, InvokeFunction],
                                      is_full: bool = False):
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
        return await self.send_raw_transaction(tx, is_full)
