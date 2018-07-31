from ontology.account.account import Account
from ontology.core.sig import Sig
from ontology.core.transaction import Transaction
from ontology.utils import util
from ontology.wallet.wallet_manager import WalletManager
from ontology.rpc import rpc
from ontology.common import define as Common


class OntologySdk(object):
    def __init__(self):
        self.rpc_client = rpc.RpcClient()
        self.wallet_manager = WalletManager()

    def sign_transaction(self, tx: Transaction, signer: Account):
        tx_hash = tx.hash256()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        sig = [Sig([signer.get_public_key()], 1, [sig_data])]
        tx.sigs = sig
        return tx

    def add_sign_transaction(self, tx: Transaction, signer: Account):
        if tx.sigs == None or len(tx.sigs) == 0:
            tx.sigs = []
        elif len(tx.sigs) >= Common.TX_MAX_SIG_SIZE:
            raise Exception("the number of transaction signatures should not be over 16")
        tx_hash = tx.hash256()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        sig = Sig([signer.serialize_public_key()], 1, [sig_data])
        tx.sigs.append(sig)
        return tx


    def open_or_create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            return self.open_wallet(wallet_file)
        return self.create_wallet(wallet_file)

    def create_wallet(self, wallet_file):
        if util.is_file_exist(wallet_file):
            raise IsADirectoryError("wallet file has already exist")
        return self.wallet_manager.open_wallet(wallet_file)

    def open_wallet(self, wallet_file):
        return self.wallet_manager.open_wallet(wallet_file)
