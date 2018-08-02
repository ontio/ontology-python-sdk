import threading

from ontology.account.account import Account
from ontology.core.sig import Sig
from ontology.core.transaction import Transaction
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.native_vm import NativeVm
from ontology.wallet.wallet_manager import WalletManager
from ontology.rpc.rpc import RpcClient
from ontology.common import define as Common
from ontology.core.program import ProgramBuilder


class OntologySdk(object):
    _instance_lock = threading.Lock()
    __instance = None

    def __init__(self):
        self.rpc = RpcClient()
        self._wallet_manager = WalletManager()
        self._native_vm = None
        self.defaultSignScheme = SignatureScheme.SHA256withECDSA

    @staticmethod
    def get_instance():
        if OntologySdk.__instance is None:
            with OntologySdk._instance_lock:
                if OntologySdk.__instance is None:
                    OntologySdk.__instance = OntologySdk()
        return OntologySdk.__instance

    def native_vm(self):
        if self._native_vm is None:
            self._native_vm = NativeVm(OntologySdk.get_instance())
        return self._native_vm

    def get_wallet_manager(self):
        if self._wallet_manager is None:
            self._wallet_manager = WalletManager()
        return self._wallet_manager

    def get_rpc(self):
        if self._rpc is None:
            self._rpc = RpcClient()
        return self._rpc

    def set_signaturescheme(self, scheme: SignatureScheme):
        self.defaultSignScheme = scheme
        self._wallet_manager.set_signature_scheme(scheme)

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

    def add_multi_sign_transaction(self, tx: Transaction, m: int, pubkeys: [], signer: Account):
        pubkeys = ProgramBuilder.sort_publickeys(pubkeys)
        tx_hash = tx.hash256()
        sig_data = signer.generate_signature(tx_hash, signer.get_signature_scheme())
        if tx.sigs == None or len(tx.sigs) == 0:
            tx.sigs = []
        elif len(tx.sigs) >= Common.TX_MAX_SIG_SIZE:
            raise Exception("the number of transaction signatures should not be over 16")
        else:
            for i in range(len(tx.sigs)):
                if tx.sigs[i].public_keys == pubkeys:
                    print(type(tx.sigs[i].sig_data))
                    if len(tx.sigs[i].sig_data) + 1 > len(pubkeys):
                        raise Exception("too more sigData")
                    if tx.sigs[i].M != m:
                        raise Exception("M error")
                    tx.sigs[i].sig_data.append(sig_data)
                    return tx
        sig = Sig(pubkeys, m, [sig_data])
        tx.sigs.append(sig)
        return tx

    def open_wallet(self, wallet_file):
        return self.wallet_manager.open_wallet(wallet_file)
