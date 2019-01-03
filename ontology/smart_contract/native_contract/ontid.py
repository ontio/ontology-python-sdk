#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import json

from time import time

from ontology.vm import build_vm
from ontology.common.define import *
from ontology.crypto.curve import Curve
from ontology.common.address import Address
from ontology.crypto.key_type import KeyType
from ontology.account.account import Account
from ontology.wallet.identity import Identity
from ontology.core.transaction import Transaction
from ontology.io.binary_reader import BinaryReader
from ontology.exception.error_code import ErrorCode
from ontology.io.memory_stream import StreamManager
from ontology.exception.exception import SDKException


class OntId(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__version = b'\x00'
        self.__contract_address = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03'

    @staticmethod
    def parse_pub_keys(ont_id: str, raw_pub_keys: str or bytes) -> list:
        if isinstance(raw_pub_keys, str):
            stream = StreamManager.GetStream(bytearray.fromhex(raw_pub_keys))
        elif isinstance(raw_pub_keys, bytes):
            stream = StreamManager.GetStream(raw_pub_keys)
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
                assert e.args[0] == 10001
                break
        return pub_keys

    @staticmethod
    def parse_attributes(serialized_attributes: str or bytes):
        if len(serialized_attributes) == 0:
            return list()
        if isinstance(serialized_attributes, str):
            stream = StreamManager.GetStream(bytearray.fromhex(serialized_attributes))
        elif isinstance(serialized_attributes, bytes):
            stream = StreamManager.GetStream(serialized_attributes)
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
                assert e.args[0] == 10001
                break
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
            stream = StreamManager.GetStream(bytearray.fromhex(serialized_ddo))
        elif isinstance(serialized_ddo, bytes):
            stream = StreamManager.GetStream(serialized_ddo)
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

    def get_public_keys(self, ont_id: str):
        if not ont_id.startswith(DID_ONT):
            raise SDKException(ErrorCode.invalid_ont_id_format(ont_id))
        args = dict(ontid=ont_id.encode('utf-8'))
        invoke_code = build_vm.build_native_invoke_code(self.__contract_address, self.__version, 'getPublicKeys', args)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, None, invoke_code, bytearray(), [])
        response = self.__sdk.get_network().send_raw_transaction_pre_exec(tx)
        pub_keys = OntId.parse_pub_keys(ont_id, response['Result'])
        return pub_keys

    def get_ddo(self, ont_id: str) -> dict:
        """
        This interface is used to get a DDO object in the from of dict.

        :param ont_id: the unique ID for identity.
        :return: a description object of ONT ID in the from of dict.
        """
        args = dict(ontid=ont_id.encode('utf-8'))
        invoke_code = build_vm.build_native_invoke_code(self.__contract_address, self.__version, 'getDDO', args)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, None, invoke_code, bytearray(), [])
        response = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        ddo = OntId.parse_ddo(ont_id, response['Result'])
        return ddo

    def get_merkle_proof(self, tx_hash: str):
        if not isinstance(tx_hash, str):
            raise SDKException(ErrorCode.other_error('Invalid TxHash type.'))
        if len(tx_hash) != 64:
            raise SDKException(ErrorCode.other_error('Invalid TxHash.'))
        network = self.__sdk.get_network()
        proof = network.get_merkle_proof(tx_hash)
        height = network.get_block_height_by_tx_hash(tx_hash)
        try:
            merkle_root = proof['TransactionsRoot']
        except KeyError:
            raise SDKException(ErrorCode.other_error('Invalid TxHash')) from None
        merkle_proof = dict(Type='MerkleProof', TxHash=tx_hash, BlockHeight=height, MerkleRoot=merkle_root)
        print(json.dumps(proof, indent=4))

    def new_add_public_key_transaction(self, ont_id: str, hex_public_key_or_recovery: str, hex_new_public_key: str,
                                       payer: str, gas_limit: int, gas_price: int):
        """
        This interface is used to send a Transaction object which is used to add public key.

        :param ont_id: ontid.
        :param hex_public_key_or_recovery: the old hexadecimal public key in the form of string.
        :param hex_new_public_key: the new hexadecimal public key in the form of string.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which is used to add public key.
        """
        contract_address = ONT_ID_CONTRACT_ADDRESS
        args = {"ontid": ont_id.encode(), "pubkey": bytearray.fromhex(hex_new_public_key),
                "pubkey_or_recovery": bytearray.fromhex(hex_public_key_or_recovery)}
        invoke_code = build_vm.build_native_invoke_code(contract_address, self.__version, 'addKey', args)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, Address.b58decode(payer).to_bytes(),
                         invoke_code, bytearray(), [])
        return tx

    def add_public_key(self, identity: Identity, password: str, hex_new_public_key: str,
                       payer: Account, gas_limit: int, gas_price: int):
        """
        This interface is used to send a Transaction object which is used to add public key.

        :param identity: an Identity object.
        :param password: a password which is used to decrypt the encrypted private key.
        :param hex_new_public_key: the new hexadecimal public key in the form of string.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return:  a hexadecimal transaction hash value.
        """
        ont_id = identity.ont_id.encode('utf-8')
        hex_public_key = identity.controls[0].public_key
        args = dict(ontid=ont_id, pubkey=bytearray.fromhex(hex_new_public_key),
                    pubkey_or_recovery=bytearray.fromhex(hex_public_key))
        invoke_code = build_vm.build_native_invoke_code(self.__contract_address, self.__version, 'addKey', args)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_bytes(),
                         invoke_code, bytearray(), [])
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        return self.__sdk.rpc.send_raw_transaction(tx)

    def new_registry_ont_id_transaction(self, ont_id: str, hex_public_key: str, b58_payer_address: str, gas_limit: int,
                                        gas_price: int):
        """
        This interface is used to generate a Transaction object which is used to register ONT ID.

        :param ont_id: OntId.
        :param hex_public_key: the hexadecimal public key in the form of string.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which is used to register ONT ID.
        """
        args = dict(ontid=ont_id.encode('utf-8'), pubkey=bytearray.fromhex(hex_public_key))
        invoke_code = build_vm.build_native_invoke_code(ONT_ID_CONTRACT_ADDRESS, self.__version, 'regIDWithPublicKey',
                                                        args)
        unix_time_now = int(time())
        bytes_payer_address = Address.b58decode(b58_payer_address).to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, bytes_payer_address, invoke_code, bytearray(),
                         [])
        return tx

    def send_registry_ont_id_transaction(self, identity: Identity, password: str, payer: Account, gas_limit: int,
                                         gas_price: int):
        """
        This interface is used to send a Transaction object which is used to registry ontid.

        :param identity: an Identity object.
        :param password: a password which is used to decrypt the encrypted private key.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a hexadecimal transaction hash value.
        """
        b58_payer_address = payer.get_address_base58()
        hex_pub_key = identity.controls[0].public_key
        tx = self.new_registry_ont_id_transaction(identity.ont_id, hex_pub_key, b58_payer_address, gas_limit, gas_price)
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        tx.sign_transaction(account)
        tx.add_sign_transaction(payer)
        return self.__sdk.rpc.send_raw_transaction(tx)

    def new_add_attribute_transaction(self, ont_id: str, hex_public_key: str, attribute_list: list,
                                      b58_payer_address: str,
                                      gas_limit: int, gas_price: int):
        """
        This interface is used to generate a Transaction object which is used to add attribute.

        :param ont_id: ontid.
        :param hex_public_key: the hexadecimal public key in the form of string.
        :param attribute_list: a list of attributes we want to add.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which is used to add attribute.
        """
        contract_address = ONT_ID_CONTRACT_ADDRESS
        args = {"ontid": ont_id.encode(), "length": len(attribute_list)}
        for i, v in enumerate(attribute_list):
            args["key" + str(i)] = bytes(attribute_list[i]["key"].encode())
            args["type" + str(i)] = bytes(attribute_list[i]["type"].encode())
            args["value" + str(i)] = bytes(attribute_list[i]["value"].encode())
        args["pubkey"] = bytearray.fromhex(hex_public_key)
        invoke_code = build_vm.build_native_invoke_code(contract_address, self.__version, "addAttributes", args)
        unix_time_now = int(time())
        array_payer_address = Address.b58decode(b58_payer_address).to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, array_payer_address, invoke_code, bytearray(),
                         [])
        return tx

    def send_add_attribute_transaction(self, identity: Identity, password: str, attribute_list: list, payer: Account,
                                       gas_limit: int, gas_price: int) -> str:
        """
        This interface is used to send a Transaction object which is used to add attribute.

        :param identity: an Identity object.
        :param password: a password which is used to decrypt the encrypted private key.
        :param attribute_list: a list of attributes we want to add.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a hexadecimal transaction hash value.
        """
        tx = self.new_add_attribute_transaction(identity.ont_id, identity.controls[0].public_key, attribute_list,
                                                payer.get_address_base58(), gas_limit, gas_price)
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        tx_hash = self.__sdk.rpc.send_raw_transaction(tx)
        return tx_hash

    def new_remove_attribute_transaction(self, ont_id: str, hex_public_key: str, path: str, b58_payer_address: str,
                                         gas_limit: int, gas_price: int):
        """
        This interface is used to generate a Transaction object which is used to remove attribute.

        :param ont_id: ontid.
        :param hex_public_key: the hexadecimal public key in the form of string.
        :param path: a string which is used to indicate which attribute we want to remove.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which is used to remove attribute.
        """
        contract_address = ONT_ID_CONTRACT_ADDRESS
        args = {"ontid": ont_id.encode(), "key": bytes(path.encode()), "pubkey": bytearray.fromhex(hex_public_key)}
        invoke_code = build_vm.build_native_invoke_code(contract_address, self.__version, "removeAttribute", args)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, Address.b58decode(b58_payer_address).to_bytes(),
                         invoke_code, bytearray(), [])
        return tx

    def send_remove_attribute_transaction(self, identity: Identity, password: str, path: str, payer: Account,
                                          gas_limit: int, gas_price: int):
        """
        This interface is used to send a Transaction object which is used to remove attribute.

        :param identity: an Identity object.
        :param password: a password which is used to decrypt the encrypted private key.
        :param path: a string which is used to indicate which attribute we want to remove.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a hexadecimal transaction hash value.
        """
        tx = self.new_remove_attribute_transaction(identity.ont_id, identity.controls[0].public_key, path,
                                                   payer.get_address_base58(), gas_limit, gas_price)
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        return self.__sdk.rpc.send_raw_transaction(tx)

    def send_add_public_key_by_recovery(self, ont_id: str, recovery: Account, hex_new_public_key: str, payer: Account,
                                        gas_limit: int, gas_price: int):
        """
        This interface is used to send a Transaction object which is used to add public key
        based on the recovery account.

        :param ont_id: ontid.
        :param recovery: an Account object which used a recovery account.
        :param hex_new_public_key: the new hexadecimal public key in the form of string.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a hexadecimal transaction hash value.
        """
        b58_payer_address = payer.get_address_base58()
        hex_recovery_address = recovery.get_address().to_hex_str()
        tx = self.new_add_public_key_transaction(ont_id, hex_recovery_address, hex_new_public_key, b58_payer_address,
                                                 gas_limit, gas_price)
        self.__sdk.sign_transaction(tx, recovery)
        self.__sdk.add_sign_transaction(tx, payer)
        tx_hash = self.__sdk.rpc.send_raw_transaction(tx)
        return tx_hash

    def new_remove_public_key_transaction(self, ont_id: str, hex_public_key_or_recovery: str,
                                          hex_remove_public_key: str,
                                          b58_payer_address: str, gas_limit: int, gas_price: int):
        """
        This interface is used to generate a Transaction object which is used to remove public key.

        :param ont_id: ontid.
        :param hex_public_key_or_recovery: the hexadecimal public key in the form of string.
        :param hex_remove_public_key: a hexadecimal public key string which will be removed.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which is used to remove public key.
        """
        contract_address = ONT_ID_CONTRACT_ADDRESS
        bytes_public_key_or_recovery = bytearray.fromhex(hex_public_key_or_recovery)
        bytes_remove_public_key = bytearray.fromhex(hex_remove_public_key)
        bytes_ont_id = ont_id.encode()
        args = {"ontid": bytes_ont_id, "pubkey": bytes_remove_public_key,
                "pubkey_or_recovery": bytes_public_key_or_recovery}
        invoke_code = build_vm.build_native_invoke_code(contract_address, self.__version, "removeKey", args)
        unix_time_now = int(time())
        bytes_payer_address = Address.b58decode(b58_payer_address).to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, bytes_payer_address, invoke_code, bytearray(),
                         [])
        return tx

    def send_remove_public_key_transaction(self, identity: Identity, password: str, hex_remove_public_key: str,
                                           payer: Account, gas_limit: int, gas_price: int):
        """
        This interface is used to send a Transaction object which is used to remove public key.

        :param identity: an Identity object.
        :param password: a password which is used to decrypt the encrypted private key.
        :param hex_remove_public_key: a hexadecimal public key string which will be removed.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a hexadecimal transaction hash value.
        """
        b58_payer_address = payer.get_address_base58()
        tx = self.new_remove_public_key_transaction(identity.ont_id, identity.controls[0].public_key,
                                                    hex_remove_public_key, b58_payer_address, gas_limit, gas_price)
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        return self.__sdk.rpc.send_raw_transaction(tx)

    def send_remove_public_key_transaction_by_recovery(self, ont_id: str, recovery: Account, hex_remove_public_key: str,
                                                       payer: Account,
                                                       gas_limit: int, gas_price: int):
        bytes_recovery_address = recovery.get_address().to_bytes()
        b58_payer_address = payer.get_address_base58()
        tx = self.new_remove_public_key_transaction(ont_id, bytes_recovery_address, hex_remove_public_key,
                                                    b58_payer_address, gas_limit, gas_price)
        self.__sdk.sign_transaction(tx, recovery)
        if recovery.get_address_base58() != payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        return self.__sdk.rpc.send_raw_transaction(tx)

    def new_add_recovery_transaction(self, ont_id: str, hex_public_key: str, b58_recovery_address: str,
                                     b58_payer_address: str, gas_limit: int, gas_price: int):
        """
        This interface is used to generate a Transaction object which is used to add the recovery.

        :param ont_id: ontid.
        :param hex_public_key: the hexadecimal public key in the form of string.
        :param b58_recovery_address: a base58 encode address which indicate who is the recovery.
        :param b58_payer_address: a base58 encode address which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return:
        """
        contract_address = ONT_ID_CONTRACT_ADDRESS
        bytes_recovery_address = Address.b58decode(b58_recovery_address).to_bytes()
        bytearray_public_key = bytearray.fromhex(hex_public_key)
        args = {"ontid": ont_id.encode(), "recovery": bytes_recovery_address, "pubkey": bytearray_public_key}
        invoke_code = build_vm.build_native_invoke_code(contract_address, self.__version, "addRecovery", args)
        unix_time_now = int(time())
        bytes_payer_address = Address.b58decode(b58_payer_address).to_bytes()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, bytes_payer_address, invoke_code, bytearray(),
                         [])
        return tx

    def send_add_recovery_transaction(self, identity: Identity, password: str, b58_recovery_address: str,
                                      payer: Account, gas_limit: int, gas_price: int):
        """
        This interface is used to send a Transaction object which is used to add the recovery.

        :param identity: an Identity object.
        :param password: a password which is used to decrypt the encrypted private key.
        :param b58_recovery_address: a base58 encode address which indicate who is the recovery.
        :param payer: an Account object which indicate who will pay for the transaction.
        :param gas_limit: an int value that indicate the gas limit.
        :param gas_price: an int value that indicate the gas price.
        :return: a Transaction object which is used to add the recovery.
        """
        b58_payer_address = payer.get_address_base58()
        tx = self.new_add_recovery_transaction(identity.ont_id, identity.controls[0].public_key, b58_recovery_address,
                                               b58_payer_address, gas_limit, gas_price)
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        tx_hash = self.__sdk.rpc.send_raw_transaction(tx)
        return tx_hash
