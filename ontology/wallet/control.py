class Control(object):
    def __init__(self, id="", address='', enc_alg="aes-256-gcm", key="", algorithm='', salt="",
                 param={"curve": "P-256"}, hash_value="sha256", public_key=""):
        self.address = address
        self.algorithm = algorithm
        self.enc_alg = enc_alg
        self.hash = hash_value
        self.id = id
        self.key = key
        self.parameters = param
        self.salt = salt
        self.publicKey = public_key
