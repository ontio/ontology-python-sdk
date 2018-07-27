from ontology.crypto.scrypt import Scrypt
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity
import json
from collections import namedtuple
from ontology.wallet.control import Control


class WalletData(object):
    def __init__(self, name="MyWallet", version="1.1", create_time="", default_ontid="", default_account_address="",
                 scrypt=Scrypt(), identities=[], accounts=[]):
        self.name = name
        self.version = version
        self.create_time = create_time
        self.default_ontid = default_ontid
        self.default_account_address = default_account_address
        self.scrypt = scrypt  # Scrypt class
        self.identities = identities  # a list of Identity class
        self.accounts = accounts  # a list of AccountData class

    def clone(self):
        wallet = WalletData()
        wallet.name = self.name
        wallet.version = self.version
        wallet.scrypt = self.scrypt
        wallet.accounts = self.accounts
        wallet.identities = self.identities
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

    @staticmethod
    def load(wallet_path):
        r = json.load(open(wallet_path, "r"), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        scrypt = Scrypt(r.scrypt.n, r.scrypt.r, r.scrypt.p, r.scrypt.dk_len)
        identities = []

        for index in range(len(r.identities)):
            control = [Control(id=r.identities[index].controls[0].id,
                               algorithm=r.identities[index].controls[0].algorithm,
                               param=r.identities[index].controls[0].param,
                               key=r.identities[index].controls[0].key,
                               address=r.identities[index].controls[0].address,
                               salt=r.identities[index].controls[0].salt,
                               enc_alg=r.identities[index].controls[0].enc_alg,
                               hash_value=r.identities[index].controls[0].hash_value,
                               public_key=r.identities[index].controls[0].public_key)]
            temp = Identity(r.identities[index].ontid, r.identities[index].label, r.identities[index].lock, control)
            identities.append(temp)
        accounts = []

        for index in range(len(r.accounts)):
            temp = AccountData(label=r.accounts[index].label, public_key=r.accounts[index].public_key,
                               sign_scheme=r.accounts[index].sign_scheme, is_default=r.accounts[index].is_default,
                               lock=r.accounts[index].lock, address=r.accounts[index].address,
                               algorithm=r.accounts[index].algorithm, param=r.accounts[index].param,
                               key=r.accounts[index].key, enc_alg=r.accounts[index].enc_alg,
                               salt=r.accounts[index].salt, hash_value=r.accounts[index].hash_value)
            accounts.append(temp)

        res = WalletData(r.name, r.version, r.create_time, r.default_ontid, r.default_account_address, scrypt,
                         identities, accounts)
        return res

    def save(self, wallet_path):
        json.dump(self, open(wallet_path, "w"), default=lambda obj: obj.__dict__, indent=4)

    def add_identity(self, id: Identity):
        self.identities.append(id)

    def remove_identity(self, ontid):
        for index in range(len(self.identities)):
            if self.identities[index].ontid == ontid:
                del self.identities[index]
