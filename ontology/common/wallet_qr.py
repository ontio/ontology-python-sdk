#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import base64

from ontology.account.account import Account
from ontology.wallet.wallet import WalletData
from ontology.wallet.identity import Identity
from ontology.wallet.account import AccountData
from ontology.crypto.signature_scheme import SignatureScheme


class WalletQR(object):
    @staticmethod
    def export_identity_qr_code(wallet_file_or_scrypt, identity: Identity):
        control = identity.controls[0]
        address = identity.ont_id[8:]

        if type(wallet_file_or_scrypt) is WalletData:
            scrypt = json.dumps(wallet_file_or_scrypt.scrypt, default=lambda obj: obj.__dict__, sort_keys=True,
                                indent=4)
        else:
            scrypt = json.dumps(wallet_file_or_scrypt, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        data = dict(type='I', label=identity.label, key=control.key, parameters=control.parameters, algorithm='ECDSA',
                    scrypt=scrypt, address=address, salt=control.salt)
        return data

    @staticmethod
    def export_account_qr_code(wallet_file_or_scrypt, account: AccountData):
        if type(wallet_file_or_scrypt) is WalletData:
            scrypt = json.dumps(wallet_file_or_scrypt.scrypt, default=lambda obj: obj.__dict__, sort_keys=True,
                                indent=4)
        else:
            scrypt = json.dumps(wallet_file_or_scrypt, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        data = dict(type='I', label=account.label, key=account.key, parameters=account.parameters, algorithm="ECDSA",
                    scrypt=scrypt, address=account.b58_address, salt=account.salt)
        return data

    @staticmethod
    def get_private_key_from_qr_code(qr_code: str, password: str):
        data = json.loads(qr_code)
        key = data['key']
        address = data['address']
        salt = data['salt']
        n = json.loads(data['scrypt'])['n']
        acct = Account.get_gcm_decoded_private_key(key, password, address, base64.b64decode(salt), int(n),
                                                   SignatureScheme.SHA256withECDSA)
        return acct
