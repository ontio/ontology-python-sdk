from time import time
from ontology.utils import util
from ontology.vm import build_vm
from ontology.core.sig import Sig
from ontology.core.transaction import Transaction
from ontology.account.account import Account
from ontology.crypto.KeyType import KeyType
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.common.address import Address
from ontology.common.define import *
from ontology.io.MemoryStream import StreamManager
from ontology.io.BinaryReader import BinaryReader
from ontology.crypto.Curve import Curve
from binascii import b2a_hex, a2b_hex

def new_registry_ontid_transaction(ontid,pubkey,gas_limit,gas_price):
    contract_address = ONTID_CONTRACT_ADDRESS
    args = {"ontid": ontid.encode(), "pubkey": pubkey}
    invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "regIDWithPublicKey", args)
    unix_timenow = int(time())
    payer = Address.decodeBase58(ontid.replace("did:ont:","")).to_array()
    return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit,payer, invoke_code, bytearray(),
                       [], bytearray())

def new_get_ddo_transaction(ontid:str):
    contract_address = ONTID_CONTRACT_ADDRESS
    args = {"ontid": ontid.encode()}
    invoke_code = build_vm.build_native_invoke_code(contract_address, bytes([0]), "getDDO", args)
    unix_timenow = int(time())
    payer = Address(a2b_hex("0000000000000000000000000000000000000000".encode())).to_array()
    return Transaction(0, 0xd1, unix_timenow, 0, 0, payer, invoke_code, bytearray(),
                       [], bytearray())


def parse_ddo(ontid:str, ddo:str):

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
        addr = Address(str(recovery_bytes.hex()))
        print(addr.to_base58())
        d2["Recovery"] = addr.to_base58()
    d2["OntId"] = ontid
    return d2