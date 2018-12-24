from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class ClaimRecord(object):
    def __init__(self, sdk, hex_contract_address: str = '', is_rpc: bool = True):
        self.__sdk = sdk
        if isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            self.__hex_contract_address = hex_contract_address
        else:
            self.__hex_contract_address = '36bb5c053b6b839c8f6b923fe852f91239b9fccc'
        if is_rpc:
            self.__network = sdk.rpc
        else:
            self.__network = sdk.restful

    @property
    def hex_contract_address(self):
        return self.__hex_contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address):
        if isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            self.__hex_contract_address = hex_contract_address

    def send_commit(self, claim_id: str, issuer_acct: Account, subject_ont_id: str, payer_acct: Account, gas_limit: int,
                    gas_price: int):
        if gas_limit < 0 or gas_price < 0:
            raise SDKException(ErrorCode.other_error('Gas limit less than 0.'))
        if gas_price < 0:
            raise SDKException(ErrorCode.other_error('Gas price less than 0.'))
        func = InvokeFunction('Commit')
        func.set_params_value(claim_id, issuer_acct.get_address_bytes(), subject_ont_id)
        tx_hash = self.__network.send_neo_vm_transaction(self.__hex_contract_address, issuer_acct, payer_acct,
                                                         gas_limit, gas_price, func, False)
        return tx_hash
