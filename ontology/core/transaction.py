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

    def serialize_unsigned(self):
        pass

    def serialize(self):
        pass

    def hash(self):
        pass

        '''
        if tx.hash == nil {
                buf := bytes.Buffer{}
                tx.SerializeUnsigned(&buf)
        
                temp := sha256.Sum256(buf.Bytes())
                f := common.Uint256(sha256.Sum256(temp[:]))
                tx.hash = &f
            }
            return *tx.hash
        '''

class Sig(object):
    def __init__(self, public_keys, M, sig_data):
        self.public_keys = []  # a list to save public keys
        self.M = 0
        self.sig_data = []  # [][]byte


def transaction_from_hex_string(raw_tx: str):
    pass  # TODO
