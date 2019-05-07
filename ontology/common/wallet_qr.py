"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

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

        if isinstance(wallet_file_or_scrypt, WalletData):
            scrypt = json.dumps(wallet_file_or_scrypt.scrypt, default=lambda obj: obj.__dict__, sort_keys=True,
                                indent=4)
        else:
            scrypt = json.dumps(wallet_file_or_scrypt, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        data = dict(type='I', label=identity.label, key=control.key, parameters=control.parameters, algorithm='ECDSA',
                    scrypt=scrypt, address=address, salt=control.salt)
        return data

    @staticmethod
    def export_account_qr_code(wallet_file_or_scrypt, account: AccountData):
        if isinstance(wallet_file_or_scrypt, WalletData):
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
