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

from typing import Union

from ontology.vm import build_vm
from ontology.crypto.curve import Curve
from ontology.common.address import Address
from ontology.crypto.key_type import KeyType
from ontology.account.account import Account
from ontology.utils.arguments import check_ont_id
from ontology.core.transaction import Transaction
from ontology.io.binary_reader import BinaryReader
from ontology.io.memory_stream import StreamManager
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.core.invoke_transaction import InvokeTransaction


class Attribute(object):
    def __init__(self, attrib_key: str = '', attrib_type: str = '', attrib_value: str = ''):
        self.__attribute_list = list()
        self.add_attribute(attrib_key, attrib_type, attrib_value)

    @property
    def attribute_list(self):
        return self.__attribute_list

    def add_attribute(self, attrib_key, attrib_type, attrib_value):
        if not isinstance(attrib_key, str) or not isinstance(attrib_type, str) or not isinstance(attrib_value, str):
            raise SDKException(ErrorCode.require_str_params)
        if len(attrib_key) != 0 and len(attrib_type) != 0 and len(attrib_value) != 0:
            attrib = dict(key=attrib_key, type=attrib_type, value=attrib_value)
            self.__attribute_list.append(attrib)

    def to_dict(self):
        attrib_dict = dict(length=len(self.__attribute_list))
        for index, attrib in enumerate(self.__attribute_list):
            attrib_dict[f'key{index}'] = attrib['key'].encode('utf-8')
            attrib_dict[f'type{index}'] = attrib['type'].encode('utf-8')
            attrib_dict[f'value{index}'] = attrib['value'].encode('utf-8')
        return attrib_dict


class OntId(object):
    def __init__(self, sdk=None):
        self._sdk = sdk
        self._version = b'\x00'
        self._contract_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03'

    @property
    def contract_address(self) -> str:
        return bytes.hex(self._contract_address[::-1])

    @staticmethod
    def parse_pub_keys(ont_id: str, raw_pub_keys: str or bytes) -> list:
        if isinstance(raw_pub_keys, str):
            stream = StreamManager.get_stream(bytearray.fromhex(raw_pub_keys))
        elif isinstance(raw_pub_keys, bytes):
            stream = StreamManager.get_stream(raw_pub_keys)
        else:
            raise SDKException(ErrorCode.params_type_error('bytes or str parameter is required.'))
        reader = BinaryReader(stream)
        pub_keys = list()
        while True:
            try:
                kid = f'{ont_id}#keys-{reader.read_int32()}'
                bytes_key = reader.read_var_bytes()
                hex_pub_key = bytes_key.hex()
                if len(bytes_key) == 33:
                    key_info = dict(PubKeyId=kid, Type=KeyType.ECDSA.name, Curve=Curve.P256.name, Value=hex_pub_key)
                else:
                    key_type = KeyType.from_label(bytes_key[0])
                    curve = Curve.from_label(bytes_key[1])
                    key_info = dict(PubKeyId=kid, Type=key_type, Curve=curve, Value=hex_pub_key)
                pub_keys.append(key_info)
            except SDKException as e:
                if e.args[0] != 10001:
                    raise e
                else:
                    break
        return pub_keys

    @staticmethod
    def parse_attributes(serialized_attributes: str or bytes):
        if len(serialized_attributes) == 0:
            return list()
        if isinstance(serialized_attributes, str):
            stream = StreamManager.get_stream(bytearray.fromhex(serialized_attributes))
        elif isinstance(serialized_attributes, bytes):
            stream = StreamManager.get_stream(serialized_attributes)
        else:
            raise SDKException(ErrorCode.params_type_error('bytes or str parameter is required.'))
        reader = BinaryReader(stream)
        attributes_list = []
        while True:
            try:
                attr_key = reader.read_var_bytes().decode('utf-8')
                attr_type = reader.read_var_bytes().decode('utf-8')
                attr_value = reader.read_var_bytes().decode('utf-8')
                attr = dict(Key=attr_key, Type=attr_type, Value=attr_value)
                attributes_list.append(attr)
            except SDKException as e:
                if 10000 < e.args[0] < 20000:
                    break
                else:
                    raise e
        return attributes_list

    @staticmethod
    def parse_ddo(ont_id: str, serialized_ddo: str or bytes) -> dict:
        """
        This interface is used to deserialize a hexadecimal string into a DDO object in the from of dict.

        :param ont_id: the unique ID for identity.
        :param serialized_ddo: an serialized description object of ONT ID in form of str or bytes.
        :return: a description object of ONT ID in the from of dict.
        """
        if len(serialized_ddo) == 0:
            return dict()
        if isinstance(serialized_ddo, str):
            stream = StreamManager.get_stream(bytearray.fromhex(serialized_ddo))
        elif isinstance(serialized_ddo, bytes):
            stream = StreamManager.get_stream(serialized_ddo)
        else:
            raise SDKException(ErrorCode.params_type_error('bytes or str parameter is required.'))
        reader = BinaryReader(stream)
        try:
            public_key_bytes = reader.read_var_bytes()
        except SDKException:
            public_key_bytes = b''
        try:
            attribute_bytes = reader.read_var_bytes()
        except SDKException:
            attribute_bytes = b''
        try:
            recovery_bytes = reader.read_var_bytes()
        except SDKException:
            recovery_bytes = b''
        if len(recovery_bytes) != 0:
            b58_recovery = Address(recovery_bytes).b58encode()
        else:
            b58_recovery = ''
        pub_keys = OntId.parse_pub_keys(ont_id, public_key_bytes)
        attribute_list = OntId.parse_attributes(attribute_bytes)
        ddo = dict(Owners=pub_keys, Attributes=attribute_list, Recovery=b58_recovery, OntId=ont_id)
        return ddo

    def _generate_transaction(self, method: str, args: dict, payer: Union[str, bytes, Address], gas_price: int,
                              gas_limit: int) -> InvokeTransaction:
        invoke_code = build_vm.build_native_invoke_code(self._contract_address, self._version, method, args)
        return InvokeTransaction(payer, gas_price, gas_limit, invoke_code)

    @check_ont_id
    def get_public_keys(self, ont_id: str):
        args = dict(ontid=ont_id.encode('utf-8'))
        invoke_code = build_vm.build_native_invoke_code(self._contract_address, self._version, 'getPublicKeys', args)
        tx = Transaction(0, 0xd1, 0, 0, b'', invoke_code)
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        pub_keys = OntId.parse_pub_keys(ont_id, response['Result'])
        return pub_keys

    @check_ont_id
    def get_ddo(self, ont_id: str) -> dict:
        """
        This interface is used to get a DDO object in the from of dict.

        :param ont_id: the unique ID for identity.
        :return: a description object of ONT ID in the from of dict.
        """
        args = dict(ontid=ont_id.encode('utf-8'))
        invoke_code = build_vm.build_native_invoke_code(self._contract_address, self._version, 'getDDO', args)
        tx = Transaction(0, 0xd1, 0, 0, b'', invoke_code)
        response = self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        ddo = OntId.parse_ddo(ont_id, response['Result'])
        return ddo

    @check_ont_id
    def registry_ont_id(self, ont_id: str, ctrl_acct: Account, payer: Account, gas_price: int, gas_limit: int):
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
        return self._sdk.default_network.send_raw_transaction(tx)

    @check_ont_id
    def add_public_key(self, ont_id: str, operator: Account, hex_new_public_key: str, payer: Account, gas_price: int,
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
        return self._sdk.default_network.send_raw_transaction(tx)

    @check_ont_id
    def revoke_public_key(self, ont_id: str, operator: Account, revoked_pub_key: str, payer: Account,
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
        return self._sdk.default_network.send_raw_transaction(tx)

    @check_ont_id
    def add_attribute(self, ont_id: str, ctrl_acct: Account, attributes: Attribute, payer: Account, gas_price: int,
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
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    @check_ont_id
    def remove_attribute(self, ont_id: str, operator: Account, attrib_key: str, payer: Account, gas_price: int,
                         gas_limit: int):
        """
        This interface is used to send a Transaction object which is used to remove attribute.
        """
        pub_key = operator.get_public_key_bytes()
        b58_payer_address = payer.get_address_base58()
        tx = self.new_remove_attribute_tx(ont_id, pub_key, attrib_key, b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(operator)
        tx.add_sign_transaction(payer)
        return self._sdk.default_network.send_raw_transaction(tx)

    @check_ont_id
    def add_recovery(self, ont_id: str, ctrl_acct: Account, b58_recovery_address: str, payer: Account, gas_price: int,
                     gas_limit: int):
        """
        This interface is used to send a Transaction object which is used to add the recovery.
        """
        b58_payer_address = payer.get_address_base58()
        pub_key = ctrl_acct.get_public_key_bytes()
        tx = self.new_add_recovery_tx(ont_id, pub_key, b58_recovery_address, b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(ctrl_acct)
        tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    @check_ont_id
    def change_recovery(self, ont_id: str, b58_new_recovery_address: str, recovery: Account, payer: Account,
                        gas_price: int, gas_limit: int):
        b58_payer_address = payer.get_address_base58()
        b58_recovery_address = recovery.get_address_base58()
        tx = self.new_change_recovery_tx(ont_id, b58_new_recovery_address, b58_recovery_address,
                                         b58_payer_address, gas_price, gas_limit)
        tx.sign_transaction(recovery)
        tx.add_sign_transaction(payer)
        tx_hash = self._sdk.default_network.send_raw_transaction(tx)
        return tx_hash

    @check_ont_id
    def verify_signature(self, ont_id: str, key_index: int, sign_acct: Account) -> bool:
        if key_index < 1:
            raise SDKException(ErrorCode.param_err('Invalid key index.'))
        tx = self.new_verify_signature_tx(ont_id, key_index)
        tx.sign_transaction(sign_acct)
        try:
            self._sdk.default_network.send_raw_transaction_pre_exec(tx)
        except SDKException as e:
            if 'verify signature failed' in e.args[1]:
                return False
            else:
                raise e
        return True

    @check_ont_id
    def new_verify_signature_tx(self, ont_id: str, key_index: int) -> InvokeTransaction:
        if key_index < 1:
            raise SDKException(ErrorCode.param_err('Invalid key index.'))
        args = dict(ontid=ont_id.encode('utf-8'), index=key_index)
        tx = self._generate_transaction('verifySignature', args, b'', 0, 0)
        return tx

    @check_ont_id
    def new_change_recovery_tx(self, ont_id: str, b58_new_recovery_address: str, b58_recovery_address: str,
                               payer: Union[str, bytes, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        bytes_new_recovery = Address.b58decode(b58_new_recovery_address).to_bytes()
        bytes_recovery = Address.b58decode(b58_recovery_address).to_bytes()
        args = dict(ontid=ont_id.encode('utf-8'), new_recovery=bytes_new_recovery, recovery=bytes_recovery)
        tx = self._generate_transaction('changeRecovery', args, payer, gas_price, gas_limit)
        return tx

    @check_ont_id
    def new_registry_ont_id_tx(self, ont_id: str, pub_key: str or bytes, payer: Union[str, bytes, Address],
                               gas_price: int, gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a Transaction object which is used to register ONT ID.
        """
        if isinstance(pub_key, str):
            bytes_ctrl_pub_key = bytes.fromhex(pub_key)
        elif isinstance(pub_key, bytes):
            bytes_ctrl_pub_key = pub_key
        else:
            raise SDKException(ErrorCode.param_err('a bytes or str type of public key is required.'))
        args = dict(ontid=ont_id.encode('utf-8'), ctrl_pk=bytes_ctrl_pub_key)
        tx = self._generate_transaction('regIDWithPublicKey', args, payer, gas_price, gas_limit)
        return tx

    @check_ont_id
    def new_add_public_key_tx(self, ont_id: str, bytes_operator: bytes, new_pub_key: str or bytes,
                              payer: Union[str, bytes, Address], gas_price: int, gas_limit: int,
                              is_recovery: bool = False) -> InvokeTransaction:
        """
        This interface is used to send a Transaction object which is used to add public key.
        """
        if isinstance(new_pub_key, str):
            bytes_new_pub_key = bytes.fromhex(new_pub_key)
        elif isinstance(new_pub_key, bytes):
            bytes_new_pub_key = new_pub_key
        else:
            raise SDKException(ErrorCode.params_type_error('a bytes or str type of public key is required.'))
        if is_recovery:
            args = dict(ontid=ont_id, pk=bytes_new_pub_key, operator=bytes_operator)
        else:
            args = dict(ontid=ont_id, pk=bytes_new_pub_key, operator=bytes_operator)
        tx = self._generate_transaction('addKey', args, payer, gas_price, gas_limit)
        return tx

    @check_ont_id
    def new_revoke_public_key_tx(self, ont_id: str, bytes_operator: bytes, revoked_pub_key: str or bytes,
                                 payer: Union[str, bytes, Address], gas_price: int,
                                 gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a Transaction object which is used to remove public key.
        """
        if isinstance(revoked_pub_key, str):
            bytes_revoked_pub_key = bytes.fromhex(revoked_pub_key)
        elif isinstance(revoked_pub_key, bytes):
            bytes_revoked_pub_key = revoked_pub_key
        else:
            raise SDKException(ErrorCode.params_type_error('a bytes or str type of public key is required.'))
        bytes_ont_id = ont_id.encode('utf-8')
        args = dict(ontid=bytes_ont_id, pk=bytes_revoked_pub_key, operator=bytes_operator)
        tx = self._generate_transaction('removeKey', args, payer, gas_price, gas_limit)
        return tx

    @check_ont_id
    def new_add_attribute_tx(self, ont_id: str, pub_key: str or bytes, attributes: Attribute,
                             payer: Union[str, bytes, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a Transaction object which is used to add attribute.
        """
        if isinstance(pub_key, str):
            bytes_pub_key = bytes.fromhex(pub_key)
        elif isinstance(pub_key, bytes):
            bytes_pub_key = pub_key
        else:
            raise SDKException(ErrorCode.params_type_error('a bytes or str type of public key is required.'))
        bytes_ont_id = ont_id.encode('utf-8')
        args = dict(ontid=bytes_ont_id)
        attrib_dict = attributes.to_dict()
        args = dict(**args, **attrib_dict)
        args['pubkey'] = bytes_pub_key
        tx = self._generate_transaction('addAttributes', args, payer, gas_price, gas_limit)
        return tx

    @check_ont_id
    def new_remove_attribute_tx(self, ont_id: str, pub_key: str or bytes, attrib_key: str,
                                payer: Union[str, bytes, Address], gas_price: int, gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a Transaction object which is used to remove attribute.
        """
        if isinstance(pub_key, str):
            bytes_pub_key = bytes.fromhex(pub_key)
        elif isinstance(pub_key, bytes):
            bytes_pub_key = pub_key
        else:
            raise SDKException(ErrorCode.params_type_error('a bytes or str type of public key is required.'))
        args = dict(ontid=ont_id.encode('utf-8'), attrib_key=attrib_key.encode('utf-8'), pk=bytes_pub_key)
        tx = self._generate_transaction('removeAttribute', args, payer, gas_price, gas_limit)
        return tx

    @check_ont_id
    def new_add_recovery_tx(self, ont_id: str, pub_key: str or bytes, b58_recovery_address: str,
                            payer: Union[str, bytes, Address], gas_price: int,
                            gas_limit: int) -> InvokeTransaction:
        """
        This interface is used to generate a Transaction object which is used to add the recovery.
        """
        if isinstance(pub_key, str):
            bytes_pub_key = bytes.fromhex(pub_key)
        elif isinstance(pub_key, bytes):
            bytes_pub_key = pub_key
        else:
            raise SDKException(ErrorCode.params_type_error('a bytes or str type of public key is required.'))
        bytes_recovery_address = Address.b58decode(b58_recovery_address).to_bytes()
        args = dict(ontid=ont_id.encode('utf-8'), recovery=bytes_recovery_address, pk=bytes_pub_key)
        tx = self._generate_transaction('addRecovery', args, payer, gas_price, gas_limit)
        return tx
