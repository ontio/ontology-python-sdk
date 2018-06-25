RPC_GET_VERSION = "getversion"
RPC_GET_TRANSACTION = "getrawtransaction"
RPC_SEND_TRANSACTION = "sendrawtransaction"
RPC_GET_BLOCK = "getblock"
RPC_GET_BLOCK_COUNT = "getblockcount"
RPC_GET_BLOCK_HASH = "getblockhash"
RPC_GET_CURRENT_BLOCK_HASH = "getbestblockhash"
RPC_GET_ONT_BALANCE = "getbalance"
RPC_GET_SMART_CONTRACT_EVENT = "getsmartcodeevent"
RPC_GET_STORAGE = "getstorage"
RPC_GET_SMART_CONTRACT = "getcontractstate"
RPC_GET_GENERATE_BLOCK_TIME = "getgenerateblocktime"
RPC_GET_MERKLE_PROOF = "getmerkleproof"

# JsonRpc version
JSON_RPC_VERSION = "2.0"


# JsonRpcRequest object in rpc
class JsonRpcRequest(object):
    def __init__(self):
        self.version = ''
        self.id = ''
        self.method = ''
        self.params = []


# JsonRpcResponse object response for JsonRpcRequest
class JsonRpcResponse(object):
    def __init__(self):
        self.id = ''
        self.error = 0
        self.desc = ''
        self.result = ''


# BalanceRsp response object for balance request
class BalanceRsp(object):
    def __init__(self):
        self.ont = ''
        self.ong = ''
        self.ongApprove = ''
