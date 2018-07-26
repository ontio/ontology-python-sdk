did_ont = "did:ont:"


class Identity(object):
    def __init__(self, ontid="", label="", lock=False, controls=[], extra="", is_default=False):
        self.ontid = ontid
        self.label = label
        self.lock = lock
        self.controls = controls  # a list of Control()
        self.extra = extra
        self.is_default = is_default


class IdentityInfo(object):
    def __init__(self, ontid="", pubic_key="", encrypted_prikey="", address_u160="", private_key="", prikey_wif=""):
        self.ontid = ontid
        self.pubic_key = pubic_key
        self.encrypted_prikey = encrypted_prikey
        self.address_u160 = address_u160
        self.private_key = private_key
        self.prikey_wif = prikey_wif
