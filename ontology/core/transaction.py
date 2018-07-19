from ontology.common.serialize import write_byte, write_uint32, write_uint64, write_var_uint
from ontology.crypto.Digest import Digest


class Transaction(object):
    def __init__(self, version, tx_type, nonce, gas_price, gas_limit, payer, payload, attributes, sigs, hash):
        self.version = version
        self.tx_type = tx_type
        self.nonce = nonce
        self.gas_price = gas_price
        self.gas_limit = gas_limit
        self.payer = payer  # common.address [20]bytes
        self.payload = payload
        self.attributes = attributes
        self.sigs = sigs  # Sig class array
        self.hash = hash  # [32]byte

    def serialize_unsigned(self) -> bytearray:
        res = bytearray()
        res += write_byte(self.version)
        res += write_byte(self.tx_type)
        res += write_uint32(self.nonce)
        print('nonce')
        res += write_uint64(self.gas_price)
        res += write_uint64(self.gas_limit)
        res += self.payer
        res += self.payload
        res += write_var_uint(self.attributes)
        return res

    def hash(self):
        tx_serial = self.serialize_unsigned()
        r = Digest.hash256(tx_serial)
        r = Digest.hash256(r)
        return r


class Sig(object):
    def __init__(self, public_keys, M, sig_data):
        self.public_keys = []  # a list to save public keys
        self.M = 0
        self.sig_data = []  # [][]byte
