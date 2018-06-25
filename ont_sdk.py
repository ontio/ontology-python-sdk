from utils import util
from rpc import rpc_client
from account import client


class OntologySdk(object):
    def __init__(self):
        self.rpc_client = rpc_client.RpcClient()

    def open_or_create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            return self.open_wallet()
        return self.create_wallet()

    def create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            raise IsADirectoryError("wallet file has already exist")
        return client.open()

    def open_wallet(self):
        return client.open()
