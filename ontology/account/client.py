import datetime
import json
from ontology.utils import util
from ontology.crypto.Curve import Curve
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.crypto.SignatureHandler import SignatureHandler
from ontology.crypto.Signature import Signature
from ontology.common.address import Address
from ontology.crypto.KeyType import KeyType


class Account(object):
    def __init__(self, private_key, key_type):
        self.__keyType = key_type
        self.__privateKey = private_key
        self.__curve_name = Curve.P256
        self.__publicKey = Signature.ec_get_pubkey_by_prikey(private_key, self.__curve_name)
        self.__address = Address.address_from_hexstr_pubkey(self.__publicKey)

    def generateSignature(self, msg, signature_scheme):
        if signature_scheme == SignatureScheme.SHA256withECDSA:
            handler = SignatureHandler(self.__keyType, signature_scheme)
            signature_value = handler.generateSignature(self.__privateKey, msg)
            byte_signature = Signature(signature_scheme, signature_value).to_byte()
        else:
            raise TypeError
        return byte_signature

    def get_address(self):
        return self.__address
    def get_address_base58(self):
        return self.__address.to_base58()

    def get_public_key(self):
        return self.__publicKey


class AccountData(object):
    def __init__(self):
        self.keypair = ProtectedKey()
        self.label = ''
        self.public_key = ''
        self.sign_scheme = ''
        self.is_default = False
        self.lock = False


class WalletData(object):
    def __init__(self):
        self.name = ''
        self.version = ''
        self.scrypt = ScryptParam()
        self.identities = []  # Identity list
        self.accounts = []  # AccountData list
        self.extra = ''

    def load(self, wallet_path):
        with open(wallet_path, 'r') as content_file:
            content = content_file.read()
        return json.loads(content)


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


if __name__ == '__main__':
    private_key = '15746f42ec429ce1c20647e92154599b644a00644649f03868a2a5962bd2f9de'
    key_type = KeyType.ECDSA
    acct0 = Account(private_key, key_type)
    print(type(acct0.get_public_key()))
    print(acct0.get_public_key().hex())
    print(acct0.get_address())
