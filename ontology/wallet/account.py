from ontology.wallet.control import ProtectedKey


class AccountData(object):
    def __init__(self, protected_key: ProtectedKey, label, public_key, sign_scheme, is_default, lock):
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


'''
                  
                  
# TODO: determine identity structure

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
    def __init__(self, wallet_path):
        self.wallet_path = wallet_path
        self.account_address = {}  # map[string]*AccountData
        self.account_label = {}  # map[string]*AccountData
        self.default_account = AccountData()
        self.wallet_data = WalletData()
        self.unlock_account = {}  # map[string]*UnlockAccountInfo()
        self.lock = RWMutex()
        self.set_value()

    def load(self):
        # TODO
        self.wallet_data.load(self.wallet_path)  # how to use data
        # for loop

    def set_value(self):
        if util.is_file_exist(self.wallet_data):
            self.load()


def open(wallet_path):
    new_client_impl = ClientImpl(wallet_path)
    return new_client_impl

'''
