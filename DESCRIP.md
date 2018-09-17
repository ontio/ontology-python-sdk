# Python SDK For Ontology

## Introduction

Ontology Python SDK function consists of four parts, RPC interface, wallet, asset, and identity. For RPC interface, it is responsible to interact with the Ontology blockchain, including querying and sending transactions. For wallet, it manages wallet file and store the encrypted private key of the asset account and identity. The function of asset can transfer ONT/ONG, check account balance, withdraw ONT/ONG and so on. The function of identity can send request to register ONT ID and get DDO object. In addition to these four parts, SDK also support constructing, deploying, and invoking a smart contract. 

## Preparations


Installation requires a Python 3.7 or later environment.

```bash
pip install ontology-python-sdk
```

## RPC interface function list

 |      | Main   Function                                        |
 | :--- | :----------------------------------------------------- |
 | 1    | get_version()                                          |
 | 2    | get_block_by_hash (block_hash)                         |
 | 3    | get_block_by_height (block_height)                     |
 | 4    | get_block_count ()                                     |
 | 5    | get_current_block_hash ()                              |
 | 6    | get_block_hash_by_height (block_height)                |
 | 7    | get_balance (account_address)                          |
 | 8    | get_allowance (account_address)                        |
 | 9    | get_storage (contract_address, key)                    |
 | 10   | get_smart_contract_event_by_tx_hash (transaction_hash) |
 | 11   | get_smart_contract_event_by_height (block_height)      |
 | 12   | get_raw_transaction (transaction_hash)                 |
 | 13   | get_smart_contract (contract_address)                  |
 | 14   | get_merkle_proof (transaction_hash)                    |
 | 15   | send_raw_transaction (transaction)                     |
 | 16   | send_raw_transaction_pre_exec (transaction)            |
 | 17   | get_node_count ()                                      |
 | 18   | get_gas_price ()                                       |

## Wallet function list

The wallet function includes three parts, digit account, digit identity, and mnemonics and kestore interface. Mnemonics and kestore interface will be supported in the future.

### Digit account

 |      | Main   Function                                                                           |
 | :--- | :---------------------------------------------------------------------------------------- |
 | 1    | import_account(label: str, encrypted_pri_key: str, pwd: str, base58_addr: str, salt: str) |
 | 2    | create_account(label: str, pwd: str, salt: str, priv_key: bytes, account_flag: bool)      |
 | 3    | create_account_from_private_key(label: str, pwd: str, private_key: bytes)                 |
 | 4    | get_account(address: str, pwd: str)                                                       |
 | 5    | get_accounts()                                                                            |
 | 6    | get_default_account()                                                                     |
 | 7    | set_default_account_by_address(b58_address: str)                                          |
 | 8    | set_default_account_by_index(index: int)                                                  |
 | 9    | get_default_account_address()                                                             |

### Digit identity

 |      | Main   Function                                                                        |
 | :--- | :------------------------------------------------------------------------------------- |
 | 1    | import_identity(label: str, encrypted_pri_key: str, pwd: str, salt: str, address: str) |
 | 2    | create_identity(label: str, pwd: str, salt: str, private_key: bytes)                   |
 | 3    | create_identity_from_private_key(label: str, pwd: str, private_key: bytes)             |

## Asset function list

The asset includes native digit asset and Nep-5 smart constract digit asset. Nep-5 smart constract will be supported in the future.

### Native digit asset


 |      | Main   Function                                                                                                                                |
 | :--- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
 | 1    | new_transfer_transaction(asset: str, from_address: str, to_address: str, amount: int, payer: str, gas_limit: int, gas_price: int)              |
 | 2    | query_balance(asset: str, addr: str)                                                                                                           |
 | 3    | query_allowance(asset: str, b58_from_address: str, b58_to_address: str)                                                                        |
 | 4    | query_name(asset: str)                                                                                                                         |
 | 5    | query_symbol(asset: str)                                                                                                                       |
 | 6    | query_decimals(asset: str)                                                                                                                     |
 | 7    | send_withdraw_ong_transaction(claimer: Account, recv_addr: str, amount: int, payer: Account, gas_limit: int, gas_price: int)                   |
 | 8    | send_approve(asset: str, sender: Account, recv_addr: str, amount: int, payer: Account, gas_limit: int, gas_price: int)                         |
 | 9    | send_transfer_from(asset: str, sender: Account, from_address: str, recv_addr: str, amount: int,payer: Account, gas_limit: int, gas_price: int) |
 
## Identity function list 

### ONT ID

 |      | Main   Function                                                                                                                         |
 | :--- | :-------------------------------------------------------------------------------------------------------------------------------------- |
 | 1    | new_registry_ont_id_transaction(ont_id: str, pubkey: str, payer: str, gas_limit: int, gas_price: int)                                    |
 | 2    | new_add_attribute_transaction(ont_id: str, pubkey: str, attris: list, payer: str, gas_limit: int, gas_price: int)                       |
 | 3    | new_remove_attribute_transaction(ont_id: str, pubkey: bytearray, path: str, payer: str, gas_limit: int, gas_price: int)                 |
 | 4    | new_add_public_key_transaction(ont_id: str, pubkey_or_recovery: bytes, new_pubkey: bytes, payer: str,gas_limit: int, gas_price: int)        |
 | 5    | new_remove_public_key_transaction(ont_id: str, pubkey_or_recovery: bytes, remove_pubkey: bytes, payer: str, gas_limit: int, gas_price: int) |
 | 6    | new_add_recovery_transaction(ont_id: str, pubkey: bytes, recovery: str, payer: str, gas_limit: int,gas_price: int)                      |
 | 7    | new_get_ddo_transaction(ont_id: str)                                                                                                    |
 | 8    | parse_ddo(ont_id: str, ddo: str)                                                                                                        |

## Site

* https://ont.io/

## License

The Ontology library (i.e. all code outside of the cmd directory) is licensed under the GNU Lesser General Public License v3.0, also included in our repository in the License file.
