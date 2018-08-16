from ontology.crypto.scrypt import Scrypt
from ontology.wallet.account import AccountData
from ontology.wallet.identity import Identity


class WalletData(object):
    def __init__(self, name: str = "MyWallet", version: str = "1.1", create_time: str = "", default_id: str = "",
                 default_address="", scrypt: Scrypt = None, identities: list = None, accounts: list = None):
        if scrypt is None:
            scrypt = Scrypt()
        if identities is None:
            identities = list()
        if accounts is None:
            accounts = list()
        self.name = name
        self.version = version
        self.create_time = create_time
        self.default_ont_id = default_id
        self.default_account_address = default_address
        self.scrypt = scrypt
        self.identities = identities
        self.accounts = accounts

    def clone(self):
        wallet = WalletData()
        wallet.name = self.name
        wallet.version = self.version
        wallet.create_time = self.create_time
        wallet.default_ont_id = self.default_ont_id
        wallet.default_account_address = self.default_account_address
        wallet.scrypt = self.scrypt
        wallet.accounts = self.accounts
        wallet.identities = self.identities
        return wallet

    def add_account(self, acc: AccountData):
        self.accounts.append(acc)

    def remove_account(self, address: str):
        account = self.get_account_by_address(address)
        if account is None:
            raise Exception("no the account")
        return self.accounts.remove(account)

    def get_accounts(self):
        return self.accounts

    def get_account_by_index(self, index: int):
        if index < 0 or index >= len(self.accounts):
            return ValueError("wrong account index")
        return self.accounts[index]

    def get_account_by_address(self, address: str):
        for index in range(len(self.accounts)):
            if self.accounts[index].address == address:
                return self.accounts[index]
        return None

    def add_identity(self, id: Identity):
        for identity in self.identities:
            if identity.ont_id == id.ont_id:
                raise Exception("ont id is equal.")
        self.identities.append(id)

    def remove_identity(self, ont_id):
        for index in range(len(self.identities)):
            if self.identities[index].ont_id == ont_id:
                del self.identities[index]
                break

    def get_identity_by_ontid(self, ont_id: str):
        for identity in self.identities:
            if identity.ont_id == ont_id:
                return identity
        return None
