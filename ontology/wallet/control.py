class ProtectedKey(object):
    def __init__(self, address='', enc_alg='', key=bytearray(), algorithm='', salt=bytearray(), hash_value='',
                 param={}):
        self.address = address
        self.enc_alg = enc_alg
        self.key = key
        self.algorithm = algorithm
        self.salt = salt
        self.hash_value = hash_value
        self.param = param


class Control(object):
    def __init__(self, id="", publicKey="", protected_key=ProtectedKey()):
        self.id = id
        self.publicKey = publicKey
        self.protected_key = protected_key

