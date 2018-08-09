import json
from collections import namedtuple
from time import time
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams


class ClaimRecord(object):

    def __init__(self, sdk):
        self.__sdk = sdk
        self.contract_address = "36bb5c053b6b839c8f6b923fe852f91239b9fccc"
        self.abi = '{"hash":"0x36bb5c053b6b839c8f6b923fe852f91239b9fccc","entrypoint":"Main","functions":[{"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args","type":"Array"}],"returntype":"Any"},{"name":"Commit","parameters":[{"name":"claimId","type":"ByteArray"},{"name":"commiterId","type":"ByteArray"},{"name":"ownerId","type":"ByteArray"}],"returntype":"Boolean"},{"name":"Revoke","parameters":[{"name":"claimId","type":"ByteArray"},{"name":"ontId","type":"ByteArray"}],"returntype":"Boolean"},{"name":"GetStatus","parameters":[{"name":"claimId","type":"ByteArray"}],"returntype":"ByteArray"}],"events":[{"name":"ErrorMsg","parameters":[{"name":"id","type":"ByteArray"},{"name":"error","type":"String"}],"returntype":"Void"},{"name":"Push","parameters":[{"name":"id","type":"ByteArray"},{"name":"msg","type":"String"},{"name":"args","type":"ByteArray"}],"returntype":"Void"}]}'

    def make_commit(self, issuerOntid: str, subjectOntid: str, claimId: str, payer: str,
                    gas_limit: int, gas_price: int):
        abi = json.loads(self.abi, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        abi_info = AbiInfo(abi.hash, abi.entrypoint, abi.functions, abi.events)
        func = abi_info.get_function("Commit")
        func.set_params_value(bytes(claimId.encode()), bytes(issuerOntid.encode()), bytes(subjectOntid.encode()))
        params = BuildParams.serialize_abi_function(func)
        unix_timenow = int(time())
        return Transaction(0, 0xd1, unix_timenow, gas_price, gas_limit, Address.decodeBase58(payer).to_array(),
                           params, bytearray(), [], bytearray())
