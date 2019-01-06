# Ontology Python SDK

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9078ef6584424280b8d6b75556976f94)](https://www.codacy.com/app/NashMiao/ontology-python-sdk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ontio/ontology-python-sdk/&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/9078ef6584424280b8d6b75556976f94)](https://www.codacy.com/app/NashMiao/ontology-python-sdk?utm_source=github.com&utm_medium=referral&utm_content=ontio/ontology-python-sdk/&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.com/ontio/ontology-python-sdk.svg?branch=master)](https://travis-ci.com/ontio/ontology-python-sdk)
[![pypi-w](https://img.shields.io/pypi/wheel/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)
[![docs](https://img.shields.io/badge/docs-yes-brightgreen.svg)](https://apidoc.ont.io/pythonsdk/#introduction)
[![pypi-pyversions](https://img.shields.io/pypi/pyversions/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)
[![pypi-v](https://img.shields.io/pypi/v/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)

## Introduction

The Ontology official Python SDK is a comprehensive SDK which is based on `Python3.6`. Currently, it supports local wallet management, digital identity management, digital asset management, deployment and invoke for smart contract, the calling of OEP4, and communication with the Ontology blockchain. The future will also support more functions and applications.

## Preparations

Installation requires a Python 3.7 or later environment.

```bash
pip install ontology-python-sdk
```

## Interface

Read more in the [ontology-python-sdk API document](https://apidoc.ont.io/pythonsdk/).

### Network

This is an API set that allows you to interact with an Ontology nodes.

|       | Main Function                         |
| :---: | :------------------------------------ |
|   1   | get_version()                         |
|   2   | get_balance()                         |
|   3   | get_allowance()                       |
|   4   | get_gas_price()                       |
|   5   | get_network_id()                      |
|   6   | get_node_count()                      |
|   7   | get_block_count()                     |
|   8   | get_block_height()                    |
|   9   | get_block_by_hash()                   |
|  10   | get_block_by_height()                 |
|  11   | get_current_block_hash()              |
|  12   | get_block_hash_by_height()            |
|  13   | get_storage()                         |
|  14   | get_smart_contract()                  |
|  15   | get_smart_contract_event_by_tx_hash() |
|  16   | get_smart_contract_event_by_height()  |

### Wallet

This is an API set that allows you to handle with wallet account in the form of `AccountData`.

|       | Main Function    |
| :---: | :--------------- |
| 1     | add_account()    |
| 2     | remove_account() |

**Note**: This package has **NOT** been audited and might potentially be unsafe. Take precautions to clear memory properly, store the private keys safely, and test transaction receiving and sending functionality properly before using in production!

### Account

This is an API set that allows you to generate Ontology accounts and sign transactions and data.

|       | Main Function                      |
| :---: | :--------------------------------- |
| 1     | export_wif()                       |
| 2     | get_signature_scheme()             |
| 3     | get_public_key_bytes()             |
| 4     | get_private_key_bytes()            |
| 5     | get_public_key_hex()               |
| 6     | get_public_key_bytes()             |
| 7     | get_private_key_from_wif()         |
| 8     | get_gcm_decoded_private_key()      |
| 9     | export_gcm_encrypted_private_key() |
| 10    | get_address_hex()                  |
| 11    | get_address_hex_reverse()          |
| 12    | get_address_base58()               |
| 13    | generate_signature()               |

**Note**: This package has **NOT** been audited and might potentially be unsafe. Take precautions to clear memory properly, store the private keys safely, and test transaction receiving and sending functionality properly before using in production!

### Identity

This is an API set that allows you to generate **Ontology Digital Identity.**

|       | Main Function                        |
| :---: | :----------------------------------- |
| 1     | parse_ddo()                          |
| 2     | send_get_ddo()                       |
| 3     | new_get_ddo_transaction()            |
| 4     | new_add_recovery_transaction()       |
| 5     | new_add_attribute_transaction()      |
| 6     | new_add_public_key_transaction()     |
| 7     | new_remove_public_key_transaction()  |
| 8     | new_registry_ont_id_transaction()    |
| 9     | new_remove_attribute_transaction()   |
| 10    | send_add_recovery_transaction()      |
| 11    | send_add_attribute_transaction()     |
| 12    | send_add_public_key_transaction()    |
| 13    | send_registry_ont_id_transaction()   |
| 14    | remove_public_key() |
| 15    | send_remove_attribute_transaction()  |
| 16    | send_add_public_key_by_recovery()    |
| 17    | sign_transaction()                   |
| 18    | add_sign_transaction()               |
| 19    | add_multi_sign_transaction()         |
| 20    | get_merkle_proof()                   |
| 21    | get_transaction_by_tx_hash()                |
| 22    | send_raw_transaction()               |
| 23    | send_raw_transaction_pre_exec()      |

**Note**: This package has **NOT** been audited and might potentially be unsafe. Take precautions to clear memory properly, store the private keys safely, and test transaction receiving and sending functionality properly before using in production!

### AccountManager

This is an API set that allows you to manage your multiple account in an wallet file.

|       | Main Function                     |
| :---: | :-------------------------------- |
| 1     | import_account()                  |
| 2     | create_account()                  |
| 3     | create_account_from_private_key() |
| 4     | get_account()                     |
| 5     | get_accounts()                    |
| 6     | get_default_account()             |
| 7     | get_default_account_address()     |
| 8     | set_default_account_by_index()    |
| 9     | set_default_account_by_address()  |

**Note**: This package has **NOT** been audited and might potentially be unsafe. Take precautions to clear memory properly, store the private keys safely, and test transaction receiving and sending functionality properly before using in production!

### IdentityManager

This is an API set that allows you to manage your multiple identity in an wallet file.

|       | Main Function                      |
| :---: | :--------------------------------- |
| 1     | create_identity()                  |
| 2     | import_identity()                  |
| 3     | create_identity_from_private_key() |

**Note**: This package has **NOT** been audited and might potentially be unsafe. Take precautions to clear memory properly, store the private keys safely, and test transaction receiving and sending functionality properly before using in production!

### Asset

The `Asset` package allows you to interact with Ontology Native Digital Asset(ONT, ONG) easily.

|       | Main Function                   |
| :---: | :------------------------------ |
| 1     | query_name()                    |
| 2     | query_symbol()                  |
| 3     | query_balance()                 |
| 4     | query_decimals()                |
| 5     | query_allowance()               |
| 6     | query_unbound_ong()             |
| 7     | get_asset_address()             |
| 8     | new_approve_transaction()       |
| 9     | new_transfer_transaction()      |
| 10    | new_transfer_from_transaction() |
| 11    | new_withdraw_ong_transaction()  |
| 12    | send_transfer()                 |
| 13    | send_approve()                  |
| 14    | send_transfer_from()            |
| 15    | send_withdraw_ong_transaction() |

### ABI

The `ABI` package allows you to interact with a deployed smart contract easily.

|       | Main Function      |
| :---: | :----------------- |
| 1     | get_function]()    |
| 2     | get_parameter()    |
| 3     | set_params_value() |

### OEP4

The `OEP4` package allows you to interact with an deployed Ontology OEP4 smart contract easily.

|       | Main Function      |
| :---: | :----------------- |
| 1     | init()             |
| 2     | get_name()         |
| 3     | get_symbol()       |
| 4     | get_decimal()      |
| 5     | get_total_supply() |
| 6     | approve()          |
| 7     | allowance()        |
| 8     | balance_of()       |
| 9     | transfer()         |
| 10    | transfer_multi()   |
| 11    | transfer_from()    |

**Note**: This package has **NOT** been audited and might potentially be unsafe. Take precautions to clear memory properly, store the private keys safely, and test transaction receiving and sending functionality properly before using in production!

### Utils

The `Utils` package provides utility functions for `Ontology Dapps` and other `Ontology-Python-Sdk` packages.

|       | Main Function       |
| :---: | :------------------ |
| 1     | get_random_hex_str()    |
| 2     | get_asset_address() |
| 3     | get_random_bytes()  |

## Site

* https://ont.io/

## License

The Ontology library (i.e. all code outside of the cmd directory) is licensed under the GNU Lesser General Public License v3.0, also included in our repository in the License file.
