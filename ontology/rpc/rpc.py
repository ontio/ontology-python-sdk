import requests
from ontology.rpc.define import *
import json
from ontology.core.transaction import Transaction
from ontology.common.address import Address
from ontology.rpc.define import rpc_address
from ontology.utils.util import get_asset_address


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
    def __init__(self, qid=0, addr=None):
        self.qid = qid
        self.addr = addr

    def set_address(self, addr):
        self.addr = addr

    def set_json_rpc_version(self, method, param=None):
        JsonRpcRequest["jsonrpc"] = JSON_RPC_VERSION
        JsonRpcRequest["id"] = "1"
        JsonRpcRequest["method"] = method
        if param == None:
            JsonRpcRequest["params"] = list()
        else:
            JsonRpcRequest["params"] = param
        return JsonRpcRequest

    def get_version(self) -> str:
        rpc_struct = self.set_json_rpc_version(RPC_GET_VERSION, [])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def get_block_by_hash(self, hash_value: str):
        rpc_struct = self.set_json_rpc_version(RPC_GET_BLOCK, [hash_value, 1])
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
        rpc_struct = self.set_json_rpc_version(RPC_GET_ALLOWANCE,
                                               ["ong", Address((contract_address)).to_base58(), addr])
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

    def get_merkle_proof(self, tx_hash):
        rpc_struct = self.set_json_rpc_version(RPC_GET_MERKLE_PROOF, [tx_hash, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def send_raw_transaction(self, tx: Transaction):
        buf = tx.serialize()
        tx_data = buf.hex()
        rpc_struct = self.set_json_rpc_version(RPC_SEND_TRANSACTION, [tx_data])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())["result"]
        return res

    def send_raw_transaction_preexec(self, tx: Transaction):
        buf = tx.serialize()
        tx_data = buf.hex()
        rpc_struct = self.set_json_rpc_version(RPC_SEND_TRANSACTION, [tx_data, 1])
        r = HttpRequest.request("post", self.addr, rpc_struct)
        res = json.loads(r.content.decode())
        # print(res)
        err = res["error"]
        if err > 0:
            raise RuntimeError("error > 0")
        if res["result"]["State"] == 0:
            raise RuntimeError("State = 0")
        return res["result"]["Result"]
