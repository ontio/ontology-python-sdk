from ontology.wallet.control import ProtectedKey
from os import urandom


def reencrypt_private_key(protected_key, old_pwd, new_pwd, old_param, new_param):
    raw = decrypt_with_custom_scrypt(protected_key, old_pwd, old_param)
    new_prot = encrypt_with_custom_scrypt(raw, protected_key.address, new_pwd, new_param)
    return new_prot


def decrypt_with_custom_scrypt(prot_key, pwd, param):
    pass


def encrypt_with_custom_scrypt(private_key, addr: str, pwd: bytearray, param):
    pass

def get_random_bytes(length):
    res = bytes(urandom(length))
    return res
