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


# Balance object for account
class Balance(object):
    def __init__(self):
        self.ont = 0
        self.ong = 0


# SmartContactEvent object for event of transaction
class SmartContactEvent(object):
    def __init__(self):
        self.tx_hash = ''
        self.state = bytes()
        self.gas_consumed = 0

    class NotifyEventInfo(object):
        def __init__(self):
            self.contract_address = ''
            self.states = ''


# MerkleProof return structure
class MerkleProof(object):
    merkle_proof_type = ''
    transactions_root = ''
    block_height = 0
    cur_block_root = ''
    cur_block_height = 0
    target_hashes = []  # string array
