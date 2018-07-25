did_ont = "did:ont:"


class Identity(object):
    def __init__(self):
        self.ontid = ""
        self.label = ""
        self.lock = False
        self.controls = []  # a list of Control()
        self.extra = ""
        self.is_default = False


class IdentityInfo(object):
    def __init__(self, ontid="", pubic_key="", encrypted_prikey="", address_u160="", private_key="", prikey_wif=""):
        self.ontid = ontid
        self.pubic_key = pubic_key
        self.encrypted_prikey = encrypted_prikey
        self.address_u160 = address_u160
        self.private_key = private_key
        self.prikey_wif = prikey_wif
