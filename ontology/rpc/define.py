RPC_GET_VERSION = "getversion"
RPC_GET_TRANSACTION = "getrawtransaction"
RPC_SEND_TRANSACTION = "sendrawtransaction"
RPC_GET_BLOCK = "getblock"
RPC_GET_BLOCK_COUNT = "getblockcount"
RPC_GET_BLOCK_HASH = "getblockhash"
RPC_GET_CURRENT_BLOCK_HASH = "getbestblockhash"
RPC_GET_BALANCE = "getbalance"
RPC_GET_ALLOWANCE = "getallowance"
RPC_GET_SMART_CONTRACT_EVENT = "getsmartcodeevent"
RPC_GET_STORAGE = "getstorage"
RPC_GET_SMART_CONTRACT = "getcontractstate"
RPC_GET_GENERATE_BLOCK_TIME = "getgenerateblocktime"
RPC_GET_MERKLE_PROOF = "getmerkleproof"
SEND_EMERGENCY_GOV_REQ = "sendemergencygovreq"
GET_BLOCK_ROOT_WITH_NEW_TX_ROOT = "getblockrootwithnewtxroot"

# JsonRpc version
JSON_RPC_VERSION = "2.0"

# JsonRpcRequest object in rpc
JsonRpcRequest = {"jsonrpc": "", "id": "", "method": "", "params": ""}
