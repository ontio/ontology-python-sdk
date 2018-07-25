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
    def __init__(self, wallet_path, scheme=SignatureScheme.SHA256withECDSA):
        self.__wallet_path = wallet_path
        self.__scheme = scheme
        self.__wallet_file = WalletData()
        self.__wallet_in_mem = WalletData()

    def open_wallet(self):
        if is_file_exist(self.__wallet_path) is False:
            # create a new wallet file
            self.__wallet_file.create_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.__wallet_file.save(self.__wallet_path)
        # wallet file exists now
        self.__wallet_file = self.read_data_from_file(self.__wallet_path)
        self.__wallet_in_mem = self.read_data_from_file(self.__wallet_path)
        return self.__wallet_file

    def read_data_from_file(self, wallet_path):
        file = open(wallet_path, 'r', encoding='utf-8')
        content = json.load(file)
        return content

    def get_wallet(self):
        return self.__wallet_in_mem

    def write_wallet(self):
        self.__wallet_in_mem.save(self.__wallet_path)

    def reset_wallet(self):
        self.__wallet_in_mem = self.__wallet_file.clone()
        return self.__wallet_in_mem

    def get_signature_scheme(self):
        return self.__scheme

    def set_signature_scheme(self, scheme):
        self.__scheme = scheme

    def import_identity(self, label: str, encrypted_privkey: str, pwd, salt: bytearray, address: str):
        encrypted_privkey = base64.decodebytes(encrypted_privkey.encode())
        private_key = Account.get_gcm_decoded_private_key(encrypted_privkey, pwd, address, salt,
                                                          Scrypt().get_n(),
                                                          self.__scheme)

        info = self.create_identity(label, pwd, salt, private_key)
        private_key = None
        for index in range(len(self.__wallet_in_mem.identities)):
            if self.__wallet_in_mem.identities[index].ontid == info.ontid:
                return self.__wallet_in_mem.identities[index]
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
        info = self.create_identity("", pwd, hex_to_bytes(private_key))
        private_key = None
        for index in range(len(self.__wallet_in_mem.identities)):
            if self.__wallet_in_mem.identities[index].ontid == info.ontid:
                return self.__wallet_in_mem.identities[index]
        return None

    def create_account(self, label, pwd, salt, priv_key, account_flag: bool):
        account = Account(priv_key, self.__scheme)
        # initialization
        if self.__scheme == SignatureScheme.SHA256withECDSA:
            prot = ProtectedKey(algorithm="ECDSA", enc_alg="aes-256-gcm", hash_value="SHA256withECDSA",
                                param={"curve": "secp256r1"})
            acct = AccountData(protected_key=prot, sign_scheme="SHA256withECDSA")  # todo init
        else:
            raise ValueError("scheme type is error")
        # set key
        if pwd != None:
            acct.protected_key.key = account.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
            pwd = None
        else:
            acct.protected_key.key = account.serialize_private_key().hex()

        acct.protected_key.address = Address.address_from_bytes_pubkey(account.get_address().to_array()).to_base58()
        # set label
        if label == None or label == "":
            label = str(uuid.uuid4())[0:8]
        if account_flag:
            for index in range(len(self.__wallet_in_mem.accounts)):
                if acct.protected_key.address == self.__wallet_in_mem.accounts[index].protected_key.address:
                    raise ValueError("wallet account exists")

            if len(self.__wallet_in_mem.accounts) == 0:
                acct.is_default = True
                self.__wallet_in_mem.default_account_address = acct.protected_key.address
            acct.label = label
            acct.protected_key.salt = salt
            self.__wallet_in_mem.accounts.append(acct)
        else:
            for index in range(len(self.__wallet_in_mem.identities)):
                if self.__wallet_in_mem.identities[index].ontid == did_ont + acct.protected_key.address:
                    raise ValueError("wallet identity exists")

        idt = Identity()
        idt.ontid = did_ont + acct.protected_key.address
        idt.label = label
        if len(self.__wallet_in_mem.identities) == 0:
            idt.is_default = True
            self.__wallet_in_mem.default_ontid = idt.ontid
        prot = ProtectedKey(key=acct.protected_key.key, algorithm="ECDSA", param={"curve": "secp256r1"}, salt=salt,
                            address=acct.protected_key.address)
        ctl = Control(id="keys-1", protected_key=prot)
        idt.controls.append(ctl)
        self.__wallet_in_mem.identities.append(idt)
        return account

    def import_account(self, label, encrypted_prikey, pwd, address, salt):
        private_key = Account.get_gcm_decoded_private_key(encrypted_prikey, pwd, address, salt, Scrypt().get_n(),
                                                          self.__scheme)
        info = self.create_account_info(label, pwd, salt, hex_to_bytes(private_key))
        private_key, pwd = None, None
        for index in range(len(self.__wallet_in_mem.accounts)):
            if info.address_base58 == self.__wallet_in_mem.accounts[index].protected_key.address:
                return self.__wallet_in_mem.accounts[index]
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
        info = self.create_account_info("", pwd, salt, hex_to_bytes(private_key))
        for index in range(len(self.__wallet_in_mem.accounts)):
            if info.address_base58 == self.__wallet_in_mem.accounts[index].protected_key.address:
                return self.__wallet_in_mem.accounts[index]
        return None

    def get_account_by_address(self, address: Address, pwd, salt):
        for index in range(len(self.__wallet_in_mem.accounts)):
            if self.__wallet_in_mem.accounts[index].protected_key.address == address.to_base58():
                key = self.__wallet_in_mem.accounts[index].protected_key.key
                addr = self.__wallet_in_mem.accounts[index].protected_key.address
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.__scheme)
                return Account(hex_to_bytes(private_key), self.__scheme)

        for index in range(len(self.__wallet_in_mem.identities)):
            if self.__wallet_in_mem.identities[index].ontid == did_ont + address.to_base58():
                addr = self.__wallet_in_mem.identities[index].ontid.replace(did_ont, "")
                key = self.__wallet_in_mem.identities[index].controls[0].key
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.__scheme)
                return Account(hex_to_bytes(private_key), self.__scheme)
        return None


if __name__ == '__main__':
    wallet_path = '/Users/zhaoxavi/test.txt'
    w = WalletManager(wallet_path=wallet_path)
    res = w.open_wallet()
    print(res)
