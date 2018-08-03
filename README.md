<h1 align="center">Python SDK For Ontology</h1>

<p align="center" class="version">Version 0.1.0</p>

<!-- TOC -->

- [Introduction](#introduction)
- [Preparations](#preparations)
- [RPC interface function list](#rpc-interface-function-list)
- [Wallet function list](#wallet-function-list)
  - [Digit account](#digit-account)
  - [Digit identity](#digit-identity)
- [Asset function list](#asset-function-list)
  - [Native digit asset](#native-digit-asset)
- [Identity function list](#identity-function-list)
  - [ONT ID](#ont-id)
- [Contribution](#contribution)
- [Site](#site)
- [License](#license)

<!-- /TOC -->


## Introduction
Ontology Python SDK function consists of four parts, RPC interface, wallet, asset, and identity. For RPC interface, it is responsible to interact with the Ontology blockchain, including querying and sending transactions. For wallet, it manages wallet file and store the encrypted private key of the asset account and identity. The function of asset can transfer ONT/ONG, check account balance, withdraw ONT/ONG and so on. The function of identity can send request to register ONT ID and get DDO object. In addition to these four parts, SDK also support constructing, deploying, and invoking a smart contract. 

## Preparations

To avoid installing wrong package, we recommend you to run
the Python script to install all the third-party package that our SDK is needed in the `setup_package` folder.

```python
python3 ./setup_package/cn_install.py
```

or

```python
python3 ./setup_package/install.py
```

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
 |   14 | get_merkle_proof (transaction_hash)   |  
 |   15 | send_raw_transaction (transaction)    |  
 |  16 | send_raw_transaction_preexec (transaction)  | 


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
 |   9 | send_transfer_from(self, asset: str, sender: Account, from_addr: str, recv_addr: str, amount: int,payer: Account, gas_limit: int, gas_price: int)|         
 
## Identity function list 

### ONT ID

 |     | Main   Function |          
 |:-----|:--------|
 |   1 | new_registry_ontid_transaction(self, ontid: str, pubkey: str, payer: str, gas_limit: int, gas_price: int)      |
|    2 | new_add_attribute_transaction(self, ontid: str, pubkey: str, attris: list, payer: str, gas_limit: int, gas_price: int)  |  
|    3 | new_remove_attribute_transaction(self, ontid: str, pubkey: bytearray, path: str, payer: str, gas_limit: int, gas_price: int) |  
 |   4 | new_add_pubkey_transaction(self, ontid: str, pubkey_or_recovery: bytes, new_pubkey: bytes, payer: str,gas_limit: int, gas_price: int)      |  
 |   5 | new_remove_pubkey_transaction(self, ontid: str, pubkey_or_recovery: bytes, remove_pubkey: bytes, payer: str, gas_limit: int, gas_price: int)                       |  
 |   6 | new_add_recovery_transaction(self, ontid: str, pubkey: bytes, recovery: str, payer: str, gas_limit: int,gas_price: int)    | 
 |   7 | new_get_ddo_transaction(self, ontid: str)      |                                                                                                 
 |   8 | parse_ddo(self, ontid: str, ddo: str)                 | 
                                                                                                   


## Contribution

Can I contribute patches to Ontology project?

Yes! Please open a pull request with signed-off commits. We appreciate your help!

You can also send your patches as emails to the developer mailing list.
Please join the Ontology mailing list or forum and talk to us about it.

Either way, if you don't sign off your patches, we will not accept them.
This means adding a line that says "Signed-off-by: Name <email>" at the
end of each commit, indicating that you wrote the code and have the right
to pass it on as an open source patch.

Also, please write good git commit messages.  A good commit message
looks like this:

Header line: explain the commit in one line (use the imperative)

Body of commit message is a few lines of text, explaining things
in more detail, possibly giving some background about the issue
being fixed, etc etc.

The body of the commit message can be several paragraphs, and
please do proper word-wrap and keep columns shorter than about
74 characters or so. That way "git log" will show things
nicely even when it's indented.

Make sure you explain your solution and why you're doing what you're
doing, as opposed to describing what you're doing. Reviewers and your
future self can read the patch, but might not understand why a
particular solution was implemented.

Reported-by: whoever-reported-it
Signed-off-by: Your Name <youremail@yourhost.com>


## Site

* https://ont.io/

## License

The Ontology library (i.e. all code outside of the cmd directory) is licensed under the GNU Lesser General Public License v3.0, also included in our repository in the License file.
