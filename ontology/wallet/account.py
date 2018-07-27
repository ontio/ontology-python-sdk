class AccountData(object):
    def __init__(self, address='', enc_alg="aes-256-gcm", key="", algorithm="ECDSA", salt="", param={"curve": "P-256"},
                 label="", public_key="", sign_scheme="SHA256withECDSA", is_default=True, lock=False,
                 hash_value="sha256"):
        self.address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.hash = hash_value
        self.isDefault = is_default
        self.key = key
        self.label = label
        self.lock = lock
        self.parameters = param
        self.salt = salt
        self.publicKey = public_key
        self.signatureScheme = sign_scheme

    def set_label(self, label: str):
        self.label = label

    def set_address(self, address):
        self.address = address

    def set_public_key(self, public_key):
        self.publicKey = public_key

    def set_key(self, key):
        self.key = key

    def get_label(self):
        return self.label

    def get_address(self):
        return self.address

    def get_public_key(self):
        return self.publicKey

    def get_key(self):
        return self.key


