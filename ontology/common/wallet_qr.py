import base64
import json

from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.wallet.account import AccountData
from ontology.wallet.wallet import WalletData
from ontology.wallet.identity import Identity


class WalletQR(object):

    def export_identity_qrcode(self, wallet_file_or_scrypt, identity: Identity):
        control = identity.controls[0]
        address = identity.ontid[8:]
        d = dict()
        d["type"] = "I"
        d["label"] = identity.label
        d["key"] = control.key
        d["parameters"] = control.parameters
        d["algorithm"] = "ECDSA"
        if type(wallet_file_or_scrypt) is WalletData:
            d["scrypt"] = json.dumps(wallet_file_or_scrypt.scrypt, default=lambda obj: obj.__dict__, sort_keys=True,indent=4)
        else:
            d["scrypt"] = json.dumps(wallet_file_or_scrypt, default=lambda obj: obj.__dict__, sort_keys=True,indent=4)

        d["address"] = address
        d["salt"] = control.salt
        return d

    def export_account_qrcode(self, wallet_file_or_scrypt, account: AccountData):
        d = dict()
        d["type"] = "I"
        d["label"] = account.label
        d["key"] = account.key
        d["parameters"] = account.parameters
        d["algorithm"] = "ECDSA"
        if type(wallet_file_or_scrypt) is WalletData:
            d["scrypt"] = json.dumps(wallet_file_or_scrypt.scrypt, default=lambda obj: obj.__dict__, sort_keys=True,indent=4)
        else:
            d["scrypt"] = json.dumps(wallet_file_or_scrypt, default=lambda obj: obj.__dict__, sort_keys=True,indent=4)
        d["address"] = account.address
        d["salt"] = account.salt
        return d

    def get_prikey_from_qrcode(self, qr_code: str, password: str):
        d = json.loads(qr_code)
        key = d["key"]
        address = d["address"]
        salt = d["salt"]
        n = json.loads(d["scrypt"])["n"]
        return Account.get_gcm_decoded_private_key(key, password, address, base64.b64decode(salt), int(n), SignatureScheme.SHA256withECDSA)