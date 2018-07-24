from ontology.crypto.Curve import Curve
from ontology.crypto.SignatureScheme import SignatureScheme
from ontology.crypto.SignatureHandler import SignatureHandler
from ontology.crypto.Signature import Signature
from ontology.common.address import Address
from ontology.crypto.KeyType import KeyType


class Account(object):
    def __init__(self, private_key, scheme):
        self.__signature_scheme = scheme
        if scheme == SignatureScheme.SHA256withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_384withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_384withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA512withECDSA:
            self.__keyType = KeyType.ECDSA
        elif scheme == SignatureScheme.SHA3_224withECDSA:
            self.__keyType = KeyType.ECDSA
        else:
            raise TypeError
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
        return self.__address  # __address is a class not a string or bytes

    def get_address_base58(self):
        return self.__address.to_base58()

    def get_public_key(self):
        return self.__publicKey
        
    def export_gcm_encrypted_private_key(self, password: bytes, salt: bytes, n: int):
        r = 8
        p = 8
        dk_len = 64
        scrypt = Scrypt(n, r, p, dk_len)
        derivedkey = scrypt.generate_kd(password, salt)
        iv = derivedkey[0:12]
        derivedhalf2 = derivedkey[32:64]
        scrypt = Scrypt(n, r, p, dk_len)
        scrypt.generate_kd(password, salt)
        mac_tag, cipher_text = AESHandler.aes_gcm_encrypt_with_iv(bytes(self.__privateKey, encoding='utf8'),
                                                                  self.__address.to_base58(),
                                                                  derivedhalf2,
                                                                  iv)
        encrypted_key = b2a_hex(mac_tag) + b2a_hex(cipher_text)
        return encrypted_key

    def get_gcm_decoded_private_key(self, encrypted_key: bytes, password: bytes, address: bytes, salt: bytes, n: int,
                                    scheme: SignatureScheme):
        r = 8
        p = 8
        dk_len = 64
        scrypt = Scrypt(n, r, p, dk_len)
        derivedkey = scrypt.generate_kd(password, salt)
        iv = derivedkey[0:12]
        derivedhalf2 = derivedkey[32:64]
        mac_tag = a2b_hex(encrypted_key[:32])
        cipher_text = a2b_hex(encrypted_key[32:])
        raw_key = AESHandler.aes_gcm_decrypt_with_iv(cipher_text, address, mac_tag, derivedhalf2, iv)
        acct = Account(private_key, scheme)
        if acct.get_address().to_base58() != address:
            raise RuntimeError
        return raw_key


if __name__ == '__main__':
    private_key = '15746f42ec429ce1c20647e92154599b644a00644649f03868a2a5962bd2f9de'
    key_type = KeyType.ECDSA
    acct0 = Account(private_key, key_type)
    print(type(acct0.get_public_key()))
    print(acct0.get_public_key().hex())
    print(acct0.get_address())
