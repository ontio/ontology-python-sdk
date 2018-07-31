from ontology.utils import util
from ontology.wallet.wallet_manager import WalletManager
from ontology.rpc import rpc


class OntologySdk(object):
    def __init__(self):
        self.rpc_client = rpc.RpcClient()
        self.wallet_manager = WalletManager()

    def open_or_create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            return self.open_wallet(wallet_file)
        return self.create_wallet(wallet_file)

    def create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            raise IsADirectoryError("wallet file has already exist")
        return WalletManager().open_wallet(wallet_file)

    def open_wallet(self, wallet_file):
        return WalletManager().open_wallet(wallet_file)
