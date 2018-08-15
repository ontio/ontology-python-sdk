from ontology.wallet.wallet import WalletData
from ontology.utils.util import is_file_exist
from ontology.crypto.signature_scheme import SignatureScheme
from datetime import datetime
import json
import base64
from ontology.crypto.scrypt import Scrypt
from ontology.account.account import Account
from ontology.wallet.account import AccountData
from ontology.wallet.account_info import AccountInfo
from ontology.wallet.control import Control
from ontology.common.address import Address
import uuid
from binascii import a2b_hex
from ontology.wallet.identity import Identity, did_ont
from ontology.wallet.identity_info import IdentityInfo
from ontology.utils.util import get_random_bytes, get_random_str
from collections import namedtuple


class WalletManager(object):
    def __init__(self, scheme=SignatureScheme.SHA256withECDSA):
        self.scheme = scheme
        self.wallet_file = WalletData()
        self.wallet_in_mem = WalletData()
        self.wallet_path = ""

    def open_wallet(self, wallet_path: str):
        self.wallet_path = wallet_path
        if is_file_exist(wallet_path) is False:
            # create a new wallet file
            self.wallet_in_mem.createTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.save()
        # wallet file exists now
        self.wallet_file = self.load()
        self.wallet_in_mem = self.wallet_file
        return self.wallet_file

    def load(self):
        with open(self.wallet_path, "r") as f:
            r = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            # f.close()
            scrypt = Scrypt(r.scrypt.n, r.scrypt.r, r.scrypt.p, r.scrypt.dk_len)

            identities = []
            for index in range(len(r.identities)):
                control = [Control(id=r.identities[index].controls[0].id,
                                   algorithm=r.identities[index].controls[0].algorithm,
                                   param=r.identities[index].controls[0].parameters,
                                   key=r.identities[index].controls[0].key,
                                   address=r.identities[index].controls[0].address,
                                   salt=r.identities[index].controls[0].salt,
                                   enc_alg=r.identities[index].controls[0].enc_alg,
                                   hash_value=r.identities[index].controls[0].hash,
                                   public_key=r.identities[index].controls[0].publicKey)]
                temp = Identity(r.identities[index].ontid, r.identities[index].label, r.identities[index].lock, control)
                identities.append(temp)

            accounts = []
            for index in range(len(r.accounts)):
                temp = AccountData(label=r.accounts[index].label, public_key=r.accounts[index].publicKey,
                                   sign_scheme=r.accounts[index].signatureScheme,
                                   is_default=r.accounts[index].isDefault,
                                   lock=r.accounts[index].lock, address=r.accounts[index].address,
                                   algorithm=r.accounts[index].algorithm, param=r.accounts[index].parameters,
                                   key=r.accounts[index].key, enc_alg=r.accounts[index].enc_alg,
                                   salt=r.accounts[index].salt, hash_value=r.accounts[index].hash)
                accounts.append(temp)

            res = WalletData(r.name, r.version, r.createTime, r.defaultOntid, r.defaultAccountAddress, scrypt,
                             identities, accounts)
            return res

    def save(self):
        with open(self.wallet_path, "w") as f:
            json.dump(self.wallet_in_mem, f, default=lambda obj: obj.__dict__, indent=4)

    def get_wallet(self):
        return self.wallet_in_mem

    def write_wallet(self):
        self.save()
        self.wallet_file = self.wallet_in_mem
        return self.wallet_file

    def reset_wallet(self):
        self.wallet_in_mem = self.wallet_file.clone()
        return self.wallet_in_mem

    def get_signature_scheme(self):
        return self.scheme

    def set_signature_scheme(self, scheme):
        self.scheme = scheme

    def import_identity(self, label: str, encrypted_privkey: str, pwd: str, salt: str, address: str):
        private_key = Account.get_gcm_decoded_private_key(encrypted_privkey, pwd, address, salt,
                                                          Scrypt().get_n(), self.scheme)
        info = self.__create_identity(label, pwd, salt, private_key)
        private_key = None
        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ontid == info.ontid:
                return self.wallet_in_mem.identities[index]
        return None

    def create_identity(self, label: str, pwd: str):
        priv_key = get_random_bytes(32)
        salt = get_random_str(16)
        return self.__create_identity(label, pwd, salt, priv_key)

    def __create_identity(self, label: str, pwd: str, salt: str, private_key: bytes):
        acct = self.__create_account(label, pwd, salt, private_key, False)
        info = IdentityInfo()
        info.ontid = did_ont + acct.get_address_base58()
        info.pubic_key = acct.serialize_public_key().hex()
        info.private_key = acct.serialize_private_key().hex()
        info.prikey_wif = acct.export_wif()
        info.encrypted_prikey = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        return self.wallet_in_mem.get_identity_by_ontid(info.ontid)

    def create_identity_from_prikey(self, label: str, pwd: str, private_key: bytes):
        salt = get_random_str(16)
        identity = self.__create_identity(label, pwd, salt, private_key)
        private_key = None
        return identity

    def create_account(self, label: str, pwd: str) -> AccountData:
        priv_key = get_random_bytes(32)
        salt = get_random_str(16)
        account = self.__create_account(label, pwd, salt, priv_key, True)
        return self.wallet_file.get_account_by_address(account.get_address_base58())

    def __create_account(self, label: str, pwd: str, salt: str, priv_key: bytes, account_flag: bool):
        account = Account(priv_key, self.scheme)
        # initialization
        if self.scheme == SignatureScheme.SHA256withECDSA:
            acct = AccountData()
        else:
            raise ValueError("scheme type is error")
        # set key
        if pwd != None:
            from Cryptodome.Util.py3compat import tobytes, bord, _copy_bytes
            acct.key = account.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
            pwd = None
        else:
            acct.key = account.serialize_private_key().hex()

        acct.address = account.get_address_base58()
        # set label
        if label is None or label == "":
            label = str(uuid.uuid4())[0:8]
        if account_flag:
            for index in range(len(self.wallet_in_mem.accounts)):
                if acct.address == self.wallet_in_mem.accounts[index].address:
                    raise ValueError("wallet account exists")

            if len(self.wallet_in_mem.accounts) == 0:
                acct.isDefault = True
                self.wallet_in_mem.defaultAccountAddress = acct.address
            acct.label = label
            acct.salt = base64.b64encode(salt.encode()).decode('ascii')
            acct.publicKey = account.serialize_public_key().hex()
            self.wallet_in_mem.accounts.append(acct)
        else:
            for index in range(len(self.wallet_in_mem.identities)):
                if self.wallet_in_mem.identities[index].ontid == did_ont + acct.address:
                    raise ValueError("wallet identity exists")
            idt = Identity()
            idt.ontid = did_ont + acct.address
            idt.label = label
            if len(self.wallet_in_mem.identities) == 0:
                idt.isDefault = True
                self.wallet_in_mem.defaultOntid = idt.ontid
            ctl = Control(id="keys-1", key=acct.key, salt=base64.b64encode(salt.encode()).decode('ascii'),
                          address=acct.address,
                          public_key=account.serialize_public_key().hex())
            idt.controls.append(ctl)
            self.wallet_in_mem.identities.append(idt)
        return account

    def import_account(self, label: str, encrypted_prikey: str, pwd: str, base58_addr: str, base64_salt: str):
        salt = base64.b64decode(base64_salt.encode('ascii')).decode('latin-1')
        private_key = Account.get_gcm_decoded_private_key(encrypted_prikey, pwd, base58_addr, salt, Scrypt().get_n(),
                                                          self.scheme)
        info = self.create_account_info(label, pwd, salt, private_key)
        private_key, pwd = None, None
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].address:
                return self.wallet_in_mem.accounts[index]
        return None

    def create_account_info(self, label: str, pwd: str, salt: str, private_key: bytes):
        acct = self.__create_account(label, pwd, salt, private_key, True)
        info = AccountInfo()
        info.address_base58 = Address.address_from_bytes_pubkey(acct.serialize_public_key()).to_base58()
        info.public_key = acct.serialize_public_key().hex()
        info.encrypted_prikey = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        info.salt = salt
        return info

    def create_account_from_prikey(self, label: str, pwd: str, private_key: bytes):
        salt = get_random_str(16)
        info = self.create_account_info(label, pwd, salt, private_key)
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].address:
                return self.wallet_in_mem.accounts[index]
        return None

    def get_account(self, address: str, pwd: str):
        for index in range(len(self.wallet_in_mem.accounts)):
            if self.wallet_in_mem.accounts[index].address == address:
                key = self.wallet_in_mem.accounts[index].key
                addr = self.wallet_in_mem.accounts[index].address
                salt = base64.b64decode(self.wallet_in_mem.accounts[index].salt)
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.scheme)
                return Account(private_key, self.scheme)

        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ontid == did_ont + address:
                addr = self.wallet_in_mem.identities[index].ontid.replace(did_ont, "")
                key = self.wallet_in_mem.identities[index].controls[0].key
                salt = base64.b64decode(self.wallet_in_mem.identities[index].controls[0].salt)
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.scheme)
                return Account(private_key, self.scheme)
        return None


if __name__ == '__main__':
    # test wallet load and save
    private_key = '99bbd375c745088b372c6fc2ab38e2fb6626bc552a9da47fc3d76baa21537a1c'
    private_key = a2b_hex(private_key.encode())
    scheme = SignatureScheme.SHA256withECDSA
    acct0 = Account(private_key, scheme)
    encrypted_key = 'T3uep1USsEqiJbP4O+CKsl2AWfpGjvuVSKxpoKeGdEUa0nfLHHjIq3G4xOz7a4PC'
    wallet_path = 'test.json'
    w = WalletManager()
    w.open_wallet(wallet_path)
    salt = get_random_str(16)
    # w.import_account("123", encrypted_key, '234', acct0.get_address_base58(), salt)
    if False:
        w.create_random_account("label", "1")
        w.create_random_identity("label-ontid", "1")
        w.create_account_from_prikey("label123", "1", private_key)
        w.create_identity_from_prikey("label123-ontid", "1", private_key)
    if True:
        acctTmp = w.get_account("AMJYVc3vHK7vZ3XfFXsBP9r9sGN1cYYeQN", "1")
        print(acctTmp.get_address_base58())
    print(w.wallet_in_mem.accounts[0].__dict__)
    w.save(wallet_path)
