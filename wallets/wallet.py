# TODO: rewrite wallet function
class OntWallet(object):
    def __init__(self, crypt_scheme, wallet_client):
        self.crypt_scheme = crypt_scheme
        self.wallet = wallet_client  # ClientImpl()

    def set_crypt_scheme(self, crypt_scheme):
        self.crypt_scheme = crypt_scheme

    def get_default_account(self):
        return self.wallet
