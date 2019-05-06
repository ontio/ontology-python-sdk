#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from os import path, environ

from ontology.exception.exception import SDKException
from ontology.sdk import Ontology

password = environ['SDK_TEST_PASSWORD']
sdk = Ontology()
sdk.rpc.connect_to_test_net()
sdk.aio_rpc.connect_to_test_net()
sdk.restful.connect_to_test_net()
sdk.aio_restful.connect_to_test_net()
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
no_panic_exception = ['balance insufficient', 'ConnectTimeout', 'already in the tx pool']


def not_panic_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SDKException as e:
            not_panic = ['balance insufficient', 'ConnectTimeout', 'unknown transaction']
            if not any(x in e.args[1] for x in not_panic):
                raise e

    return wrapper
