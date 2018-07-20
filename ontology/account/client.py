from ontology.crypto.Curve import Curve
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.crypto.SignatureHandler import SignatureHandler
from ontology.crypto.Signature import Signature
from ontology.common.address import Address
from ontology.crypto.KeyType import KeyType


class Account(object):
    def __init__(self, private_key, key_type):
        self.__keyType = key_type
        self.__privateKey = private_key
        self.__curve_name = Curve.P256
        self.__publicKey = Signature.ec_get_pubkey_by_prikey(private_key, self.__curve_name)
        self.__address = Address.address_from_hexstr_pubkey(self.__publicKey)

    def generateSignature(self, msg, signature_scheme):
        if signature_scheme == SignatureScheme.SHA256withECDSA:
            handler = SignatureHandler(self.__keyType, signature_scheme)
            signature_value = handler.generateSignature(self.__privateKey, msg)
            byte_signature = Signature(signature_scheme, signature_value).to_byte()
        else:
            raise TypeError
        return byte_signature

    def get_address(self):
        return self.__address
    def get_address_base58(self):
        return self.__address.to_base58()

    def get_public_key(self):
        return self.__publicKey




if __name__ == '__main__':
    private_key = '15746f42ec429ce1c20647e92154599b644a00644649f03868a2a5962bd2f9de'
    key_type = KeyType.ECDSA
    acct0 = Account(private_key, key_type)
    print(type(acct0.get_public_key()))
    print(acct0.get_public_key().hex())
    print(acct0.get_address())
