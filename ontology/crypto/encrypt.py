from ontology.wallet.control import ProtectedKey
from ontology.wallet.scrypt import ScryptParam
from ontology.utils.util import print_byte_array
from os import urandom


def reencrypt_private_key(protected_key, old_pwd, new_pwd, old_param, new_param):
    raw = decrypt_with_custom_scrypt(protected_key, old_pwd, old_param)
    new_prot = encrypt_with_custom_scrypt(raw, protected_key.address, new_pwd, new_param)
    return new_prot


def decrypt_with_custom_scrypt(prot_key, pwd, param):
    pass


def encrypt_with_custom_scrypt(private_key, addr: str, pwd: bytearray, param):
    prot = ProtectedKey(address=addr, enc_alg="aes-256-gcm")
    salt = get_random_bytes(16)
    prot.salt = salt


def get_random_bytes(length):
    res = bytearray(urandom(length))
    return res
