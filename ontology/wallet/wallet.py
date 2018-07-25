from ontology.crypto.scrypt import Scrypt
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity
import json


class WalletData(object):
    def __init__(self, name="MyWallet", version="1.1", create_time="", default_ontid="", default_account_address="",
                 scrypt=Scrypt(), identities=[], accounts=[], extra=""):
        self.name = name
        self.version = version
        self.create_time = create_time
        self.default_ontid = default_ontid
        self.default_account_address = default_account_address
        self.scrypt = scrypt  # Scrypt class
        self.identities = identities  # a list of Identity class
        self.accounts = accounts  # a list of AccountData class
        self.extra = extra

    def clone(self):
        wallet = WalletData()
        wallet.name = self.name
        wallet.version = self.version
        wallet.scrypt = self.scrypt
        wallet.accounts = self.accounts
        wallet.identities = self.identities
        wallet.extra = self.extra
        return wallet

    def add_account(self, acc: AccountData):
        self.accounts.append(acc)

    def remove_account(self, address: str):
        account, index = self.get_account_by_address(address)
        if index == -1:
            return
        del self.accounts[index]

    def get_account_by_index(self, index: int):
        if index < 0 or index >= len(self.accounts):
            return ValueError("wrong account index")
        return self.accounts[index]

    def get_account_by_address(self, address: str):
        for index in range(len(self.accounts)):
            if self.accounts[index].keypair.address == address:
                return self.accounts[index], index
        return None, -1

    def load(self, wallet_path):
        with open(wallet_path, 'r') as f:
            content = f.read()
        return json.loads(content)

    def save(self, wallet_path):
        json.dump(self, open(wallet_path, "w+"), default=lambda obj: obj.__dict__, indent=4)

    def add_identity(self, id: Identity):
        self.identities.append(id)

    def remove_identity(self, ontid):
        for index in range(len(self.identities)):
            if self.identities[index].ontid == ontid:
                del self.identities[index]



if __name__ == '__main__':
    w=WalletData()
    print(w.identities)
