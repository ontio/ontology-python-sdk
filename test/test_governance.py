import time
import unittest

from ontology.account.account import Account
from ontology.ont_sdk import OntologySdk

sdk = OntologySdk()
sdk.rpc.set_address("http://139.219.128.220:20336")
password = "111111"

account1 = Account('b2a7b886e69fd7fd9f12d746524d7f4ac00fce349f028900328dbbe09ba2ec23')
peer_publickey = "0278a64f9967197e58748e033dee9d7d7f58bdb166d3c7948002772fc64e791f98"


class TestGovernance(unittest.TestCase):

    def test_prepare(self):
        sdk.wallet_manager.open_wallet("./TestGovernance.json")
        identities = sdk.wallet_manager.get_wallet().identities
        if identities is None or len(identities) == 0:
            identity = sdk.wallet_manager.create_identity("sss", password)
            account = sdk.wallet_manager.get_account(identity.ont_id, password)
            tx = sdk.native_vm().ont_id().new_registry_ontid_transaction(identity.ont_id, account.serialize_public_key().hex(),
                                                                    account.get_address_base58(), 20000, 0)
            sdk.sign_transaction(tx, account)
            res = sdk.rpc.send_raw_transaction(tx)
            print("res:", res)
            print("txhash:", tx.hash256_bytes().hex())
            sdk.wallet_manager.write_wallet()
            time.sleep(6)
            tx2 = sdk.native_vm().ont_id().new_get_ddo_transaction(identity.ont_id)
            res2 = sdk.rpc.send_raw_transaction_pre_exec(tx2)
            print("res2:", res2)
        else:
            print(identities[0].ont_id)
            tx2 = sdk.native_vm().ont_id().new_get_ddo_transaction(identities[0].ont_id)
            res2 = sdk.rpc.send_raw_transaction_pre_exec(tx2)
            d = sdk.native_vm().ont_id().parse_ddo(identities[0].ont_id, res2)
            print(d)

    def test_register_candidate(self):
        sdk.wallet_manager.open_wallet("./TestGovernance.json")
        identities = sdk.wallet_manager.get_wallet().identities
        identity = identities[0]
        res = sdk.native_vm().governance().register_candidate(account1, peer_publickey, 10000, identity, password, 1,account1, 20000, 0)
        time.sleep(6)
        print(sdk.rpc.get_smart_contract_event_by_tx_hash(res))

    def test_get_peer_info(self):
        res = sdk.native_vm().governance().get_peer_info(peer_publickey)
        print("res:", res)

    def test_get_peer_info_all(self):
        res = sdk.native_vm().governance().get_peer_info_all()
        print("res:", res)
