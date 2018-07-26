from ontology.crypto.scrypt import Scrypt
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity
import json
from collections import namedtuple
from ontology.wallet.control import ProtectedKey, Control


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

    @staticmethod
    def load(wallet_path):
        r = json.load(open(wallet_path, "r"), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        scrypt = Scrypt(r.scrypt.n, r.scrypt.r, r.scrypt.p, r.scrypt.dk_len)
        identities = []
        for index in range(len(r.identities)):
            prot = ProtectedKey(r.identities[index].controls[0].protected_key.address,
                                r.identities[index].controls[0].protected_key.enc_alg,
                                r.identities[index].controls[0].protected_key.key,
                                r.identities[index].controls[0].protected_key.algorithm,
                                r.identities[index].controls[0].protected_key.salt,
                                r.identities[index].controls[0].protected_key.hash_value,
                                r.identities[index].controls[0].protected_key.param)
            c = [Control(r.identities[index].controls[0].id, r.identities[index].controls[0].publicKey, prot)]
            temp = Identity(r.identities[index].ontid, r.identities[index].label, r.identities[index].lock, c,
                            r.identities[index].extra, r.identities[index].is_default)
            identities.append(temp)
        accounts = []
        for index in range(len(r.accounts)):
            prot = ProtectedKey(r.accounts[index].protected_key.address,
                                r.accounts[index].protected_key.enc_alg,
                                r.accounts[index].protected_key.key,
                                r.accounts[index].protected_key.algorithm,
                                r.accounts[index].protected_key.salt,
                                r.accounts[index].protected_key.hash_value,
                                r.accounts[index].protected_key.param)
            temp = AccountData(prot, r.accounts[index].label, r.accounts[index].public_key,
                               r.accounts[index].sign_scheme, r.accounts[index].is_default, r.accounts[index].lock)
            accounts.append(temp)

        res = WalletData(r.name, r.version, r.create_time, r.default_ontid, r.default_account_address, scrypt,
                         identities, accounts, r.extra)

        return res

    def save(self, wallet_path):
        json.dump(self, open(wallet_path, "w"), default=lambda obj: obj.__dict__, indent=4)

    def add_identity(self, id: Identity):
        self.identities.append(id)

    def remove_identity(self, ontid):
        for index in range(len(self.identities)):
            if self.identities[index].ontid == ontid:
                del self.identities[index]
