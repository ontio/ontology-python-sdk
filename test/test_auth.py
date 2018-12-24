import json
import time
import unittest
from binascii import a2b_hex

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.exception.exception import SDKException
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo

rpc_address = 'http://polaris3.ont.io:20336'

sdk = OntologySdk()
sdk.set_rpc_address(rpc_address)
private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
acc = Account(private_key, SignatureScheme.SHA256withECDSA)
acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)

admin_identity = sdk.wallet_manager.create_identity_from_private_key("sss", "111111",
                                                                     '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf')

new_admin_identity = sdk.wallet_manager.create_identity_from_private_key("sss2", "111111",
                                                                         '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114')

identity = sdk.wallet_manager.create_identity_from_private_key("sss2", "111111",
                                                               '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f')

abi_str = '{"hash":"0xbc9795db0abe9d2d9ea565286a237dbf6b407165","entrypoint":"Main","functions":[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args","type":"Array"}],"returntype":"Any"},{"name":"foo","parameters":[],"returntype":"String"},{"name":"foo2","parameters":[],"returntype":"String"},{"name":"foo3","parameters":[],"returntype":"String"},{"name":"init","parameters":[],"returntype":"Boolean"}],"events":[]}'
#
#
# class TestAuth(unittest.TestCase):
#     def test_aa(self):
#         aa = '0000000000000000000000000000000000000006'
#         print(Address(a2b_hex(aa.encode())).to_bytes())
#         print(bytearray.fromhex(aa))
#
#     def test_make_deploy_transaction(self):
#         sdk.set_rpc_address(rpc_address)
#         code = '5ac56b6c766b00527ac46c766b51527ac4616c766b00c304696e6974876c766b52527ac46c766b52c3641100616580016c766b53527ac46222016c766b00c303666f6f876c766b54527ac46c766b54c3644400616c766b00c36c766b51c3617c650202009c6c766b55527ac46c766b55c3641500076e6f20617574686c766b53527ac462d6006165db006c766b53527ac462c8006c766b00c304666f6f32876c766b56527ac46c766b56c3644400616c766b00c36c766b51c3617c65a701009c6c766b57527ac46c766b57c3641500076e6f20617574686c766b53527ac4627b00616599006c766b53527ac4626d006c766b00c304666f6f33876c766b58527ac46c766b58c3644400616c766b00c36c766b51c3617c654c01009c6c766b59527ac46c766b59c3641500076e6f20617574686c766b53527ac4622000616557006c766b53527ac4621200046f7665726c766b53527ac46203006c766b53c3616c756651c56b6101416c766b00527ac46203006c766b00c3616c756651c56b6101426c766b00527ac46203006c766b00c3616c756651c56b6101436c766b00527ac46203006c766b00c3616c756653c56b611400000000000000000000000000000000000000066c766b00527ac4006c766b00c311696e6974436f6e747261637441646d696e612a6469643a6f6e743a41617a457666515063513247454646504c46315a4c7751374b356a446e383168766561537951795572755172755279527954727552727568164f6e746f6c6f67792e4e61746976652e496e766f6b656c766b51527ac46c766b51c300517f519c6c766b52527ac46203006c766b52c3616c756657c56b6c766b00527ac46c766b51527ac461556154c66c766b527a527ac46c766b55c36c766b52527ac46c766b52c361682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e6753637269707448617368007cc46c766b52c36c766b00c3527cc46c766b52c36c766b51c300c3517cc46c766b52c36c766b51c351c3537cc41400000000000000000000000000000000000000066c766b53527ac4006c766b53c30b766572696679546f6b656e6c766b52c361537951795572755172755279527954727552727568164f6e746f6c6f67792e4e61746976652e496e766f6b656c766b54527ac46c766b54c300517f519c6c766b56527ac46203006c766b56c3616c7566'
#         b58_payer = acc.get_address_base58()
#         gas_limit = 20000000
#         gas_price = 500
#         tx = sdk.neo_vm.make_deploy_transaction(code, True, 'name', 'v1.0', 'author', 'email', 'desp', b58_payer,
#                                                   gas_limit, gas_price)
#         sdk.sign_transaction(tx, acc)
#         res = sdk.rpc.send_raw_transaction(tx)
#         time.sleep(6)
#         print(sdk.rpc.get_smart_contract("bc9795db0abe9d2d9ea565286a237dbf6b407165"))
#
#     def test_register(self):
#         tx = sdk.native_vm.ont_id().new_registry_ont_id_transaction(admin_identity.ont_id,
#                                                                       admin_identity.controls[0].public_key,
#                                                                       acc.get_address_base58(), 20000, 0)
#         tx2 = sdk.native_vm.ont_id().new_registry_ont_id_transaction(new_admin_identity.ont_id,
#                                                                        new_admin_identity.controls[0].public_key,
#                                                                        acc.get_address_base58(), 20000, 0)
#         print(new_admin_identity.controls[0].public_key)
#         print(acc3.serialize_public_key().hex())
#         sdk.sign_transaction(tx, acc)
#         sdk.sign_transaction(tx2, acc)
#         account1 = sdk.wallet_manager.get_account(admin_identity.ont_id, "111111")
#         account2 = sdk.wallet_manager.get_account(new_admin_identity.ont_id, "111111")
#         sdk.add_sign_transaction(tx, account1)
#         sdk.add_sign_transaction(tx2, account2)
#         try:
#             tx_hash = sdk.rpc.send_raw_transaction(tx)
#             time.sleep(6)
#             print(sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash))
#         except SDKException as e:
#             self.assertIn('register ONT ID error: already registered', e.args[1])
#         try:
#             tx_hash = sdk.rpc.send_raw_transaction(tx2)
#             time.sleep(6)
#             print(sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash))
#         except SDKException as e:
#             self.assertIn('register ONT ID error: already registered', e.args[1])
#
#     def test_getddo(self):
#         tx = sdk.native_vm.ont_id().new_get_ddo_transaction(new_admin_identity.ont_id)
#         res = sdk.rpc.send_raw_transaction_pre_exec(tx)
#         print(sdk.native_vm.ont_id().parse_ddo(new_admin_identity.ont_id, res))
#
#     def test_init(self):
#         abi = json.loads(abi_str)
#         abi_info = AbiInfo(abi['hash'], abi['entrypoint'], abi['functions'], abi['events'])
#         func = abi_info.get_function("init")
#         contract_address = bytearray.fromhex("bc9795db0abe9d2d9ea565286a237dbf6b407165")
#         contract_address.reverse()
#         gas_limit = 20000000
#         gas_price = 500
#         res = sdk.rpc.send_neo_vm_transaction(contract_address, acc, acc, gas_limit, gas_price, func, False)
#         time.sleep(6)
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_transfer(self):
#         contract_address = "bc9795db0abe9d2d9ea565286a237dbf6b407165"
#         code_address = bytearray.fromhex(contract_address)
#         code_address.reverse()
#         gas_limit = 20000000
#         gas_price = 500
#         txhash = sdk.native_vm.auth().send_transfer(admin_identity, "111111", 1, code_address.hex(),
#                                                       new_admin_identity.ont_id, acc, gas_limit, gas_price)
#         time.sleep(6)
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))
#
#     def test_assign_funcs_to_role(self):
#         contract_address = "bc9795db0abe9d2d9ea565286a237dbf6b407165"
#         code_address = bytearray.fromhex(contract_address)
#         code_address.reverse()
#         function_name = list()
#         function_name.append("foo")
#         function_name.append("foo2")
#         gas_limit = 20000000
#         gas_price = 500
#         res = sdk.native_vm.auth().assign_funcs_to_role(new_admin_identity, "111111", 1, code_address.hex(), "role3",
#                                                           function_name, acc, gas_limit, gas_price)
#         time.sleep(6)
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_assign_ont_ids_to_role(self):
#         contract_address = "bc9795db0abe9d2d9ea565286a237dbf6b407165"
#         code_address = bytearray.fromhex(contract_address)
#         code_address.reverse()
#         ont_ids = list()
#         ont_ids.append(identity.ont_id)
#         gas_limit = 20000000
#         gas_price = 500
#         res = sdk.native_vm.auth().assign_ont_ids_to_role(new_admin_identity, "111111", 1, code_address.hex(),
#                                                             "role3",
#                                                             ont_ids, acc, gas_limit, gas_price)
#         time.sleep(6)
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))
#
#     def test_verify_token(self):
#         contract_address = "bc9795db0abe9d2d9ea565286a237dbf6b407165"
#         code_address = bytearray.fromhex(contract_address)
#         code_address.reverse()
#         res = sdk.native_vm.auth().verify_token(admin_identity, "111111", 1, code_address.hex(), "foo")
#         print("res:", res)
#
#     def test_delegate(self):
#         contract_address = "bc9795db0abe9d2d9ea565286a237dbf6b407165"
#         code_address = bytearray.fromhex(contract_address)
#         code_address.reverse()
#         gas_limit = 20000000
#         gas_price = 500
#         txhash = sdk.native_vm.auth().delegate(identity, "111111", 1, code_address.hex(), admin_identity.ont_id,
#                                                  "role", 60 * 5, 1, acc, gas_limit, gas_price)
#         time.sleep(6)
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))
#
#     def test_withdraw(self):
#         contract_address = "bc9795db0abe9d2d9ea565286a237dbf6b407165"
#         code_address = bytearray.fromhex(contract_address)
#         code_address.reverse()
#         gas_limit = 20000000
#         gas_price = 500
#         txhash = sdk.native_vm.auth().withdraw(identity, "111111", 1, code_address.hex(), admin_identity.ont_id,
#                                                  "role", acc, gas_limit, gas_price)
#         time.sleep(6)
#         print(sdk.rpc.get_smart_contract_event_by_tx_hash(txhash))
