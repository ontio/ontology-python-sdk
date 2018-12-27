import os
import time
import unittest

from ontology.account.account import Account
from ontology.ont_sdk import OntologySdk

sdk = OntologySdk()
rpc_address = 'http://139.219.128.220:20336'
sdk.rpc.set_address(rpc_address)
password = "111111"

account1 = Account('b2a7b886e69fd7fd9f12d746524d7f4ac00fce349f028900328dbbe09ba2ec23')
peer_publickey = "021b16a2f74c430256203685c9b742c7c27260b0bb3e76e75fd52bf3065226139e"


# class TestGovernance(unittest.TestCase):
#     def test_prepare(self):
#         path = os.path.join(os.path.dirname(__file__), 'TestGovernance.json')
#         sdk.wallet_manager.open_wallet(path)
#         identities = sdk.wallet_manager.get_wallet().identities
#         if identities is None or len(identities) == 0:
#             identity = sdk.wallet_manager.create_identity("sss", password)
#             account = sdk.wallet_manager.get_account(identity.ont_id, password)
#             tx = sdk.native_vm.ont_id().new_registry_ont_id_transaction(identity.ont_id,
#                                                                           account.get_public_key_bytes().hex(),
#                                                                           account.get_address_base58(), 20000, 0)
#             sdk.sign_transaction(tx, account)
#             res = sdk.rpc.send_raw_transaction(tx)
#             print("res:", res)
#             print("txhash:", tx.hash256_bytes().hex())
#             sdk.wallet_manager.write_wallet()
#             time.sleep(random.randint(6, 10))
#             tx2 = sdk.native_vm.ont_id().new_get_ddo_transaction(identity.ont_id)
#             res2 = sdk.rpc.send_raw_transaction_pre_exec(tx2)
#             print("res2:", res2)
#         else:
#             print(identities[0].ont_id)
#             tx2 = sdk.native_vm.ont_id().new_get_ddo_transaction(identities[0].ont_id)
#             res2 = sdk.rpc.send_raw_transaction_pre_exec(tx2)
#             d = sdk.native_vm.ont_id().parse_ddo(identities[0].ont_id, res2)
#             print(d)
#         os.remove(path)
#
#     def test_getbalance(self):
#         print(sdk.native_vm.asset().query_balance('ont', account1.get_address_base58()))
#         print(sdk.native_vm.asset().query_balance("ong", account1.get_address_base58()))
#
#     def test_register_candidate(self):
#         sdk.wallet_manager.open_wallet("./TestGovernance.json")
#         identities = sdk.wallet_manager.get_wallet().identities
#         identity = identities[0]
#         res = sdk.native_vm.governance().register_candidate(account1, peer_publickey, 10000, identity, password, 1,
#                                                               account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_unregister_candidate(self):
#         res = sdk.native_vm.governance().unregister_candidate(account1, peer_publickey, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_authorize_for_peer(self):
#         peer_publickeys = list()
#         peer_publickeys.append(peer_publickey)
#         withdraw_lists = list()
#         withdraw_lists.append(500)
#         res = sdk.native_vm.governance().authorize_for_peer(account1, peer_publickeys, withdraw_lists, account1,
#                                                               20000, 0)
#         print("res:", res)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_get_authorize_info(self):
#         res = sdk.native_vm.governance().get_authorize_info(peer_publickey, account1.get_address())
#         print("res:", res)
#
#     def test_aa(self):
#         print("voteInfoPool".encode().hex())
#
#     def test_get_peer_unbind_ong(self):
#         sdk.native_vm.governance().get_peer_unbind_ong(account1.get_address_base58())
#
#     def test_unauthorize_for_peer(self):
#         peer_publickeys = list()
#         peer_publickeys.append(peer_publickey)
#         withdraw_lists = list()
#         withdraw_lists.append(500)
#         res = sdk.native_vm.governance().unauthorize_for_peer(account1, peer_publickeys, withdraw_lists, account1,
#                                                                 20000, 0)
#         print("res:", res)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_withdraw(self):
#         peer_publickeys = list()
#         peer_publickeys.append(peer_publickey)
#         withdraw_lists = list()
#         withdraw_lists.append(500)
#         res = sdk.native_vm.governance().withdraw(account1, peer_publickeys, withdraw_lists, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_quit_node(self):
#         res = sdk.native_vm.governance().quit_node(account1, peer_publickey, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_withdraw_fee(self):
#         res = sdk.native_vm.governance().withdraw_fee(account1, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_withdraw_ong(self):
#         res = sdk.native_vm.governance().withdraw_ong(account1, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_change_max_authorization(self):
#         res = sdk.native_vm.governance().change_max_authorization(account1, peer_publickey, 10000, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_add_init_pos(self):
#         res = sdk.native_vm.governance().add_init_pos(account1, peer_publickey, 1000, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_reduce_init_pos(self):
#         res = sdk.native_vm.governance().reduce_init_pos(account1, peer_publickey, 1000, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_set_peer_cost(self):
#         res = sdk.native_vm.governance().set_peer_cost(account1, peer_publickey, 90, account1, 20000, 0)
#         time.sleep(random.randint(6, 10))
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_get_peer_attributes(self):
#         res = sdk.native_vm.governance().get_peer_attributes(peer_publickey)
#         print("res:", res)
#
#     def test_get_split_fee_address(self):
#         res = sdk.native_vm.governance().get_split_fee_address(account1.get_address_base58())
#         print("res:", res)
#
#     def test_get_peer_info(self):
#         res = sdk.native_vm.governance().get_peer_info(peer_publickey)
#         print("res:", res)
#
#     def test_get_peer_info_all(self):
#         res = sdk.native_vm.governance().get_peer_info_all()
#         print("res:", res)
#
#     def test_calc_unbind_ong(self):
#         res = sdk.native_vm.governance().calc_unbind_ong(1, 0, 31536000 * 18)
#         print(res)
#
#     def test_unbound_deadline(self):
#         print(sdk.native_vm.governance().unbound_deadline())
#
#     def test_get_total_stake(self):
#         total_stake = sdk.native_vm.governance().get_total_stake(account1.get_address_base58())
#         if total_stake is None:
#             return
#         print(total_stake.time_offset)
#         print(total_stake.stake)
#         print(total_stake.address)
