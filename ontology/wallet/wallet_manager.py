from ontology.wallet.wallet import WalletData
from ontology.utils.util import is_file_exist


class WalletManager(object):
    def __init__(self, wallet_path, scheme):
        self.wallet_path = wallet_path
        self.scheme = scheme
        self.wallet_in_mem = WalletData()
        self.wallet_in_mem = WalletData()
