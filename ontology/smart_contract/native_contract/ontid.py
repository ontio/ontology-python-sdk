from time import time
from ontology.vm import build_vm
from ontology.core.transaction import Transaction
from ontology.crypto.key_type import KeyType
from ontology.common.address import Address
from ontology.common.define import *
from ontology.io.memory_stream import StreamManager
from ontology.io.binary_reader import BinaryReader
from ontology.crypto.curve import Curve
from binascii import b2a_hex, a2b_hex


class OntId(object):

    def new_registry_ontid_transaction(self, ontid: str,pubkey: str, payer: str, gas_limit: int,gas_price: int):
        contract_address = ONTID_CONTRACT_ADDRESS
        args = {"ontid": ontid.encode(), "pubkey": pubkey}
        invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "regIDWithPublicKey", args)
        unix_timenow = int(time())
        return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                           [], bytearray())

    def new_add_attribute_transaction(self, ontid: str, pubkey: str, attris: list, payer: str, gas_limit: int,gas_price: int):
        contract_address = ONTID_CONTRACT_ADDRESS
        args = {"ontid": ontid.encode(), "length": len(attris)}
        for i in range(len(attris)):
            args["key"+str(i)] = bytes(attris[i]["key"].encode())
            args["type" + str(i)] = bytes(attris[i]["type"].encode())
            args["value" + str(i)] = bytes(attris[i]["value"].encode())
        args["pubkey"] = pubkey
        invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "addAttributes", args)
        unix_timenow = int(time())
        return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                           [], bytearray())

    def new_remove_attribute_transaction(self, ontid: str, pubkey: bytearray,path: str, payer: str, gas_limit: int,gas_price: int):
        contract_address = ONTID_CONTRACT_ADDRESS
        args = {"ontid": ontid.encode(), "key": bytes(path.encode()), "pubkey": pubkey}
        invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "removeAttribute", args)
        print("invoke_code", invoke_code.hex())
        unix_timenow = int(time())
        return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                           [], bytearray())

    def new_add_pubkey_transaction(self, ontid: str, pubkey_or_recovery: bytes, new_pubkey: bytes, payer: str, gas_limit: int, gas_price: int):
        contract_address = ONTID_CONTRACT_ADDRESS
        args = {"ontid": ontid.encode(), "pubkey": new_pubkey,"pubkey_or_recovery": pubkey_or_recovery}
        invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "addKey", args)
        unix_timenow = int(time())
        return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                           [], bytearray())

    def new_remove_pubkey_transaction(self, ontid: str, pubkey_or_recovery: bytes , remove_pubkey: bytes, payer: str, gas_limit: int, gas_price: int):
        contract_address = ONTID_CONTRACT_ADDRESS
        args = {"ontid": ontid.encode(), "pubkey": remove_pubkey,"pubkey_or_recovery": pubkey_or_recovery}
        invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "removeKey", args)
        print("invoke_code", invoke_code.hex())
        unix_timenow = int(time())
        return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                           [], bytearray())

    def new_add_rcovery_transaction(self, ontid: str, pubkey: bytes, recovery: str, payer: str, gas_limit: int, gas_price: int):
        contract_address = ONTID_CONTRACT_ADDRESS
        args = {"ontid": ontid.encode(), "recovery": Address.decodeBase58(recovery).to_array(), "pubkey": pubkey}
        invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "addRecovery", args)
        print("invoke_code", invoke_code.hex())
        unix_timenow = int(time())
        return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(), invoke_code, bytearray(),
                           [], bytearray())

    def new_get_ddo_transaction(self, ontid: str):
        contract_address = ONTID_CONTRACT_ADDRESS
        args = {"ontid": ontid.encode()}
        invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "getDDO", args)
        unix_timenow = int(time())
        payer = Address(a2b_hex("0000000000000000000000000000000000000000".encode())).to_array()
        return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(),
                           [], bytearray())

    def parse_ddo(self, ontid: str, ddo: str):
        if ddo == "":
            return ""
        ms = StreamManager.GetStream(a2b_hex(ddo))
        reader = BinaryReader(ms)
        try:
            publickey_bytes = reader.ReadVarBytes()
        except Exception as e:
            raise e
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
                    d = {}
                    d['PubKeyId'] = ontid + "#keys-" + str(index)
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
                    d["Key"] = str(key, 'utf-8')
                    d["Type"] = str(reader2.ReadVarBytes(), 'utf-8')
                    d["Value"] = str(reader2.ReadVarBytes(), 'utf-8')
                    attribute_list.append(d)
                except Exception as e:
                    break
        d2 = {}
        d2["Owners"] = pubKey_list
        d2["Attributes"] = attribute_list
        if len(recovery_bytes) != 0:
            addr = Address(recovery_bytes)
            print(addr.to_base58())
            d2["Recovery"] = addr.to_base58()
        d2["OntId"] = ontid
        return d2