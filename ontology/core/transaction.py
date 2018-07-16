class Transaction(object):
    def __init__(self):
        self.version = bytes()
        self.tx_type = bytes()
        self.nonce = 0
        self.gas_price = 0
        self.gas_limit = 0
        self.payer = bytes()  # common.address [20]bytes
        self.payload = ''  # todo
        self.attributes = bytes()
        self.sigs = []  # Sig class array
        self.hash = bytearray()  # [32]byte


class Sig(object):
    sig_data = []  # [][]byte
    public_keys = []  # a list to save public keys
    M = 0


def transaction_from_hex_string(raw_tx: str):
    pass  # TODO

