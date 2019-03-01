#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path, environ

from ontology.ont_sdk import OntologySdk

password = environ['SDK_TEST_PASSWORD']
sdk = OntologySdk()
sdk.rpc.connect_to_test_net()
sdk.restful.connect_to_test_net()
sdk.websocket.connect_to_test_net()
wallet_path = path.join(path.dirname(__file__), 'test_wallet.json')
wallet_manager = sdk.wallet_manager
wallet_manager.open_wallet(wallet_path, is_create=False)
acct1 = wallet_manager.get_account_by_b58_address('ANDfjwrUroaVtvBguDtrWKRMyxFwvVwnZD', password)
acct2 = wallet_manager.get_account_by_b58_address('Af1n2cZHhMZumNqKgw9sfCNoTWu9de4NDn', password)
acct3 = wallet_manager.get_account_by_b58_address('AXJZrP1jBRo398ebfyemsDxDaThsxcXGMk', password)
acct4 = wallet_manager.get_account_by_b58_address('APvHaLmJUMdAHiVbFHGi11gnFpuK6ozD5j', password)
ont_id_1 = 'did:ont:ANDfjwrUroaVtvBguDtrWKRMyxFwvVwnZD'
identity1 = wallet_manager.get_identity_by_ont_id(ont_id_1)
identity1_ctrl_acct = wallet_manager.get_control_account_by_index(ont_id_1, 0, password)
ont_id_2 = 'did:ont:AP8XfCUo7w3qM4b5gyQU8AEyRSwgtDFSzp'
identity2 = wallet_manager.get_identity_by_ont_id(ont_id_2)
identity2_ctrl_acct = wallet_manager.get_control_account_by_index(ont_id_2, 0, password)
wallet_manager.save()
