import json
from binascii import a2b_hex
from collections import namedtuple
from unittest import TestCase

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams

rpc_address = "http://polaris3.ont.io:20336"
# rpc_address = "http://127.0.0.1:20336"
sdk = OntologySdk()

private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
private_key4 = "f9d2d30ffb22dffdf4f14ad6f1303460efc633ea8a3014f638eaa19c259bada1"
acc = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acc2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
acc3 = Account(a2b_hex(private_key3.encode()), SignatureScheme.SHA256withECDSA)
acc4 = Account(a2b_hex(private_key4.encode()), SignatureScheme.SHA256withECDSA)


class TestNeoVm(TestCase):

    def test_big_int(self):
        num = 135241956301000000
        print(num.bit_length())
        print(num.to_bytes(8, "little").hex())
        print(num.bit_length())

    def test_balance(self):
        print(sdk.rpc)
        sdk.set_rpc(rpc_address)
        print(sdk.rpc.get_balance(acc.get_address_base58()))
        print(sdk.rpc.get_balance(acc2.get_address_base58()))
        print(sdk.rpc.get_balance(acc3.get_address_base58()))
        print(sdk.rpc.get_balance(acc4.get_address_base58()))

        print(sdk.native_vm().asset().unboundong(acc.get_address_base58()))
        print(sdk.native_vm().asset().unboundong(acc4.get_address_base58()))

        if False:
            tx = sdk.native_vm().asset().new_transfer_transaction("ont", acc2.get_address_base58(),
                                                                  acc.get_address_base58(), 120,
                                                                  acc.get_address_base58(), 20000, 500)
            sdk.sign_transaction(tx, acc)
            sdk.add_sign_transaction(tx, acc2)
            res = sdk.rpc.send_raw_transaction(tx)
            print(res)
        if False:
            tx = sdk.native_vm().asset().new_withdraw_ong_transaction(acc4.get_address_base58(),
                                                                      acc4.get_address_base58(), 1352419563015000,
                                                                      acc4.get_address_base58(), 20000, 500)
            sdk.sign_transaction(tx, acc4)
            sdk.rpc.send_raw_transaction(tx)

    def test_make_deploy_transaction(self):
        sdk.set_rpc(rpc_address)
        print(sdk.rpc.get_balance(acc2.get_address_base58()))
        code = "54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566"
        codeaddr = Address.address_from_vm_code(code)
        print(codeaddr.to_hex_string())
        tx = sdk.neo_vm().make_deploy_transaction(code, True, "name", "v1.0", "author", "email", "desp",
                                                  acc4.get_address_base58(), 20000000, 500)
        sdk.sign_transaction(tx, acc4)
        res = sdk.rpc.send_raw_transaction(tx)
        print(res)

    def test_invoke_transaction(self):
        sdk.set_rpc(rpc_address)
        code = "54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566"
        codeaddr = Address.address_from_vm_code(code)
        abi_str = '{"hash":"0x362cb5608b3eca61d4846591ebb49688900fedd0","entrypoint":"Main","functions":[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args","type":"Array"}],"returntype":"Any"},{"name":"Hello","parameters":[{"name":"msg","type":"String"}],"returntype":"Void"}],"events":[]}'
        abi = json.loads(abi_str, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        abi_info = AbiInfo(abi.hash, abi.entrypoint, abi.functions, abi.events)
        func = abi_info.get_function("Hello")
        func.set_params_value("sss")
        # params = BuildParams.serialize_abi_function(func)
        # print("params:", type(params))
        # tx = sdk.neo_vm().make_invoke_transaction(codeaddr.to_array(),"",bytearray(params),acc2.get_address().to_array(),20000,500)
        print(codeaddr.to_hex_string())
        contract_addr = bytearray(codeaddr.to_array())
        print(contract_addr.hex())
        res = sdk.neo_vm().send_transaction(contract_addr, None, None, 0, 0, func, True)
        print(res)
