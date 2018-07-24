from ontology.wallet.scrypt import ScryptParam
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity
from ontology.crypto.encrypt import reencrypt_private_key
import json


class WalletData(object):
    def __init__(self, name="MyWallet", version="1.1", scrypt=ScryptParam(), identities=None,
                 accounts=[], extra=""):
        self.name = name
        self.version = version
        self.scrypt = scrypt  # ScryptParam class
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

    def to_low_security(self, passwords):
        low_security = ScryptParam(4096, 8, 8, 64)
        self.reencrypt(passwords, low_security)

    def to_default_security(self, passwords):
        self.reencrypt(passwords, None)

    def reencrypt(self, passwords, param):
        if len(passwords) != len(self.accounts):
            raise ValueError("no enough passwords for the accounts")
        keys = []
        for index in range(len(self.accounts)):
            res = reencrypt_private_key(self.accounts[index].protected_key, passwords[index], passwords[index],
                                        self.scrypt, param)
            keys.append(res)

        for index in range(len(keys)):
            self.accounts[index].set_key_pair(keys[index])

        if param != None:
            self.scrypt = param
        else:
            self.scrypt = ScryptParam()

    def add_identity(self, id: Identity):
        self.identities.append(id)

    def remove_identity(self, ontid):
        for index in range(len(self.identities)):
            if self.identities[index].ontid == ontid:
                del self.identities[index]
