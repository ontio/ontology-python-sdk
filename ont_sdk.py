from utils import util
from rpc import rpc_client
from account import client


class OntologySdk(object):
    def __init__(self):
        self.rpc_client = rpc_client.RpcClient()

    def open_or_create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            return self.open_wallet(wallet_file)
        return self.create_wallet(wallet_file)

    def create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            raise IsADirectoryError("wallet file has already exist")
        return client.open(wallet_file)

    def open_wallet(self, wallet_file):
        return client.open(wallet_file)
