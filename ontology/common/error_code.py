#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


class ErrorCode:
    @staticmethod
    def get_error(code: int, msg: str) -> json:
        data = dict()
        data['error'] = code
        data['desc'] = msg
        return data

    # account error
    invalid_params = get_error.__func__(51001, "Account Error, invalid params")
    unsupported_key_type = get_error.__func__(51002, "Account Error,unsupported key type")
    invalid_message = get_error.__func__(51003, "Account Error, invalid message")
    without_private = get_error.__func__(51004, "Account Error, account without private key cannot generate signature")
    invalid_sm2_signature = get_error.__func__(51005,
                                               "Account Error, invalid SM2 signature parameter, ID (String) excepted")
    account_invalid_input = get_error.__func__(51006, "Account Error, account invalid input")
    account_without_public_key = get_error.__func__(51007,
                                                    "Account Error, account without public key cannot verify signature")
    unknown_key_type = get_error.__func__(51008, "Account Error, unknown key type")
    null_input = get_error.__func__(51009, "Account Error, null input")
    invalid_data = get_error.__func__(51010, "Account Error, invalid data")
    decoded_3bytes_error = get_error.__func__(51011, "Account Error, decoded 3 bytes error")
    decode_pri_key_passphrase_error = get_error.__func__(51012, "Account Error, decode prikey passphrase error.")
    pri_key_length_error = get_error.__func__(51013, "Account Error, Prikey length error")
    encrypted_pri_key_error = get_error.__func__(51014, "Account Error, Prikey length error")
    encrypted_pri_key_address_password_err = get_error.__func__(51015,
                                                                "Account Error, encrypted private key address password not match.")
    encrypt_private_key_error = get_error.__func__(51016, "Account Error, encrypt private key error,")

    param_length_err = get_error.__func__(52001, "Uint256 Error,param length error")
    checksum_not_validate = get_error.__func__(52002, "Base58 Error,Checksum does not validate")
    input_too_short = get_error.__func__(52003, "Base58 Error,Input too short")
    unknown_curve = get_error.__func__(52004, "Curve Error,unknown curve")
    unknown_curve_label = get_error.__func__(52005, "Curve Error,unknown curve label")
    unknown_asymmetric_key_type = get_error.__func__(52006, "keyType Error,unknown asymmetric key type")
    invalid_signature_data = get_error.__func__(52007,
                                                "Signature Error, invalid signature data: missing the ID parameter for SM3withSM2")
    invalid_signature_data_len = get_error.__func__(52008, "Signature Error, invalid signature data length")
    malformed_signature = get_error.__func__(52009, "Signature Error, malformed signature")
    unsupported_signature_scheme = get_error.__func__(52010, "Signature Error, unsupported signature scheme:")
    data_signature_err = get_error.__func__(52011, "Signature Error, Data signature error.")
    un_support_operation = get_error.__func__(52012, "Address Error, UnsupportedOperationException")

    # Core Error
    tx_deserialize_error = get_error.__func__(53001, "Core Error, Transaction deserialize failed")
    block_deserialize_error = get_error.__func__(53002, "Core Error, Block deserialize failed")

    # merkle error
    merkle_verifier_err = get_error.__func__(54001, "Wrong params: the tree size is smaller than the leaf index")
    target_hashes_err = get_error.__func__(54002, "targetHashes error")

    @staticmethod
    def constructed_root_hash_err(msg: str) -> json:
        return ErrorCode.get_error(54003, "Other Error, " + msg)

    assert_failed_hash_full_tree = get_error.__func__(54004, "assert failed in hash full tree")
    left_tree_full = get_error.__func__(54005, "left tree always full")

    # SmartCodeTx Error
    send_raw_tx_error = get_error.__func__(58001, "SmartCodeTx Error, sendRawTransaction error")
    type_error = get_error.__func__(58002, "SmartCodeTx Error, type error")

    # OntIdTx Error
    null_code_hash = get_error.__func__(58003, "OntIdTx Error, null codeHash")
    param_error = get_error.__func__(58004, "param error")

    @staticmethod
    def param_err(msg: str):
        return ErrorCode.get_error(58005, msg)

    did_null = get_error.__func__(58006, "OntIdTx Error, SendDid or receiverDid is null in metaData")
    not_exist_claim_issuer = get_error.__func__(58007, "OntIdTx Error, Not exist claim issuer")
    not_found_public_key_id = get_error.__func__(58008, "OntIdTx Error, not found PublicKeyId")
    public_key_id_err = get_error.__func__(58009, "OntIdTx Error, PublicKeyId err")
    block_height_not_match = get_error.__func__(58010, "OntIdTx Error, BlockHeight not match")
    nodes_not_match = get_error.__func__(58011, "OntIdTx Error, nodes not match")
    result_is_null = get_error.__func__(58012, "OntIdTx Error, result is null")
    create_ont_id_claim_err = get_error.__func__(58013, "OntIdTx Error, createOntIdClaim error")
    verify_ont_id_claim_err = get_error.__func__(58014, "OntIdTx Error, verifyOntIdClaim error")
    write_var_bytes_error = get_error.__func__(58015, "OntIdTx Error, writeVarBytes error")
    send_raw_transaction_pre_exec = get_error.__func__(58016, "OntIdTx Error, sendRawTransaction PreExec error")
    sender_amt_not_eq_password_amt = get_error.__func__(58017,
                                                        "OntIdTx Error, senders amount is not equal password amount")
    expire_err = get_error.__func__(58017, "OntIdTx Error, expire is wrong")

    @staticmethod
    def get_status_err(msg: str) -> json:
        return ErrorCode.get_error(58017, "GetStatus Error," + msg)

    # OntAsset Error
    asset_name_error = get_error.__func__(58101, "OntAsset Error, asset name error")
    did_error = get_error.__func__(58102, "OntAsset Error, Did error")
    null_pk_id = get_error.__func__(58103, "OntAsset Error, null pkId")
    null_claim_id = get_error.__func__(58104, "OntAsset Error, null claimId")
    amount_error = get_error.__func__(58105, "OntAsset Error, amount or gas is less than or equal to zero")
    param_length_not_same = get_error.__func__(58105, "OntAsset Error, param length is not the same")

    # RecordTx Error
    null_key_or_value = get_error.__func__(58201, "RecordTx Error, null key or value")
    null_key = get_error.__func__(58202, "RecordTx Error, null  key")

    # OntSdk Error
    web_socket_not_init = get_error.__func__(58301, "OntSdk Error, web socket not init")
    conn_restful_not_init = get_error.__func__(58302, "OntSdk Error, connRestful not init")

    # abi error
    set_params_value_value_num_error = get_error.__func__(58401, "AbiFunction Error, setParamsValue value num error")
    connect_url_err = get_error.__func__(58402, "Interfaces Error, connect error:")

    @staticmethod
    def connect_err(msg: str) -> json:
        return ErrorCode.get_error(58403, "connect error: " + msg)

    # WalletManager Error
    get_account_by_address_err = get_error.__func__(58501, "WalletManager Error, getAccountByAddress err")

    @staticmethod
    def other_error(msg: str) -> json:
        return ErrorCode.get_error(59000, "Other Error, " + msg)
