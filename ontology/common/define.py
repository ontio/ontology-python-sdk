VERSION_TRANSACTION = bytes([0])
VERSION_CONTRACT_ONT = bytes([0])
VERSION_CONTRACT_ONG = bytes([0])

NATIVE_TRANSFER = "transfer"
NATIVE_TRANSFER_FROM = "transferFrom"
NATIVE_APPROVE = "approve"
NATIVE_ALLOWANCE = "allowance"

# NeoVM invokes a smart contract return type
neo_vm_return_type = bytes
NEOVM_TYPE_BOOL = 1
NEOVM_TYPE_INTEGER = 2
NEOVM_TYPE_BYTE_ARRAY = 3
NEOVM_TYPE_STRING = 4

UINT256_SIZE = 32


# Balance object for account
class Balance(object):
    def __init__(self, ont=0, ong=0):
        self.ont = ont
        self.ong = ong


# Response object for balance request
class BalanceRsp(object):
    def __init__(self, ont="", ong=""):
        self.ont = ont
        self.ong = ong


# SmartContactEvent object for event of transaction
class SmartContactEvent(object):
    def __init__(self, tx_hash="", state=bytearray(), gas_consumed=0):
        self.tx_hash = tx_hash
        self.state = state
        self.gas_consumed = gas_consumed

    class NotifyEventInfo(object):
        contract_address = ""
        states = ""


# MerkleProof return structure
class MerkleProof(object):
    def __init__(self, merkle_proof_type='', transactions_root="", block_height=0, cur_block_root="",
                 cur_block_height=0, target_hashes=[]):
        self.merkle_proof_type = merkle_proof_type
        self.transactions_root = transactions_root
        self.block_height = block_height
        self.cur_block_root = cur_block_root
        self.cur_block_height = cur_block_height
        self.target_hashes = target_hashes  # string array
