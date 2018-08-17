import json
from collections import namedtuple
from time import time
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams


class Nep5(object):
    def __init__(self, sdk: OntologySdk):
        self.nep5_abi = '{\"hash\":\"0xd17d91a831c094c1fd8d8634b8cd6fa9fbaedc99\",\"entrypoint\":\"Main\"," + "\"functions\":[{\"name\":\"Name\",\"parameters\":[],\"returntype\":\"String\"}," + "{\"name\":\"Symbol\",\"parameters\":[],\"returntype\":\"String\"}," + "{\"name\":\"Decimals\",\"parameters\":[],\"returntype\":\"Integer\"},{\"name\":\"Main\",\"parameters\":[{\"name\":\"operation\",\"type\":\"String\"}," + "{\"name\":\"args\",\"type\":\"Array\"}],\"returntype\":\"Any\"}," + "{\"name\":\"Init\",\"parameters\":[],\"returntype\":\"Boolean\"}," + "{\"name\":\"TotalSupply\",\"parameters\":[],\"returntype\":\"Integer\"}," + "{\"name\":\"Transfer\",\"parameters\":[{\"name\":\"from\",\"type\":\"ByteArray\"},{\"name\":\"to\",\"type\":\"ByteArray\"},{\"name\":\"value\",\"type\":\"Integer\"}],\"returntype\":\"Boolean\"}," + "{\"name\":\"BalanceOf\",\"parameters\":[{\"name\":\"address\",\"type\":\"ByteArray\"}],\"returntype\":\"Integer\"}]," + "\"events\":[{\"name\":\"transfer\",\"parameters\":[{\"name\":\"arg1\",\"type\":\"ByteArray\"},{\"name\":\"arg2\",\"type\":\"ByteArray\"},{\"name\":\"arg3\",\"type\":\"Integer\"}],\"returntype\":\"Void\"}]}'
        self.__sdk = sdk
        self.contract_addr = "d17d91a831c094c1fd8d8634b8cd6fa9fbaedc99"

    def set_contract_addr(self, addr: str):
        self.contract_addr = addr

    def get_contract_addr(self):
        return self.contract_addr

    def send_init(self, acct: Account, payer: Account, gaslimit: int, gasprice: int):
        return self.__send_init(acct, payer, gaslimit, gasprice, False)

    def send_init_pre_exec(self, acct: Account, payer: Account, gaslimit: int, gasprice: int):
        return self.__send_init(acct, payer, gaslimit, gasprice, True)

    def __send_init(self, acct: Account, payer_acct: Account, gas_limit: int, gas_price: int, pre_exec=False):
        if self.contract_addr is None or self.contract_addr == "":
            raise Exception("null code_address")
        abi = json.loads(self.nep5_abi, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        abi_info = AbiInfo(abi.hash, abi.entrypoint, abi.functions, abi.events)
        func = abi_info.get_function("init")
        if pre_exec:
            params = BuildParams.serialize_abi_function(func)
            unix_time_now = int(time())
            tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, bytearray(),
                             params, bytearray(), [], bytearray())
            if acct is not None:
                self.__sdk.sign_transaction(tx, acct)
            obj = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
            if int(obj["Result"]) is not 1:
                raise Exception("send_raw_transaction PreExec error:", obj)
            return obj["Gas"]
        if acct is None or payer_acct is None:
            raise Exception("acct or payer_acct should not be None")
        return self.__sdk.neo_vm().send_transaction(bytearray(self.contract_addr), acct, payer_acct, gas_limit, gas_price,
                                                    func, pre_exec)
