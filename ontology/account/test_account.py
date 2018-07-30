from unittest import TestCase

from ontology.account.account import Account
from ontology.utils import util
from ontology.crypto.signature_scheme import SignatureScheme


class TestAccount(TestCase):
    def test_export_gcm_encrypted_private_key(self):
        account = Account(util.hex_to_bytes("75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"),SignatureScheme.SHA256withECDSA)
        salt = util.get_random_bytes(16)
        enprivateKey = account.export_gcm_encrypted_private_key("1",salt,16384)
        print(enprivateKey)
        privateKey = account.get_gcm_decoded_private_key(enprivateKey,"1",account.get_address_base58(),salt,16384,SignatureScheme.SHA256withECDSA)
        print(privateKey.hex())

    def test_generateSignature(self):
        account = Account(util.hex_to_bytes("523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"),
                          SignatureScheme.SHA256withECDSA)
        data = account.generateSignature(bytes("test".encode()), SignatureScheme.SHA256withECDSA)
        print(data.hex())

    def test_serialize_private_key(self):
        account = Account(util.hex_to_bytes("523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"),
                          SignatureScheme.SHA256withECDSA)
        print(account.serialize_private_key().hex())
        print(account.serialize_public_key().hex())
        print(account.export_wif())
        print(account.get_address().to_base58())
        print(account.get_address_base58())


