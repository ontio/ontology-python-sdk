from ontology.wallet.wallet import WalletData
from ontology.utils.util import is_file_exist
from ontology.crypto.SignatureScheme import SignatureScheme
from datetime import datetime
import json
import base64
from ontology.crypto.scrypt import Scrypt
from ontology.account.account import Account
from ontology.wallet.account import AccountData
from ontology.wallet.control import ProtectedKey
from ontology.common.address import Address
import uuid


class WalletManager(object):
    def __init__(self, wallet_path, scheme=SignatureScheme.SHA256withECDSA):
        self.__wallet_path = wallet_path
        self.__scheme = scheme
        self.__wallet_file = WalletData()
        self.__wallet_in_mem = WalletData()

    def open_wallet(self):
        if is_file_exist(self.__wallet_path) is False:
            # create a new wallet file
            self.__wallet_file.create_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.__wallet_file.save(self.__wallet_path)
        # wallet file exists now
        self.__wallet_file = self.read_data_from_file(self.__wallet_path)
        self.__wallet_in_mem = self.read_data_from_file(self.__wallet_path)
        return self.__wallet_file

    def read_data_from_file(self, wallet_path):
        file = open(wallet_path, 'r', encoding='utf-8')
        content = json.load(file)
        return content

    def get_wallet(self):
        return self.__wallet_in_mem

    def write_wallet(self):
        self.__wallet_in_mem.save(self.__wallet_path)

    def reset_wallet(self):
        self.__wallet_in_mem=self.__wallet_file.clone()
        return self.__wallet_in_mem

    def get_signature_scheme(self):
        return self.__scheme

    def set_signature_scheme(self, scheme):
        self.__scheme = scheme

    def import_identity(self, label: str, encrypted_privkey: str, pwd, salt: bytearray, address: str):
        encrypted_privkey = base64.decodebytes(encrypted_privkey.encode())
        private_key = Account.get_gcm_decoded_private_key(encrypted_privkey, pwd, address.encode(), salt,
                                                          Scrypt().get_n(),
                                                          self.__scheme)

        info = self.create_identity(label, pwd, salt, private_key)
        private_key = None
        return  # todo getWallet().getIdentity(info.ontid);

    def create_identity(self, label: str, pwd, salt, private_key):
        pass

    def create_account(self, label, pwd, salt, priv_key, account_flag: bool):
        account = Account(priv_key, self.__scheme)
        # initialization
        if self.__scheme == SignatureScheme.SHA256withECDSA:
            prot = ProtectedKey(algorithm="ECDSA", enc_alg="aes-256-gcm", hash_value="SHA256withECDSA",
                                param={"curve": "secp256r1"})
            acct = AccountData(protected_key=prot, sign_scheme="SHA256withECDSA")  # todo init
        else:
            raise ValueError("scheme type is error")
        # set key
        if pwd != None:
            acct.protected_key.key = account.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
            pwd = None
        else:
            acct.protected_key.key = account.serialize_private_key().hex()

        acct.protected_key.address=Address.address_from_bytes_pubkey(account.get_address()).to_base58()
        # set label
        if label==None or label=="":
            uuidstr=str(uuid.uuid4())[0:8]
        if account_flag:
            pass




    '''
    
        if (accountFlag) {
            for (Account e : walletInMem.getAccounts()) {
                if (e.address.equals(acct.address)) {
                    throw new SDKException(ErrorCode.ParamErr("wallet account exist"));
                }
            }
            if (walletInMem.getAccounts().size() == 0) {
                acct.isDefault = true;
                walletInMem.setDefaultAccountAddress(acct.address);
            }
            acct.label = label;
            acct.setSalt(salt);
            walletInMem.getAccounts().add(acct);
        } else {
            for (Identity e : walletInMem.getIdentities()) {
                if (e.ontid.equals(Common.didont + acct.address)) {
                    throw new SDKException(ErrorCode.ParamErr("wallet Identity exist"));
                }
            }
            Identity idt = new Identity();
            idt.ontid = Common.didont + acct.address;
            idt.label = label;
            if (walletInMem.getIdentities().size() == 0) {
                idt.isDefault = true;
                walletInMem.setDefaultOntid(idt.ontid);
            }
            idt.controls = new ArrayList<Control>();
            Control ctl = new Control(acct.key, "keys-1");
            ctl.setSalt(salt);
            ctl.setAddress(acct.address);
            idt.controls.add(ctl);
            walletInMem.getIdentities().add(idt);
        }
        return account;
    }
    '''


'''
private IdentityInfo createIdentity(String label,String password,byte[] salt, byte[] prikey) throws Exception {
        com.github.ontio.account.Account acct = createAccount(label,password,salt, prikey, false);
        IdentityInfo info = new IdentityInfo();
        info.ontid = Common.didont + Address.addressFromPubKey(acct.serializePublicKey()).toBase58();
        info.pubkey = Helper.toHexString(acct.serializePublicKey());
        info.setPrikey(Helper.toHexString(acct.serializePrivateKey()));
        info.setPriwif(acct.exportWif());
        info.encryptedPrikey = acct.exportGcmEncryptedPrikey(password, salt,walletFile.getScrypt().getN());
        info.addressU160 = acct.getAddressU160().toHexString();
        return info;
'''

if __name__ == '__main__':
    wallet_path = '/Users/zhaoxavi/test.txt'
    w = WalletManager(wallet_path=wallet_path)
    res = w.open_wallet()
    print(res)


