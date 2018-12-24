from os import path

from ontology.ont_sdk import OntologySdk

password = input('password: ')
sdk = OntologySdk()
wallet_path = path.join(path.dirname(__file__), 'test_wallet.json')
wallet_manager = sdk.wallet_manager
wallet_manager.open_wallet(wallet_path)
acct1 = wallet_manager.get_account('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', password)
acct2 = wallet_manager.get_account('AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve', password)
acct3 = wallet_manager.get_account('Ad4H6AB3iY7gBGNukgBLgLiB6p3v627gz1', password)
acct4 = wallet_manager.get_account('AHX1wzvdw9Yipk7E9MuLY4GGX4Ym9tHeDe', password)
wallet_manager.save()
