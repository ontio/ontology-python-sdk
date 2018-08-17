from time import time
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.common.define import ZERO_ADDRESS
from ontology.core.deploy_transaction import DeployTransaction
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.core.transaction import Transaction
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_contract.claim_record import ClaimRecord


class NeoVm(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def claim_record(self):
        return ClaimRecord(self.__sdk)

    def send_transaction(self, contract_address: bytearray, acct: Account, payer_acct: Account, gas_limit: int,
                         gas_price: int, func: AbiFunction, pre_exec: bool):
        params = bytearray()
        if func is not None:
            params = BuildParams.serialize_abi_function(func)
        if pre_exec:
            tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 0, 0)
            if acct is not None:
                self.__sdk.sign_transaction(tx, acct)
            return self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        unix_time_now = int(time())
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_acct.get_address().to_array(),
                         params, bytearray(), [], bytearray())
        self.__sdk.sign_transaction(tx, acct)
        if payer_acct is not None and acct.get_address_base58() != payer_acct.get_address_base58():
            self.__sdk.add_sign_transaction(tx, payer_acct)
        return self.__sdk.rpc.send_raw_transaction(tx)

    @staticmethod
    def make_deploy_transaction(code_str: str, need_storage: bool, name: str, code_version: str, author: str,
                                email: str, desp: str, payer: str, gas_limit: int, gas_price: int):
        unix_time_now = int(time())
        deploy_tx = DeployTransaction()
        deploy_tx.payer = Address.b58decode(payer)
        deploy_tx.attributes = bytearray()
        deploy_tx.nonce = unix_time_now
        deploy_tx.code = bytearray.fromhex(code_str)
        deploy_tx.code_version = code_version
        deploy_tx.version = 0
        deploy_tx.need_storage = need_storage
        deploy_tx.name = name
        deploy_tx.author = author
        deploy_tx.email = email
        deploy_tx.gas_limit = gas_limit
        deploy_tx.gas_price = gas_price
        deploy_tx.description = desp
        return deploy_tx

    @staticmethod
    def make_invoke_transaction(code_addr: bytearray, params: bytearray, payer: bytes,
                                gas_limit: int, gas_price: int):
        params += bytearray([0x67])
        params += code_addr
        invoke_tx = InvokeTransaction()
        invoke_tx.version = 0
        invoke_tx.sigs = bytearray()
        invoke_tx.attributes = bytearray()
        unix_time_now = int(time())
        invoke_tx.nonce = unix_time_now
        invoke_tx.code = params
        invoke_tx.gas_limit = gas_limit
        invoke_tx.gas_price = gas_price
        if isinstance(payer, bytes) and payer != b'':
            invoke_tx.payer = payer
        else:
            invoke_tx.payer = Address(ZERO_ADDRESS).to_array()
        return invoke_tx
