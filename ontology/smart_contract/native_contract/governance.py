#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from time import time
from binascii import a2b_hex

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from ontology.vm.build_vm import build_native_invoke_code
from ontology.wallet.identity import Identity


class Governance(object):

    CONTRACT_ADDRESS = "0000000000000000000000000000000000000007"
    AUTHORIZE_INFO_POOL = "voteInfoPool"
    PEER_ATTRIBUTES = "peerAttributes"
    SPLIT_FEE_ADDRESS = "splitFeeAddress"
    GOVERNANCE_VIEW = "governanceView"
    PEER_POOL = "peerPool"
    TOTAL_STAKE = "totalStake"
    UNBOUND_GENERATION_AMOUNT = [5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    UNBOUND_TIME_INTERVAL = 31536000
    ONT_TOTAL_SUPPLY = 1000000000

    def __init__(self, sdk):
        self.__sdk = sdk

    def register_candidate(self, account: Account, peer_pubkey: str, init_pos: int, identity: Identity, password: str, key_no: int,
                          payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"peer_pubkey": peer_pubkey, "address": account.get_address().to_array(), "init_pos": init_pos, "ontid": identity.ont_id.encode(), "key_no": key_no}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "registerCandidate", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [],
                           bytearray())
        self.__sdk.sign_transaction(tx, account)
        ontid_acc = self.__sdk.wallet_manager.get_account(identity.ont_id, password)
        self.__sdk.add_sign_transaction(tx, ontid_acc)
        if account.get_address_base58() is not payer:
            self.__sdk.add_sign_transaction(tx, payer)
        res = self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def unregister_candidate(self, account: Account, peer_pubkey: str, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"peer_pubkey":peer_pubkey, "address": account.get_address().to_array()}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "unRegisterCandidate", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def withdraw_ong(self, account: Account, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"address": account.get_address().to_array()}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "withdrawOng", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def withdraw_fee(self, account: Account, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"address": account.get_address().to_array()}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "withdrawFee", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def authorize_for_peer(self, account: Account, peer_publickeys: list, pos_lists: list, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        if len(peer_publickeys) != len(pos_lists):
            raise Exception("the length of peer_publickeys should equal the length of pos_lists")
        param = {"address": account.get_address().to_array(), "publickeys_length": len(peer_publickeys)}
        for i in range(len(peer_publickeys)):
            param["publickey" + str(i)] = peer_publickeys[i]
        param["pos_lists_length"] = len(pos_lists)
        for i in range(len(pos_lists)):
            param["pos_lists" + str(i)] = pos_lists[i]
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "authorizeForPeer", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        res = self.__sdk.rpc.send_raw_transaction(tx)
        print(res)
        return tx.hash256_explorer()

    def unauthorize_for_peer(self, account: Account, peer_publickeys: [], pos_lists: [], payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        if len(peer_publickeys) != len(pos_lists):
            raise Exception("the length of peer_publickeys should equal the length of pos_lists")
        param = {"address": account.get_address().to_array(), "publickeys_length": len(peer_publickeys)}
        for i in range(len(peer_publickeys)):
            param["publickey" + str(i)] = peer_publickeys[i]
        param["pos_lists_length"] = len(pos_lists)
        for i in range(len(pos_lists)):
            param["pos_lists" + str(i)] = pos_lists[i]
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "unAuthorizeForPeer", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def withdraw(self, account: Account, peer_publickeys: list, withdraw_list: list, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        if len(peer_publickeys) != len(withdraw_list):
            raise Exception("the length of peer_publickeys should equal the length of pos_lists")
        param = {"address": account.get_address().to_array(), "publickeys_length": len(peer_publickeys)}
        for i in range(len(peer_publickeys)):
            param["publickey" + str(i)] = peer_publickeys[i]
        param["pos_lists_length"] = len(withdraw_list)
        for i in range(len(withdraw_list)):
            param["pos_lists" + str(i)] = withdraw_list[i]
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "withdraw", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def quit_node(self, account: Account, peer_publickey: str, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"peer_publickey": peer_publickey, "address": account.get_address().to_array()}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "quitNode", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def change_max_authorization(self, account: Account, peer_publickey: str, max_authorize: int, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"peer_publickey": peer_publickey, "address": account.get_address().to_array(), "maxAuthorize": max_authorize}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "changeMaxAuthorization", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def add_init_pos(self, account: Account, peer_publickey: str, pos: int, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"peer_publickey": peer_publickey, "address": account.get_address().to_array(), "pos": pos}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "addInitPos", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def reduce_init_pos(self, account: Account, peer_publickey: str, pos: int, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"peer_publickey": peer_publickey, "address": account.get_address().to_array(), "pos": pos}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "reduceInitPos", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def set_peer_cost(self, account: Account, peer_publickey: str, peer_cost: int, payer: Account, gas_limit: int, gas_price: int):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        param = {"peer_publickey": peer_publickey, "address": account.get_address().to_array(), "peer_cost": peer_cost}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "setPeerCost", param)
        unix_time_now = int(time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer.get_address().to_array(), invoke_code, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, account)
        if payer is not None and account.get_address_base58() is not payer.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer)
        self.__sdk.rpc.send_raw_transaction(tx)
        return tx.hash256_explorer()

    def get_peer_unbind_ong(self, address: str):
        block0 = self.__sdk.rpc.get_block_by_height(0)
        timestamp0 = block0['Header']['Timestamp']
        current_height = self.__sdk.rpc.get_block_count()
        block = self.__sdk.rpc.get_block_by_height(current_height - 1)
        timestamp = block['Header']['Timestamp'] - timestamp0
        total_stake = self.get_total_stake(address)
        return self.calc_unbind_ong(total_stake.stake, total_stake.time_offset, timestamp)

    def calc_unbind_ong(self, balance: int, start_offset: int, end_offset: int):
        amount = 0
        if start_offset >= end_offset:
            return 0
        unbound_deadline = self.unbound_deadline()
        if start_offset < unbound_deadline:
            ustart = start_offset / self.UNBOUND_TIME_INTERVAL
            istart = start_offset % self.UNBOUND_TIME_INTERVAL
            if end_offset >= unbound_deadline:
                end_offset = unbound_deadline
            uend = end_offset / self.UNBOUND_TIME_INTERVAL
            iend = end_offset % self.UNBOUND_TIME_INTERVAL
            while ustart < int(uend):
                amount = (self.UNBOUND_TIME_INTERVAL - istart) * self.UNBOUND_GENERATION_AMOUNT[int(ustart)]
                ustart += 1
                istart = 0
            amount += (iend - istart) * self.UNBOUND_GENERATION_AMOUNT[int(ustart)]
        return amount * balance

    def unbound_deadline(self):
        count = 0
        for i in range(len(self.UNBOUND_GENERATION_AMOUNT)):
            count += self.UNBOUND_GENERATION_AMOUNT[i]
        count *= self.UNBOUND_TIME_INTERVAL
        num_interval = len(self.UNBOUND_GENERATION_AMOUNT)
        return self.UNBOUND_TIME_INTERVAL * num_interval - (count - self.ONT_TOTAL_SUPPLY)

    def get_total_stake(self, address: str):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        contract_address.reverse()
        total_bytes = self.TOTAL_STAKE.encode('utf-8')
        address_bytes = Address.b58decode(address).to_array()
        key = total_bytes + address_bytes
        res = self.__sdk.rpc.get_storage(contract_address.hex(), key.hex())
        stream = StreamManager.GetStream(bytearray.fromhex(res))
        reader = BinaryReader(stream)
        total_stake = TotalStake()
        total_stake.deserialize(reader)
        stream.close()
        return total_stake

    def get_peer_attributes(self, peer_pubkey: str):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        contract_address.reverse()
        peer_attributes = self.PEER_ATTRIBUTES.encode('utf-8')
        peer_pubkey_bytes = a2b_hex(peer_pubkey.encode())
        key = peer_attributes + peer_pubkey_bytes
        res = self.__sdk.rpc.get_storage(contract_address.hex(), key.hex())
        if res is None or res == '':
            return None
        peer_attributes = PeerAttributes()
        stream = StreamManager.GetStream(bytearray.fromhex(res))
        reader = BinaryReader(stream)
        peer_attributes.deserialize(reader)
        stream.close()
        return peer_attributes.to_json()

    def get_split_fee_address(self, address: str):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        contract_address.reverse()
        split_fee_address_bytes = self.SPLIT_FEE_ADDRESS.encode()
        address_bytes = Address.b58decode(address).to_array()
        key = split_fee_address_bytes + address_bytes
        res = self.__sdk.rpc.get_storage(contract_address.hex(), key.hex())
        if res is None or res == '':
            return None
        split_fee_address = SplitFeeAddress()
        stream = StreamManager.GetStream(bytearray.fromhex(res))
        reader = BinaryReader(stream)
        split_fee_address.deserialize(reader)
        stream.close()
        return split_fee_address.to_json()

    def get_peer_info(self, peer_pubkey: str):
        return self.__get_peer_pool_map(peer_pubkey)

    def get_peer_info_all(self):
        return self.__get_peer_pool_map()

    def __get_peer_pool_map(self, peer_pubkey=None):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        contract_address.reverse()
        view = self.__sdk.rpc.get_storage(contract_address.hex(), self.GOVERNANCE_VIEW.encode().hex())
        stream = StreamManager.GetStream(bytearray.fromhex(view))
        reader = BinaryReader(stream)
        governance_view = GovernanceView()
        governance_view.deserialize(reader)
        stream.close()
        stream2 = StreamManager.GetStream()
        writer = BinaryWriter(stream2)
        writer.write_int32(governance_view.view)
        view_bytes = stream2.ToArray()
        peer_pool_bytes = self.PEER_POOL.encode('utf-8')
        key_bytes = peer_pool_bytes + a2b_hex(view_bytes)
        value = self.__sdk.rpc.get_storage(contract_address.hex(), key_bytes.hex())
        stream3 = StreamManager.GetStream(bytearray.fromhex(value))
        reader2 = BinaryReader(stream3)
        length = reader2.read_int32()
        peer_pool_map = {}
        for i in range(length):
            item = PeerPoolItem()
            item.deserialize(reader2)
            peer_pool_map[item.peer_pubkey] = item.to_json()
        if peer_pubkey is not None:
            if peer_pubkey not in peer_pool_map:
                return None
            return peer_pool_map[peer_pubkey]
        return peer_pool_map

    def get_authorize_info(self, peer_pubkey: str, addr: Address):
        contract_address = bytearray.fromhex(self.CONTRACT_ADDRESS)
        contract_address.reverse()
        peer_pubkey_prefix = bytearray.fromhex(peer_pubkey)
        address_bytes = addr.to_array()
        authorize_info_pool = self.AUTHORIZE_INFO_POOL.encode()
        key = authorize_info_pool + peer_pubkey_prefix + address_bytes
        res = self.__sdk.rpc.get_storage(contract_address.hex(), key.hex())
        if res is None or res == '':
            return None
        stream = StreamManager.GetStream(bytearray.fromhex(res))
        reader = BinaryReader(stream)
        authorize_info = AuthorizeInfo()
        authorize_info.deserialize(reader)
        return authorize_info.to_json()


class TotalStake(object):
    def __init__(self):
        self.address = None
        self.stake = 0
        self.time_offset = 0

    def deserialize(self, reader: BinaryReader):
        self.address = Address(reader.read_bytes(20))
        self.stake = reader.read_int64()
        self.time_offset = reader.read_int32()


class SplitFeeAddress(object):
    def __init__(self):
        self.address = None
        self.amount = 0

    def deserialize(self, reader: BinaryReader):
        self.address = Address(reader.read_bytes(20))
        self.amount = reader.read_int64()

    def to_json(self):
        map = dict()
        map["address"] = self.address.b58encode()
        map["amount"] = self.amount
        return map


class PeerAttributes(object):
    def __init__(self):
        self.peer_pubkey = ''
        self.max_authorize = 0
        self.old_peerCost = 0
        self.new_peer_cost = 0
        self.set_cost_view = 0
        self.field1 = bytearray()
        self.field2 = bytearray()
        self.field3 = bytearray()
        self.field4 = bytearray()

    def deserialize(self, reader: BinaryReader):
        self.peer_pubkey = a2b_hex(reader.read_var_str()).hex()
        self.max_authorize = reader.read_int64()
        self.old_peerCost = reader.read_int64()
        self.new_peer_cost = reader.read_int64()
        self.set_cost_view = reader.read_int32()
        self.field1 = reader.read_var_bytes()
        self.field2 = reader.read_var_bytes()
        self.field3 = reader.read_var_bytes()
        self.field4 = reader.read_var_bytes()

    def to_json(self):
        map = dict()
        map["peer_pubkey"] = self.peer_pubkey
        map["max_authorize"] = self.max_authorize
        map["old_peerCost"] = self.old_peerCost
        map["new_peer_cost"] = self.new_peer_cost
        map["set_cost_view"] = self.set_cost_view
        map["field1"] = self.field1
        map["field2"] = self.field2
        map["field3"] = self.field3
        map["field4"] = self.field4
        return map


class AuthorizeInfo(object):
    def __init__(self):
        self.peer_pubkey = ''
        self.address = None
        self.consensus_pos = 0
        self.freeze_pos = 0
        self.new_pos = 0
        self.withdraw_pos = 0
        self.withdraw_freeze_pos = 0
        self.withdraw_unfreeze_pos = 0

    def deserialize(self, reader: BinaryReader):
        self.peer_pubkey = a2b_hex(reader.read_var_str()).hex()
        self.address = Address(reader.read_bytes(20))
        self.consensus_pos = reader.read_int64()
        self.freeze_pos = reader.read_int64()
        self.new_pos = reader.read_int64()
        self.withdraw_pos = reader.read_int64()
        self.withdraw_freeze_pos = reader.read_int64()
        self.withdraw_unfreeze_pos = reader.read_int64()

    def to_json(self):
        map = dict()
        map["peer_pubkey"] = self.peer_pubkey
        map["address"] = self.address.b58encode()
        map["consensus_pos"] = self.consensus_pos
        map["freeze_pos"] = self.freeze_pos
        map["new_pos"] = self.new_pos
        map["withdraw_pos"] = self.withdraw_pos
        map["withdraw_freeze_pos"] = self.withdraw_freeze_pos
        map["withdraw_unfreeze_pos"] = self.withdraw_unfreeze_pos
        return map


class GovernanceView(object):
    def __init__(self):
        self.view = 0
        self.height = 0
        self.tx_hash = None

    def deserialize(self, reader: BinaryReader):
        self.view = reader.read_int32()
        self.height = reader.read_int32()
        self.tx_hash = reader.read_bytes(32).hex()


class PeerPoolItem(object):
    def __init__(self):
        self.index = 0
        self.peer_pubkey = ''
        self.address = None
        self.status = 0
        self.init_pos = 0
        self.total_pos = 0

    def deserialize(self, reader: BinaryReader):
        self.index = reader.read_int32()
        self.peer_pubkey = a2b_hex(reader.read_var_str()).hex()
        self.address = Address(reader.read_bytes(20))
        self.status = reader.read_byte()
        self.init_pos = reader.read_int64()
        self.total_pos = reader.read_int64()

    def to_json(self):
        item = {}
        item["index"] = self.index
        item["peer_pubkey"] = self.peer_pubkey
        item["address"] = self.address.b58encode()
        item["status"] = self.status
        item["init_pos"] = self.init_pos
        item["total_pos"] = self.total_pos
        return item






