import requests
from ontology.rpc.define import *
import json
from ontology.core.transaction import Sig
from ontology.account.account import Account
from ontology.crypto.KeyType import KeyType
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.common.address import Address
from ontology.smart_contract.native_contract.asset import new_transfer_transaction
from ontology.crypto.encrypt import get_random_bytes
from ontology.smart_contract.native_contract import ontid
from ontology.io.BinaryReader import BinaryReader
from ontology.io.MemoryStream import StreamManager
from ontology.utils.util import *
from ontology.crypto.Curve import Curve
import base64
import base58

rpc_address = "http://polaris1.ont.io:20336"
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

    def transfer(self, gas_price: int, gas_limit: int, asset: str, from_account, to_addr, amount: int):
        tx = new_transfer_transaction(gas_price, gas_limit, asset, from_account.get_address().to_array(), to_addr,
                                      amount)
        tx = self.sign_to_transaction(tx, from_account)
        self.send_raw_transaction(tx)
        return tx
    def registry_ontid(self, account: Account,gas_limit: int, gas_price: int):
        did = "did:ont:"+account.get_address_base58()
        print(did)
        tx = ontid.new_registry_ontid_transaction( did,account.get_public_key(),gas_limit, gas_price)
        tx = self.sign_to_transaction(tx, account)
        return tx
    def get_ddo(self, did: str):
        tx = ontid.new_get_ddo_transaction(did)
        p = Address.decodeBase58("AKFMnJT1u5pyPhzGRuauD1KkyUvqjQsmGs").to_array()
        tx.payer = str(p)
        return tx
    def sign_to_transaction(self, tx, signer: Account):
        tx.payer = signer.get_address().to_array()
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
        res = json.loads(r.content.decode())["result"]
        return res

if __name__ == '__main__':
    cli = RpcClient(0, rpc_address)
    private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
    acc = Account(private_key, SignatureScheme.SHA256withECDSA)
    print(acc.get_address_base58())
    print(acc.get_public_key().hex())
    if False:
        toAddr = Address.decodeBase58("AKFMnJT1u5pyPhzGRuauD1KkyUvqjQsmGs")
        print(toAddr.to_array().hex())
        tx = cli.transfer(500, 20000, "ont", acc, toAddr.to_array(), 1)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        cli.send_raw_transaction(tx)
    if False:
        tx = cli.registry_ontid(acc, 20000, 500)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        cli.send_raw_transaction(tx)
    if True:
        tx = cli.get_ddo("did:ont:"+acc.get_address_base58())
        result = cli.send_raw_transaction_preexec(tx)
        ddo = result.get("Result")
        print("ddo:", ddo)
        ms = StreamManager.GetStream(hex_to_bytes("76010000002103036c12be3726eb283d078dff481175e96224f0b0c632c7a37e10eb40fe6be8890200000023131402c06c72787291a7ce27be41ce569b42abd5824d2a93158ec3c49575d1ae9e37c703000000231314029682e54813cb5fc382f69803a6da84fe0a085bb888ee63d90d0e72f5e65fed0d26046b65793206537472696e670676616c756532046b65793106537472696e670676616c7565311456bf94c2c1b246c9efcde7ac584b9447d06d24e5"))
        reader = BinaryReader(ms)
        try:
            publickey_bytes = reader.ReadVarBytes()
        except Exception as e:
            publickey_bytes = bytearray()
        try:
            attribute_bytes = reader.ReadVarBytes()
        except Exception as e:
            attribute_bytes = bytearray()
        try:
            recovery_bytes = reader.ReadVarBytes()
        except Exception as e:
            recovery_bytes = bytearray()
        pubKey_list = []
        if len(publickey_bytes) != 0:
            ms = StreamManager.GetStream(publickey_bytes)
            reader2 = BinaryReader(ms)
            while True:
                try:
                    index = reader2.ReadInt32()
                    addr = acc.get_address_base58()
                    d = {}
                    d['PubKeyId'] = "did:ont:" + addr + "#keys-" + str(index)
                    pubkey = reader2.ReadVarBytes()
                    if len(pubkey) == 33:
                        d["Type"] = KeyType.ECDSA.name
                        d["Curve"] = Curve.P256.name
                        d["Value"] = pubkey.hex()
                    else:
                        print(pubkey)
                        d["Type"] = KeyType.from_label(pubkey[0])
                        d["Curve"] = Curve.from_label(pubkey[1])
                        d["Value"] = pubkey.hex()
                    pubKey_list.append(d)
                except Exception as e:
                    break
        attribute_list = []
        if len(attribute_bytes) != 0:
            ms = StreamManager.GetStream(attribute_bytes)
            reader2 = BinaryReader(ms)
            while True:
                try:
                    d = {}
                    key = reader2.ReadVarBytes()
                    if len(key) == 0:
                        break
                    d["Key"] = str(key, 'utf8')
                    d["Type"] = str(reader2.ReadVarBytes(), 'utf-8')
                    d["Value"] = str(reader2.ReadVarBytes(), 'utf-8')
                    attribute_list.append(d)
                except Exception as e:
                    break
        d2 = {}
        d2["Owners"] = pubKey_list
        d2["Attributes"] = attribute_list
        if len(recovery_bytes) != 0:
            addr = Address(str(recovery_bytes.hex()))
            print(addr.to_base58())
            d2["Recovery"] = addr.to_base58()
        d2["OntId"] = "did:ont:" + acc.get_address_base58()
        print(d2)
