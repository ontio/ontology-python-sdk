from ontology.wallet.control import ProtectedKey
from ontology.crypto.SignatureScheme import SignatureScheme


class AccountData(object):
    def __init__(self, protected_key: ProtectedKey, label="", public_key="",
                 sign_scheme=SignatureScheme.SHA256withECDSA, is_default=False, lock=False):
        self.protected_key = protected_key
        self.label = label
        self.public_key = public_key
        self.sign_scheme = sign_scheme
        self.is_default = is_default
        self.lock = lock

    def set_key_pair(self, key_info: ProtectedKey):
        self.protected_key.address = key_info.address
        self.protected_key.enc_alg = key_info.enc_alg
        self.protected_key.key = key_info.key
        self.protected_key.algorithm = key_info.algorithm
        self.protected_key.salt = key_info.salt
        self.protected_key.hash_value = key_info.hash_value
        self.protected_key.param = key_info.hash_value

    def get_key_pair(self):
        new_ProtectedKey = ProtectedKey()
        new_ProtectedKey.address = self.protected_key.address
        new_ProtectedKey.enc_alg = self.protected_key.enc_alg
        new_ProtectedKey.key = self.protected_key.key
        new_ProtectedKey.algorithm = self.protected_key.algorithm
        new_ProtectedKey.salt = self.protected_key.salt
        new_ProtectedKey.hash_value = self.protected_key.hash_value
        new_ProtectedKey.param = self.protected_key.param
        return new_ProtectedKey

    def set_label(self, label: str):
        self.label = label


class AccountInfo():
    def __init__(self):
        self.address_base58 = ""
        self.public_key = ""
        self.encrypted_prikey = ""
        self.address_u160 = ""
        self.private_key = ""
        self.prikey_wif = ""


