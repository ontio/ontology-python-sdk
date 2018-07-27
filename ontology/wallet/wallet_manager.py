from ontology.wallet.wallet import WalletData
from ontology.utils.util import is_file_exist
from ontology.crypto.SignatureScheme import SignatureScheme
from datetime import datetime
import json
import base64
from ontology.crypto.scrypt import Scrypt
from ontology.account.account import Account
from ontology.wallet.account import AccountData, AccountInfo
from ontology.wallet.control import ProtectedKey, Control
from ontology.common.address import Address
import uuid
from ontology.wallet.identity import Identity, did_ont, IdentityInfo
from ontology.utils.util import hex_to_bytes, get_random_bytes


class WalletManager(object):
    def __init__(self, scheme=SignatureScheme.SHA256withECDSA):
        self.scheme = scheme
        self.wallet_file = WalletData()
        self.wallet_in_mem = WalletData()

    def open_wallet(self, wallet_path):
        if is_file_exist(wallet_path) is False:
            # create a new wallet file
            self.wallet_file.create_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.wallet_file.save(wallet_path)
        # wallet file exists now
        self.wallet_file = self.load(wallet_path)
        self.wallet_in_mem = self.wallet_file
        return self.wallet_file

    def load(self, wallet_path):
        res = WalletData.load(wallet_path)
        return res

    def save(self, wallet_path):
        json.dump(self.wallet_in_mem, open(wallet_path, "w"), default=lambda obj: obj.__dict__, indent=4)

    def get_wallet(self):
        return self.wallet_in_mem

    def write_wallet(self, wallet_path):
        self.wallet_in_mem.save(wallet_path)
        self.wallet_file = self.wallet_in_mem
        return self.wallet_file

    def reset_wallet(self):
        self.wallet_in_mem = self.wallet_file.clone()
        return self.wallet_in_mem

    def get_signature_scheme(self):
        return self.scheme

    def set_signature_scheme(self, scheme):
        self.scheme = scheme

    def import_identity(self, label: str, encrypted_privkey: str, pwd, salt: bytes, address: str):
        encrypted_privkey = base64.decodebytes(encrypted_privkey.encode())
        private_key = Account.get_gcm_decoded_private_key(encrypted_privkey, pwd, address, salt,
                                                          Scrypt().get_n(), self.scheme)
        info = self.create_identity(label, pwd, salt, private_key)
        private_key = None
        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ontid == info.ontid:
                return self.wallet_in_mem.identities[index]
        return None

    def create_identity(self, label: str, pwd, salt, private_key):
        acct = self.create_account(label, pwd, salt, private_key, False)
        info = IdentityInfo()
        info.ontid = did_ont + Address.address_from_bytes_pubkey(acct.get_address().to_array()).to_base58()
        info.pubic_key = acct.serialize_public_key().hex()
        info.private_key = acct.serialize_private_key().hex()
        info.prikey_wif = acct.export_wif()
        info.encrypted_prikey = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        return info

    def create_identity_from_prikey(self, pwd, private_key):
        salt = get_random_bytes(16)
        info = self.create_identity("", pwd, salt, private_key)
        private_key = None
        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ontid == info.ontid:
                return self.wallet_in_mem.identities[index]
        return None

    def create_account(self, label, pwd, salt, priv_key, account_flag: bool):
        account = Account(priv_key, self.scheme)
        # initialization
        if self.scheme == SignatureScheme.SHA256withECDSA:
            prot = ProtectedKey(algorithm="ECDSA", enc_alg="aes-256-gcm", hash_value="SHA256withECDSA",
                                param={"curve": "secp256r1"})
            acct = AccountData(protected_key=prot, sign_scheme="SHA256withECDSA")
        else:
            raise ValueError("scheme type is error")
        # set key
        if pwd != None:
            acct.protected_key.key = account.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n()).decode()
            print(acct.protected_key.key)
            pwd = None
        else:
            acct.protected_key.key = account.serialize_private_key().hex()

        acct.protected_key.address = Address.address_from_bytes_pubkey(
            account.get_address().to_array()).to_base58()
        # set label
        if label == None or label == "":
            label = str(uuid.uuid4())[0:8]
        if account_flag:
            for index in range(len(self.wallet_in_mem.accounts)):
                if acct.protected_key.address == self.wallet_in_mem.accounts[index].protected_key.address:
                    raise ValueError("wallet account exists")

            if len(self.wallet_in_mem.accounts) == 0:
                acct.is_default = True
                self.wallet_in_mem.default_account_address = acct.protected_key.address
            acct.label = label
            acct.protected_key.salt = base64.b64encode(salt).decode()
            self.wallet_in_mem.accounts.append(acct)
        else:
            for index in range(len(self.wallet_in_mem.identities)):
                if self.wallet_in_mem.identities[index].ontid == did_ont + acct.protected_key.address:
                    raise ValueError("wallet identity exists")

        idt = Identity()
        idt.ontid = did_ont + acct.protected_key.address
        idt.label = label
        if len(self.wallet_in_mem.identities) == 0:
            idt.is_default = True
            self.wallet_in_mem.default_ontid = idt.ontid
        prot = ProtectedKey(key=acct.protected_key.key, algorithm="ECDSA", param={"curve": "secp256r1"},
                            salt=base64.b64encode(salt).decode(),
                            address=acct.protected_key.address)
        ctl = Control(id="keys-1", protected_key=prot)
        idt.controls.append(ctl)
        self.wallet_in_mem.identities.append(idt)
        return account

    def import_account(self, label, encrypted_prikey, pwd, base58_addr: str, salt):
        private_key = Account.get_gcm_decoded_private_key(encrypted_prikey, pwd, base58_addr, salt, Scrypt().get_n(),
                                                          self.scheme)
        info = self.create_account_info(label, pwd, salt, hex_to_bytes(private_key))
        private_key, pwd = None, None
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].protected_key.address:
                return self.wallet_in_mem.accounts[index]
        return None

    def create_account_info(self, label, pwd, salt, private_key):
        acct = self.create_account(label, pwd, salt, private_key, True)
        info = AccountInfo()
        info.address_base58 = Address.address_from_bytes_pubkey(acct.serialize_public_key()).to_base58()
        info.public_key = acct.serialize_public_key().hex()
        info.private_key = acct.serialize_private_key().hex()
        info.prikey_wif = acct.export_wif()
        info.encrypted_prikey = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        return info

    def create_account_from_prikey(self, pwd, private_key):
        salt = get_random_bytes(16)
        info = self.create_account_info("", pwd, salt, private_key)
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].protected_key.address:
                return self.wallet_in_mem.accounts[index]
        return None

    def get_account_by_address(self, address: Address, pwd, salt):
        for index in range(len(self.wallet_in_mem.accounts)):
            if self.wallet_in_mem.accounts[index].protected_key.address == address.to_base58():
                key = self.wallet_in_mem.accounts[index].protected_key.key
                addr = self.wallet_in_mem.accounts[index].protected_key.address
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.scheme)
                return Account(hex_to_bytes(private_key), self.scheme)

        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ontid == did_ont + address.to_base58():
                addr = self.wallet_in_mem.identities[index].ontid.replace(did_ont, "")
                key = self.wallet_in_mem.identities[index].controls[0].key
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.scheme)
                return Account(hex_to_bytes(private_key), self.scheme)
        return None


if __name__ == '__main__':
    # test wallet load and save
    private_key = '99bbd375c745088b372c6fc2ab38e2fb6626bc552a9da47fc3d76baa21537a1b'
    scheme = SignatureScheme.SHA256withECDSA
    acct0 = Account(private_key, scheme)
    encrypted_key = 'T3uep1USsEqiJbP4O+CKsl2AWfpGjvuVSKxpoKeGdEUa0nfLHHjIq3G4xOz7a4PC'
    wallet_path = '/Users/zhaoxavi/test.txt'
    w = WalletManager()
    w.open_wallet(wallet_path)
    salt = get_random_bytes(16)
    #w.import_account("123", encrypted_key, '234', acct0.get_address_base58(), salt)
    # w.create_account_from_prikey("123", private_key)
    # w.create_account("123", "567", salt, private_key, True)
    a=Address.decodeBase58("ASBNLVgyuB7hG2Qt6YcmVLuizNUmkZtyRH").to_base58()
    print(a.__dict__)
    #w.save(wallet_path)
    # print((w.wallet_in_mem.accounts[0].protected_key.__dict__))
