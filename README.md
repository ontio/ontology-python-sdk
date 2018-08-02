<h1 align="center">Ontology SDK Function List</h1>

<p align="center" class="version">Version 1.0.0</p>

- [Introduction](#introduction)
- [RPC interface function list](#rpc-interface-function-list)
- [Wallet function list](#wallet-function-list)
  - [Digit account](#digit-account)
  - [Digit identity](#digit-identity)
- [Asset function list](#asset-function-list)
  - [Native digit asset](#native-digit-asset)


## Introduction
Ontology Python SDK function consists of four parts, RPC interface, wallet, asset, and identity. For RPC interface, it is responsible to interact with the Ontology blockchain, including querying and sending transactions. For wallet, it manages wallet file and store the encrypted private key of the asset account and identity. The function of asset can transfer ONT/ONG, check account balance, withdraw ONT/ONG and so on. The function of identity can send request to register ONT ID and get DDO object. In addition to these four parts, SDK also support constructing, deploying, and invoking a smart contract. 



## RPC interface function list


 |     | Main   Function |     
 |:-----|:--------|
 |   1 | get_version()              |  
 |    2 | get_block_by_hash (block_hash)                    |  
 |    3 | get_block_by_height (block_height)                   |  
 |    4 | get_block_count ()               |  
 |    5 | get_current_block_hash ()                 |  
 |    6 | get_block_hash_by_height (block_height)                    |  
 |    7 | get_balance (account_address)            |                             
 |    8 | get_allowance (account_address)  |  
 |   9 | get_storage (contract_address, key)              |  
 |   10 | get_smart_contract_event_by_txhash (transaction_hash)  |  
 |   11 | get_smart_contract_event_by_block (block_height)               |  
 |   12 | get_raw_transaction (transaction_hash)         |  
 |   13 | get_smart_contract (contract_address)     | 
 |   14 | get_generate_block_time ()          |  
 |   15 | get_merkle_proof (transaction_hash)   |  
 |   16 | send_raw_transaction (transaction)    |  
 |  17 | send_raw_transaction_preexec (transaction)  | 


## Wallet function list

The wallet function includes three parts, digit account, digit identity, and mnemonics and kestore interface. Mnemonics and kestore interface will be supported in the future.
 
### Digit account

 |     | Main   Function |    
 |:-----|:--------|
|   1 | import_account(self, label: str, encrypted_prikey: str, pwd: str, base58_addr: str, salt: bytes)   |   
|   2 | create_account(self, label: str, pwd: str, salt: bytes, priv_key: bytes, account_flag: bool)   |
|   3 | create_random_account(self, label: str, pwd: str)|   
|   4 | create_account_from_prikey(self, label: str, pwd: str, private_key: bytes)    |   
|   5 | get_account(self, address: str, pwd: str)    |   


### Digit identity

 |     | Main   Function |       
 |:-----|:--------|
|   1 | import_identity(self, label: str, encrypted_privkey: str, pwd: str, salt: bytes, address: str) |   
|   2 | create_identity(self, label: str, pwd: str, salt: bytes, private_key: bytes)          |   
|   3 | create_identity_from_prikey(self, label: str, pwd: str, private_key: bytes)       |   
 |  4 | create_random_identity(self, label: str, pwd: str)           |    

   
## Asset function list

The asset includes native digit asset and Nep-5 smart constract digit asset. Nep-5 smart constract will be supported in the future.

### Native digit asset


 |     | Main   Function |         
 |:-----|:--------|
 |    1 | new_transfer_transaction(asset: str, from_addr: str, to_addr: str, amount: int, payer: str, gas_limit: int, gas_price: int)   |  
 |   2 | query_balance(self, asset: str, addr: str)                                                     |  
 |   3 | query_allowance(self, asset: str, from_addr: str, to_addr: str)                                      |  
 |   4 | query_name(self, asset: str)    |  
 |   5 | query_symbol(self, asset: str) |  
 |   6 | query_decimals(self, asset: str)                                                                   |  
 |   7 | send_withdraw_ong_transaction(self, claimer: Account, recv_addr: str, amount: int, payer: Account, gas_limit: int, gas_price: int) |                                                              
 |   8 | send_approve(self, asset: str, sender: Account, recv_addr: str, amount: int, payer: Account, gas_limit: int, gas_price: int) |                                                                       
 |   9 | send_transfer_from(self, asset: str, send_addr: str, from_addr: str, recv_addr: str, amount: int,payer: str, gas_limit: int, gas_price: int)|                                                                 

