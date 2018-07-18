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


class Sig(object):
    sig_data = []  # [][]byte
    public_keys = []  # a list to save public keys
    M = 0


def transaction_from_hex_string(raw_tx: str):
    pass  # TODO
