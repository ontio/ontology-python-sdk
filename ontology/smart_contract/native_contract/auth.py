from binascii import a2b_hex
from time import time

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.common.define import ZERO_ADDRESS
from ontology.exception.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.vm.build_vm import build_native_invoke_code
from ontology.wallet.identity import Identity


class Auth(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.contract_address = '0000000000000000000000000000000000000006'

    def send_transfer(self, admin_identity: Identity, password: str, key_no: int, contract_address: str,
                      new_admin_ont_id,
                      payer: Account, gas_limit: int, gas_price: int):
        if admin_identity is None or password is None or password == '' or contract_address is None or contract_address == '' or new_admin_ont_id is None or new_admin_ont_id == '' or payer is None:
            raise SDKException(ErrorCode.param_err("parameter should not be None"))
        if key_no < 0 or gas_limit < 0 or gas_price < 0:
            raise SDKException(ErrorCode.param_err('key_no or gas_limit or gas_price should not less than 0'))
        tx = self.make_transfer(contract_address, new_admin_ont_id, key_no, payer, gas_limit, gas_price)
        account = self.__sdk.wallet_manager.get_account_by_ont_id(admin_identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def make_transfer(self, contract_address: str, new_admin_ont_id: str, key_no: str, payer: Account, gas_limit: str,
                      gas_price: str):
        param = {"contract_address": a2b_hex(contract_address.encode()),
                 'new_admin_ont_id': new_admin_ont_id.encode('utf-8'), 'key_no': key_no}
        invoke_code = build_native_invoke_code(bytearray.fromhex(self.contract_address), bytes([0]), "transfer", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address_bytes(), invoke_code,
                         bytearray(), [])
        return tx

    def verify_token(self, identity: Identity, password: str, key_no: int, contract_address: str, function_name: str):
        contract_address = bytearray.fromhex(contract_address)
        param = {"contract_address": contract_address, "ontid": identity.ont_id.encode('utf-8'),
                 "function_name": function_name.encode('utf-8'), "key_no": key_no}
        invoke_code = build_native_invoke_code(bytearray.fromhex(self.contract_address), bytes([0]), "verifyToken",
                                               param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, Address(ZERO_ADDRESS).to_bytes(), invoke_code, bytearray(), [])
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return res

    def assign_funcs_to_role(self, admin_identity: Identity, password: str, key_no: int, contract_address: str,
                             role: str, function_name: list,
                             payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(contract_address)
        param = {"contract_address": contract_address, "ontid": admin_identity.ont_id.encode('utf-8'),
                 "role": role.encode('utf-8')}
        param['length'] = len(function_name)
        for i in range(len(function_name)):
            param['name' + str(i)] = function_name[i]
        param['key_no'] = key_no
        invoke_code = build_native_invoke_code(bytearray.fromhex(self.contract_address), bytes([0]),
                                               "assignFuncsToRole", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_bytes(), invoke_code,
                         bytearray(), [])
        account = self.__sdk.wallet_manager.get_account_by_ont_id(admin_identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        res = self.__sdk.rpc.send_raw_transaction(tx)
        return res

    def assign_ont_ids_to_role(self, admin_identity: Identity, password: str, key_no: int, contract_address: str,
                               role: str, ont_ids: list,
                               payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(contract_address)
        param = {"contract_address": contract_address, "ontid": admin_identity.ont_id.encode('utf-8'),
                 "role": role.encode('utf-8')}
        param['length'] = len(ont_ids)
        for i in range(len(ont_ids)):
            param['name' + str(i)] = ont_ids[i]
        param['key_no'] = key_no
        invoke_code = build_native_invoke_code(bytearray.fromhex(self.contract_address), bytes([0]),
                                               "assignOntIDsToRole", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_bytes(), invoke_code,
                         bytearray(), [])
        account = self.__sdk.wallet_manager.get_account_by_ont_id(admin_identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        res = self.__sdk.rpc.send_raw_transaction(tx)
        return res

    def delegate(self, identity: Identity, password: str, key_no: int, contract_address: str, to_ont_id: str, role: str,
                 period: int, level: int,
                 payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(contract_address)
        param = {"contract_address": contract_address, "ont_id": identity.ont_id.encode('utf-8'),
                 "to_ont_id": to_ont_id.encode('utf-8'),
                 "role": role.encode('utf-8'), "period": period, "level": level, "key_no": key_no}
        invoke_code = build_native_invoke_code(bytearray.fromhex(self.contract_address), bytes([0]), "delegate", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_bytes(), invoke_code,
                         bytearray(), [])
        account = self.__sdk.wallet_manager.get_account_by_ont_id(identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        res = self.__sdk.rpc.send_raw_transaction(tx)
        return res

    def withdraw(self, initiator_identity: Identity, password: str, key_no: int, contract_address: str, delegate: str,
                 role: str, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(contract_address)
        param = {"contract_address": contract_address, "ont_id": initiator_identity.ont_id.encode('utf-8'),
                 "delegate": delegate.encode('utf-8'),
                 "role": role.encode('utf-8'), "key_no": key_no}
        invoke_code = build_native_invoke_code(bytearray.fromhex(self.contract_address), bytes([0]), "withdraw", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_bytes(), invoke_code,
                         bytearray(), [])
        account = self.__sdk.wallet_manager.get_account_by_ont_id(initiator_identity.ont_id, password)
        self.__sdk.sign_transaction(tx, account)
        self.__sdk.add_sign_transaction(tx, payer)
        res = self.__sdk.rpc.send_raw_transaction(tx)
        return res
