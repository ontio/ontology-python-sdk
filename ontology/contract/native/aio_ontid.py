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
from ontology.account.account import Account
from ontology.contract.native.ontid import OntId, Attribute
from ontology.core.transaction import Transaction
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.utils.arguments import check_ont_id
from ontology.vm import build_vm


class AioOntId(OntId):
    def __init__(self, sdk):
        super().__init__(sdk)

    @check_ont_id
    async def get_public_keys(self, ont_id: str):
        args = dict(ontid=ont_id.encode('utf-8'))
        invoke_code = build_vm.build_native_invoke_code(self._contract_address, self._version, 'getPublicKeys', args)
        tx = Transaction(0, 0xd1, 0, 0, b'', invoke_code)
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        pub_keys = OntId.parse_pub_keys(ont_id, response['Result'])
        return pub_keys

    @check_ont_id
    async def get_ddo(self, ont_id: str) -> dict:
        """
        This interface is used to get a DDO object in the from of dict.

        :param ont_id: the unique ID for identity.
        :return: a description object of ONT ID in the from of dict.
        """
        args = dict(ontid=ont_id.encode('utf-8'))
        invoke_code = build_vm.build_native_invoke_code(self._contract_address, self._version, 'getDDO', args)
        tx = Transaction(0, 0xd1, 0, 0, b'', invoke_code)
        response = await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        ddo = OntId.parse_ddo(ont_id, response['Result'])
        return ddo

    @check_ont_id
    async def registry_ont_id(self, ont_id: str, ctrl_acct: Account, payer: Account, gas_price: int, gas_limit: int):
        """
        This interface is used to send a Transaction object which is used to registry ontid.
        """
        if not isinstance(ctrl_acct, Account) or not isinstance(payer, Account):
            raise SDKException(ErrorCode.require_acct_params)
        b58_payer_address = payer.get_address_base58()
        bytes_ctrl_pub_key = ctrl_acct.get_public_key_bytes()
        tx = self.new_registry_ont_id_tx(ont_id, bytes_ctrl_pub_key, b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(ctrl_acct)
        tx.add_sign_transaction(payer)
        return await self._sdk.default_aio_network.send_raw_transaction(tx)

    @check_ont_id
    async def add_public_key(self, ont_id: str, operator: Account, hex_new_public_key: str, payer: Account,
                             gas_price: int,
                             gas_limit: int, is_recovery: bool = False):
        """
        This interface is used to send a Transaction object which is used to add public key.
        """
        if not isinstance(operator, Account) or not isinstance(payer, Account):
            raise SDKException(ErrorCode.require_acct_params)
        if is_recovery:
            bytes_operator = operator.get_address_bytes()
        else:
            bytes_operator = operator.get_public_key_bytes()
        b58_payer_address = payer.get_address_base58()
        tx = self.new_add_public_key_tx(ont_id, bytes_operator, hex_new_public_key, b58_payer_address, gas_price,
                                        gas_limit, is_recovery)
        tx.sign_transaction(operator)
        tx.add_sign_transaction(payer)
        return await self._sdk.default_aio_network.send_raw_transaction(tx)

    @check_ont_id
    async def revoke_public_key(self, ont_id: str, operator: Account, revoked_pub_key: str, payer: Account,
                                gas_limit: int, gas_price: int, is_recovery: bool = False):
        """
        This interface is used to send a Transaction object which is used to remove public key.
        """
        if not isinstance(operator, Account) or not isinstance(payer, Account):
            raise SDKException(ErrorCode.require_acct_params)
        b58_payer_address = payer.get_address_base58()
        if is_recovery:
            bytes_operator = operator.get_address_bytes()
        else:
            bytes_operator = operator.get_public_key_bytes()
        tx = self.new_revoke_public_key_tx(ont_id, bytes_operator, revoked_pub_key, b58_payer_address, gas_limit,
                                           gas_price)
        tx.sign_transaction(operator)
        tx.add_sign_transaction(payer)
        return await self._sdk.default_aio_network.send_raw_transaction(tx)

    @check_ont_id
    async def add_attribute(self, ont_id: str, ctrl_acct: Account, attributes: Attribute, payer: Account,
                            gas_price: int,
                            gas_limit: int) -> str:
        """
        This interface is used to send a Transaction object which is used to add attribute.
        """
        if not isinstance(ctrl_acct, Account) or not isinstance(payer, Account):
            raise SDKException(ErrorCode.require_acct_params)
        pub_key = ctrl_acct.get_public_key_bytes()
        b58_payer_address = payer.get_address_base58()
        tx = self.new_add_attribute_tx(ont_id, pub_key, attributes, b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(ctrl_acct)
        tx.add_sign_transaction(payer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    @check_ont_id
    async def remove_attribute(self, ont_id: str, operator: Account, attrib_key: str, payer: Account, gas_price: int,
                               gas_limit: int):
        """
        This interface is used to send a Transaction object which is used to remove attribute.
        """
        pub_key = operator.get_public_key_bytes()
        b58_payer_address = payer.get_address_base58()
        tx = self.new_remove_attribute_tx(ont_id, pub_key, attrib_key, b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(operator)
        tx.add_sign_transaction(payer)
        return await self._sdk.default_aio_network.send_raw_transaction(tx)

    @check_ont_id
    async def add_recovery(self, ont_id: str, ctrl_acct: Account, b58_recovery_address: str, payer: Account,
                           gas_price: int, gas_limit: int):
        """
        This interface is used to send a Transaction object which is used to add the recovery.
        """
        b58_payer_address = payer.get_address_base58()
        pub_key = ctrl_acct.get_public_key_bytes()
        tx = self.new_add_recovery_tx(ont_id, pub_key, b58_recovery_address, b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(ctrl_acct)
        tx.add_sign_transaction(payer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    @check_ont_id
    async def change_recovery(self, ont_id: str, b58_new_recovery_address: str, recovery: Account, payer: Account,
                              gas_price: int, gas_limit: int):
        b58_payer_address = payer.get_address_base58()
        b58_recovery_address = recovery.get_address_base58()
        tx = self.new_change_recovery_tx(ont_id, b58_new_recovery_address, b58_recovery_address,
                                         b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(recovery)
        tx.add_sign_transaction(payer)
        tx_hash = await self._sdk.default_aio_network.send_raw_transaction(tx)
        return tx_hash

    @check_ont_id
    async def verify_signature(self, ont_id: str, key_index: int, sign_acct: Account) -> bool:
        if key_index < 1:
            raise SDKException(ErrorCode.param_err('Invalid key index.'))
        tx = self.new_verify_signature_tx(ont_id, key_index)
        tx.sign_transaction(sign_acct)
        try:
            await self._sdk.default_aio_network.send_raw_transaction_pre_exec(tx)
        except SDKException as e:
            if 'verify signature failed' in e.args[1]:
                return False
            else:
                raise e
        return True
