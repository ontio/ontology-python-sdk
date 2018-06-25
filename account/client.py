import datetime


class AccountData(object):
    def __init__(self):
        self.keypair = ProtectedKey()
        self.label = ''
        self.public_key = ''
        self.sign_scheme = ''
        self.is_default = False
        self.lock = False


class Account(object):
    def __init__(self):
        self.private_key = ''
        self.public_key = ''
        self.address = bytearray()
        self.sig_scheme = bytes()

    # get private key and then return public key
    def public(self):
        pass


class WalletData(object):
    def __init__(self):
        self.name = ''
        self.version = ''
        self.scrypt = ScryptParam()
        self.identities = []  # Identity list
        self.accounts = []  # AccountData list
        self.extra = ''


class ProtectedKey(object):
    def __init__(self):
        self.address = ''
        self.enc_alg = ''
        self.key = bytearray()
        self.alg = ''
        self.salt = bytearray()
        self.hash = ''
        self.param = {}


class ScryptParam(object):
    def __init__(self):
        self.p = 0
        self.n = 0
        self.r = 0
        self.DKLen = 0


# TODO: determine identity structure
class Identity(object):
    def __init__(self):
        pass


class RWMutex(object):
    def __init__(self):
        self.w = self.Mutex()
        writer_sem = 0
        reader_sem = 0
        reader_count = 0
        reader_wait = 0

    class Mutex(object):
        def __init__(self):
            state = 0
            sema = 0


class UnlockAccountInfo(object):
    def __init__(self):
        self.account = Account()
        self.unlock_time = datetime.time()
        self.expired_at = 0


class ClientImpl(object):
    def __init__(self):
        self.path = ''
        self.account_address = {}  # map[string]*AccountData
        self.account_label = {}  # map[string]*AccountData
        self.default_account = AccountData()
        self.wallet_data = WalletData()
        self.unlock_account = {}  # map[string]*UnlockAccountInfo()
        self.lock = RWMutex()

def open():
    pass