"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""


class ErrorCode:
    @staticmethod
    def get_error(code: int, msg: str) -> dict:
        data = dict()
        data['error'] = code
        data['desc'] = msg
        return data

    @staticmethod
    def unpack_error(msg: str) -> dict:
        return ErrorCode.get_error(10001, f'Binary Reader Error, {msg}')

    @staticmethod
    def read_byte_error(msg: str) -> dict:
        return ErrorCode.get_error(10002, f'Binary Reader Error, {msg}')

    @staticmethod
    def params_type_error(msg: str) -> dict:
        return ErrorCode.get_error(20000, 'Interface Error, ' + msg)

    require_bool_params = get_error.__func__(20001, 'Interface Error, the type of parameter should be int.')
    require_int_params = get_error.__func__(20002, 'Interface Error, the type of parameter should be int.')
    require_float_params = get_error.__func__(20003, 'Interface Error, the type of parameter should be float.')
    require_str_params = get_error.__func__(20004, 'Interface Error, the type of parameter should be str.')
    require_bytes_params = get_error.__func__(20005, 'Interface Error, the type of parameter should be bytes.')
    require_list_params = get_error.__func__(20006, 'Interface Error, the type of parameter should be list.')
    require_tuple_params = get_error.__func__(20007, 'Interface Error, the type of parameter should be tuple.')
    require_set_params = get_error.__func__(20008, 'Interface Error, the type of parameter should be set.')
    require_dict_params = get_error.__func__(20009, 'Interface Error, the type of parameter should be dict.')
    require_control_params = get_error.__func__(20010, 'Interface Error, a Control object is required.')
    require_acct_params = get_error.__func__(20011, 'Interface Error, a Account object is required.')

    invalid_b64_claim_data = get_error.__func__(21001, 'Interface Error, invalid base64 encode claim.')
    invalid_blk_proof = get_error.__func__(21002, 'Interface Error, invalid blockchain proof.')
    invalid_merkle_root = get_error.__func__(21003, 'Interface Error, invalid merkle root.')
    invalid_claim_type = get_error.__func__(21004, 'Interface Error, invalid claim type.')
    invalid_claim_alg = get_error.__func__(21004, 'Interface Error, invalid claim algorithm.')
    invalid_claim_head_params = get_error.__func__(21005, 'Interface Error, invalid claim head parameter.')

    @staticmethod
    def invalid_ont_id_format(ont_id: str):
        return ErrorCode.get_error(30001, f'Identity Error, invalid OntId: {ont_id}')

    invalid_ont_id_type = get_error.__func__(30002, 'Identity Error, invalid type of OntId')

    @staticmethod
    def invalid_wallet_path(path: str):
        return ErrorCode.get_error(40001, f'WalletManager Error, invalid path: {path}')

    @staticmethod
    def invalid_contract_address(contract_address: str):
        return ErrorCode.get_error(50001, f'NeoVm Error, invalid hex contract address: {contract_address}')

    @staticmethod
    def invalid_tx_hash(tx_hash: str):
        return ErrorCode.get_error(60001, f'Network Error, invalid TxHash: {tx_hash}')

    @staticmethod
    def connect_timeout(url: str):
        return ErrorCode.get_error(60002, f'Network Error, ConnectionError: {url}')

    hd_index_out_of_range = get_error.__func__(70001, 'Crypto Error, index is out of range: 0 <= index <= 2**32 - 1')
    hd_root_key_not_master_key = get_error.__func__(70002, "Crypto Error, root_key must be a master key if m is the first element of the path")

    unknown_curve_label = get_error.__func__(70003, "Crypto Error, unknown curve label")

    invalid_private_key = get_error.__func__(100001, 'Account Error, invalid private key.')
    unsupported_key_type = get_error.__func__(100002, 'Account Error, unsupported key type.')

    invalid_message = get_error.__func__(100003, "Account Error, invalid message")
    without_private = get_error.__func__(100004, "Account Error, account without private key cannot generate signature")
    invalid_sm2_signature = get_error.__func__(100005,
                                               "Account Error, invalid SM2 signature parameter, ID (String) excepted")
    account_invalid_input = get_error.__func__(100006, "Account Error, account invalid input")
    account_without_public_key = get_error.__func__(100007,
                                                    "Account Error, account without public key cannot verify signature")
    null_input = get_error.__func__(100009, "Account Error, null input")
    invalid_data = get_error.__func__(100010, "Account Error, invalid data")
    decoded_3bytes_error = get_error.__func__(100011, "Account Error, decoded 3 bytes error")
    decode_pri_key_passphrase_error = get_error.__func__(100012, "Account Error, decode prikey passphrase error.")
    pri_key_length_error = get_error.__func__(100013, "Account Error, Prikey length error")
    encrypted_pri_key_error = get_error.__func__(100014, "Account Error, Prikey length error")
    encrypted_pri_key_address_password_err = get_error.__func__(100015,
                                                                "Account Error, encrypted private key address password not match.")
    encrypt_private_key_error = get_error.__func__(100016, "Account Error, encrypt private key error,")
    decrypt_encrypted_private_key_error = get_error.__func__(100017,
                                                             "Account Error, decrypt encrypted private key error.")

    param_length_err = get_error.__func__(200001, "Uint256 Error,param length error")
    checksum_not_validate = get_error.__func__(200002, "Base800 Error,Checksum does not validate")
    input_too_short = get_error.__func__(200003, "Base800 Error,Input too short")
    unknown_curve = get_error.__func__(200004, "Curve Error,unknown curve")
    unknown_asymmetric_key_type = get_error.__func__(200006, "keyType Error,unknown asymmetric key type")
    invalid_signature_data = get_error.__func__(200007,
                                                "Signature Error, invalid signature data: missing the ID parameter for SM3withSM2")
    invalid_signature_data_len = get_error.__func__(200008, "Signature Error, invalid signature data length")
    malformed_signature = get_error.__func__(200009, "Signature Error, malformed signature")
    unsupported_signature_scheme = get_error.__func__(200010, "Signature Error, unsupported signature scheme:")
    data_signature_err = get_error.__func__(200011, "Signature Error, Data signature error.")
    un_support_operation = get_error.__func__(200012, "Address Error, UnsupportedOperationException")

    # Core Error
    tx_deserialize_error = get_error.__func__(300001, "Core Error, Transaction deserialize failed")
    block_deserialize_error = get_error.__func__(300002, "Core Error, Block deserialize failed")

    # merkle error
    merkle_verifier_err = get_error.__func__(400001, "Wrong params: the tree size is smaller than the leaf index")
    target_hashes_err = get_error.__func__(400002, "targetHashes error")

    @staticmethod
    def constructed_root_hash_err(msg: str) -> dict:
        return ErrorCode.get_error(400003, "Other Error, " + msg)

    assert_failed_hash_full_tree = get_error.__func__(400004, "assert failed in hash full tree")
    left_tree_full = get_error.__func__(400005, "left tree always full")

    # SmartCodeTx Error
    send_raw_tx_error = get_error.__func__(800001, "SmartCodeTx Error, sendRawTransaction error")
    type_error = get_error.__func__(800002, "SmartCodeTx Error, type error")

    # OntIdTx Error
    null_code_hash = get_error.__func__(800003, "OntIdTx Error, null codeHash")
    param_error = get_error.__func__(800004, "param error")

    @staticmethod
    def param_err(msg: str):
        return ErrorCode.get_error(800005, msg)

    did_null = get_error.__func__(800006, "OntIdTx Error, SendDid or receiverDid is null in metaData")
    not_exist_claim_issuer = get_error.__func__(800007, "OntIdTx Error, Not exist claim issuer")
    not_found_public_key_id = get_error.__func__(800008, "OntIdTx Error, not found PublicKeyId")
    public_key_id_err = get_error.__func__(800009, "OntIdTx Error, PublicKeyId err")
    block_height_not_match = get_error.__func__(800010, "OntIdTx Error, BlockHeight not match")
    nodes_not_match = get_error.__func__(800011, "OntIdTx Error, nodes not match")
    result_is_null = get_error.__func__(800012, "OntIdTx Error, result is null")
    create_ont_id_claim_err = get_error.__func__(800013, "OntIdTx Error, createOntIdClaim error")
    verify_ont_id_claim_err = get_error.__func__(800014, "OntIdTx Error, verifyOntIdClaim error")
    write_var_bytes_error = get_error.__func__(800015, "OntIdTx Error, writeVarBytes error")
    send_raw_transaction_pre_exec = get_error.__func__(800016, "OntIdTx Error, sendRawTransaction PreExec error")
    sender_amt_not_eq_password_amt = get_error.__func__(800017,
                                                        "OntIdTx Error, senders amount is not equal password amount")
    expire_err = get_error.__func__(800017, "OntIdTx Error, expire is wrong")

    @staticmethod
    def get_status_err(msg: str) -> dict:
        return ErrorCode.get_error(800017, "GetStatus Error," + msg)

    # OntAsset Error
    asset_name_error = get_error.__func__(800101, "OntAsset Error, asset name error")
    did_error = get_error.__func__(800102, "OntAsset Error, Did error")
    null_pk_id = get_error.__func__(800103, "OntAsset Error, null pkId")
    null_claim_id = get_error.__func__(800104, "OntAsset Error, null claimId")
    amount_error = get_error.__func__(800105, "OntAsset Error, amount or gas is less than or equal to zero")
    param_length_not_same = get_error.__func__(800105, "OntAsset Error, param length is not the same")

    # RecordTx Error
    null_key_or_value = get_error.__func__(800201, "RecordTx Error, null key or value")
    null_key = get_error.__func__(800202, "RecordTx Error, null  key")

    # OntSdk Error
    web_socket_not_init = get_error.__func__(800301, "OntSdk Error, web socket not init")
    conn_restful_not_init = get_error.__func__(800302, "OntSdk Error, connRestful not init")

    # abi error
    set_params_value_value_num_error = get_error.__func__(800401, "AbiFunction Error, setParamsValue value num error")
    connect_url_err = get_error.__func__(800402, "Interfaces Error, connect error:")

    @staticmethod
    def connect_err(msg: str) -> dict:
        return ErrorCode.get_error(800403, "connect error: " + msg)

    # WalletManager Error
    get_account_by_address_err = get_error.__func__(800501, "WalletManager Error, get account by address error")
    get_default_account_err = get_error.__func__(800502, "WalletManager Error, get default account error")
    get_account_by_index_err = get_error.__func__(800503, 'WalletManager Error, get account by index error')

    @staticmethod
    def other_error(msg: str) -> dict:
        return ErrorCode.get_error(59000, "Other Error, " + msg)
