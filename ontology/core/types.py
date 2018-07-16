class Header(object):
    def __init__(self):
        self.version = ""
        self.prev_block_hash = bytearray()  # [32]bytes
        self.TransactionsRoot = bytearray()  # [32]bytes
        self.BlockRoot = bytearray()  # [32]bytes
        self.Timestamp = 0
        self.Height = 0
        self.ConsensusData = 0
        self.ConsensusPayload = bytearray()
        self.NextBookkeeper = bytearray()  # [20]bytes
        self.Bookkeepers = []  # ]keypair.PublicKey
        self.SigData = []  # [][]byte
        self.hash = bytearray()  # [32]bytes


class Transaction(object):
    pass


class Block(object):
    def __init__(self):
        self.header = ''  # todo
        self.transaction = ''  # todo
