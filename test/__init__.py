#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path, environ

from ontology.ont_sdk import OntologySdk

password = environ['SDK_TEST_PASSWORD']
sdk = OntologySdk()
wallet_path = path.join(path.dirname(__file__), 'test_wallet.json')
wallet_manager = sdk.wallet_manager
wallet_manager.open_wallet(wallet_path)
acct1 = wallet_manager.get_account('ANDfjwrUroaVtvBguDtrWKRMyxFwvVwnZD', password)
acct2 = wallet_manager.get_account('Af1n2cZHhMZumNqKgw9sfCNoTWu9de4NDn', password)
acct3 = wallet_manager.get_account('AXJZrP1jBRo398ebfyemsDxDaThsxcXGMk', password)
acct4 = wallet_manager.get_account('APvHaLmJUMdAHiVbFHGi11gnFpuK6ozD5j', password)
wallet_manager.save()
