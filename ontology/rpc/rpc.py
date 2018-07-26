import time

import requests
from ontology.rpc.define import *
import json
from ontology.core.sig import Sig
from ontology.account.account import Account
from ontology.crypto.KeyType import KeyType
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.common.address import Address
from ontology.crypto.encrypt import get_random_bytes
from ontology.smart_contract.native_contract import asset,ontid
import base64
from binascii import b2a_hex, a2b_hex
from time import *

rpc_address = "http://polaris3.ont.io:20336"
rest_address = "http://polaris1.ont.io:20334"


class HttpRequest(object):
    _timeout = 10

    @staticmethod
    def set_timeout(timeout=10):
        HttpRequest._timeout = timeout

    @staticmethod
    def request(method, url, payload):
        header = {'Content-type': 'application/json'}
        if method == "post":
            res = requests.post(url, json=payload, headers=header, timeout=HttpRequest._timeout)
            return res
        elif method == "get":
            res = requests.get(url, params=json.dumps(payload), timeout=HttpRequest._timeout)
            return res


class RpcClient(object):
    def __init__(self, qid=0, addr=""):
        self.qid = qid
        self.addr = addr

    def set_address(self, addr):
        self.addr = addr

    def set_json_rpc_version(self, method, param=[]):
        JsonRpcRequest["jsonrpc"] = JSON_RPC_VERSION
        JsonRpcRequest["id"] = "1"
        JsonRpcRequest["method"] = method
        JsonRpcRequest["params"] = param
        return JsonRpcRequest

    def get_version(self) -> str:
        rpc_struct = self.set_json_rpc_version(RPC_GET_VERSION, [])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_block_by_hash(self, hash: str):
        rpc_struct = self.set_json_rpc_version(RPC_GET_BLOCK, [hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_block_by_height(self, height):
        rpc_struct = self.set_json_rpc_version(RPC_GET_BLOCK, [height, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_block_count(self):
        rpc_struct = self.set_json_rpc_version(RPC_GET_BLOCK_COUNT)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_current_block_hash(self):
        rpc_struct = self.set_json_rpc_version(RPC_GET_CURRENT_BLOCK_HASH)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_block_hash_by_height(self, height):
        rpc_struct = self.set_json_rpc_version(RPC_GET_BLOCK_HASH, [height, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_balance(self, addr):
        rpc_struct = self.set_json_rpc_version(RPC_GET_BALANCE, [addr, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_allowance(self, addr):
        contract_address = get_asset_address("ont")
        print(contract_address)
        print(Address(str(contract_address.hex())).to_base58())
        print(addr)
        rpc_struct = self.set_json_rpc_version(RPC_GET_ALLOWANCE, ["ong", Address(str(contract_address.hex())).to_base58(), addr])
        print(rpc_struct)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_storage(self, addr, key):
        rpc_struct = self.set_json_rpc_version(RPC_GET_STORAGE, [addr, key, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        s = json.loads(r.content.decode())["result"]
        s = bytearray.fromhex(s)
        res = (s[0]) | (s[1]) << 8 | (s[2]) << 16 | (s[3]) << 24 | (s[4]) << 32 | (s[5]) << 40 | (s[6]) << 48 | (
            s[7]) << 56
        return res

    def get_smart_contract_event_by_txhash(self, tx_hash):
        rpc_struct = self.set_json_rpc_version(RPC_GET_SMART_CONTRACT_EVENT, [tx_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_smart_contract_event_by_block(self, height):
        rpc_struct = self.set_json_rpc_version(RPC_GET_SMART_CONTRACT_EVENT, [height, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_raw_transaction(self, tx_hash):
        rpc_struct = self.set_json_rpc_version(RPC_GET_TRANSACTION, [tx_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_smart_contract(self, contract_addr):
        rpc_struct = self.set_json_rpc_version(RPC_GET_SMART_CONTRACT, [contract_addr, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_generate_block_time(self):
        rpc_struct = self.set_json_rpc_version(RPC_GET_GENERATE_BLOCK_TIME)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_merkle_proof(self, tx_hash):
        rpc_struct = self.set_json_rpc_version(RPC_GET_MERKLE_PROOF, [tx_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def sign_to_transaction(self, tx, signer: Account):
        tx_hash = tx.hash256()
        sig_data = signer.generateSignature(tx_hash, SignatureScheme.SHA256withECDSA)
        sig = [Sig([signer.get_public_key()], 1, [sig_data])]
        tx.sigs = sig
        return tx

    def send_raw_transaction(self, tx):
        buf = tx.serialize()
        tx_data = buf.hex()
        rpc_struct = self.set_json_rpc_version(RPC_SEND_TRANSACTION, [tx_data])
        print(rpc_struct)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        print(r.content.decode())
        res = json.loads(r.content.decode())["result"]
        return res
    def send_raw_transaction_preexec(self, tx):
        buf = tx.serialize()
        tx_data = buf.hex()
        rpc_struct = self.set_json_rpc_version(RPC_SEND_TRANSACTION, [tx_data,1])
        print(rpc_struct)
        r = HttpRequest.request("post", self.addr, rpc_struct)
        print(r.content.decode())
        err = json.loads(r.content.decode())["error"]
        if err > 0:
            raise RuntimeError
        res = json.loads(r.content.decode())["result"]
        if res["State"] == 0:
            print(res)
            raise RuntimeError
        print(res)
        return res["Result"]

if __name__ == '__main__':
    cli = RpcClient(0,rpc_address)
    private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
    acc = Account(private_key, SignatureScheme.SHA256withECDSA)
    print(acc.get_address_base58())
    print(acc.get_public_key().hex())
    num = 100
    print(num.to_bytes(4, "little"))
    if False :
        tx = asset.new_transfer_transaction( "ont", acc.get_address().to_base58(), "AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve",513, 20000, 500)
        tx = cli.sign_to_transaction(tx, acc)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        cli.send_raw_transaction(tx)
    if False:
        tx = asset.new_get_balance_transaction("ont", acc.get_address_base58())
        result = cli.send_raw_transaction_preexec(tx)
        balance = int.from_bytes(a2b_hex(result.encode()), byteorder='little')
        print(balance)
    if True:
        did = "did:ont:" + acc.get_address_base58()
        tx = ontid.new_registry_ontid_transaction(did, acc.get_public_key(), 20000, 500)
        tx = cli.sign_to_transaction(tx, acc)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        cli.send_raw_transaction(tx)
    if False:
        did = "did:ont:"+acc.get_address_base58()
        tx = ontid.new_get_ddo_transaction(did)
        ddo = cli.send_raw_transaction_preexec(tx)
        print(ontid.parse_ddo(did,ddo))


if __name__ == '__main__':
    #rpc_address = "http://127.0.0.1:20336"
    cli = RpcClient(0, rpc_address)
    private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
    private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
    private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
    acc = Account(private_key, SignatureScheme.SHA256withECDSA)
    acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
    acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
    print("#################################")
    if False:
        print(acc.get_address_base58())
        print(acc2.get_address_base58())
        print(acc3.get_address_base58())
        print(cli.get_balance(acc.get_address_base58()))
        print(cli.get_balance(acc2.get_address_base58()))
        print(cli.get_balance(acc3.get_address_base58()))
    if False:
        print(acc.get_address_base58())
        print(acc2.get_address_base58())
        tx = asset.new_get_allowance_transaction("ont", acc.get_address_base58(), acc2.get_address_base58())
        print(cli.send_raw_transaction_preexec(tx))
        # tx2 = new_approve_transaction("ont", acc.get_address_base58(), acc2.get_address_base58(), 10, 20000, 500)
        # cli.sign_to_transaction(tx2, acc)
        # cli.send_raw_transaction(tx2)
        tx2 = asset.new_transferfrom_transaction("ont", acc2.get_address_base58(), acc.get_address_base58(), acc2.get_address_base58(), 10, 20000, 500)
        cli.sign_to_transaction(tx2, acc2)
        cli.send_raw_transaction(tx2)
        sleep(6)
        tx = asset.new_get_allowance_transaction("ont", acc.get_address_base58(), acc2.get_address_base58())
        print(cli.send_raw_transaction_preexec(tx))
    if False:
        print(asset.unboundong(cli, acc.get_address_base58()))
    if True:
        print(asset.unboundong(cli, acc.get_address_base58()))
        print(cli.get_balance(acc.get_address_base58()))
        tx = asset.new_withdraw_ong_transaction(acc.get_address().to_base58(), acc.get_address().to_base58(), 200, 20000, 500)
        tx = cli.sign_to_transaction(tx, acc)
        cli.send_raw_transaction(tx)
        sleep(6)
        print(cli.get_balance(acc.get_address_base58()))
        print(asset.unboundong(cli, acc.get_address_base58()))
    if False:
        tx = asset.new_transfer_transaction("ont", acc.get_address().to_base58(), "AKFMnJT1u5pyPhzGRuauD1KkyUvqjQsmGs", 1, 20000, 500)
        tx = cli.sign_to_transaction(tx, acc)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        print(cli.get_balance(acc.get_address_base58()))
        print(cli.get_balance("AKFMnJT1u5pyPhzGRuauD1KkyUvqjQsmGs"))
        cli.send_raw_transaction(tx)
        sleep(6)
        print(cli.get_balance(acc.get_address_base58()))
        print(cli.get_balance("AKFMnJT1u5pyPhzGRuauD1KkyUvqjQsmGs"))
    if False:
        toAddr = Address.decodeBase58("AKFMnJT1u5pyPhzGRuauD1KkyUvqjQsmGs")
        print(toAddr.to_array())
        tx = asset.new_get_balance_transaction("ont", "AKFMnJT1u5pyPhzGRuauD1KkyUvqjQsmGs")
        result = cli.send_raw_transaction_preexec(tx)
        print(result)
    if False:
        did = "did:ont:" + acc.get_address_base58()
        tx = ontid.new_registry_ontid_transaction(did, acc.get_public_key(), 20000, 500)
        tx = cli.sign_to_transaction(tx, acc)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        cli.send_raw_transaction(tx)
    if False:
        did = "did:ont:"+acc.get_address_base58()
        tx = ontid.new_get_ddo_transaction(did)
        ddo = cli.send_raw_transaction_preexec(tx)
        print(asset.parse_ddo(did, ddo))