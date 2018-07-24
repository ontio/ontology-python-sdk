from ontology.wallet.wallet import WalletData
from ontology.utils.util import is_file_exist
from ontology.crypto.SignatureScheme import SignatureScheme
from datetime import datetime
import json
import base64
from ontology.crypto.scrypt import Scrypt
from ontology.account.account import Account

class WalletManager(object):
    def __init__(self, wallet_path, scheme=SignatureScheme.SHA256withECDSA):
        self.__wallet_path = wallet_path
        self.__scheme = scheme
        self.wallet_file = WalletData()

    def open_wallet(self):
        if is_file_exist(self.__wallet_path) is False:
            # create a new wallet file
            self.wallet_file.create_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.wallet_file.save(self.__wallet_path)
        # wallet file exists now
        self.wallet_file = self.read_data_from_file(self.__wallet_path)
        return self.wallet_file

    def read_data_from_file(self, wallet_path):
        file = open(wallet_path, 'r', encoding='utf-8')
        content = json.load(file)
        return content

    def get_wallet_file(self):
        return self.wallet_file

    def get_signature_scheme(self):
        return self.__scheme

    def set_signature_scheme(self, scheme):
        self.__scheme = scheme

    def import_identity(self, label: str, encrypted_prikey: str, pwd, salt: bytearray, address: str):
        pass


'''

private_key=Account.get_gcm_decoded_private_key(encrypted_prikey,pwd,address,salt,Scrypt.get_n(),self.__scheme)


String prikey = com.github.ontio.account.Account.getGcmDecodedPrivateKey(encryptedPrikey, password, address,salt, walletFile.getScrypt().getN(), scheme);
        IdentityInfo info = createIdentity(label,password,salt, Helper.hexToBytes(prikey));
        prikey = null;
        return getWallet().getIdentity(info.ontid);
'''

if __name__ == '__main__':
    wallet_path = '/Users/zhaoxavi/test.txt'
    w = WalletManager(wallet_path=wallet_path)
    res = w.open_wallet()
    print(res)

