from ontology.core.transaction import Transaction
from ontology.io.binary_writer import BinaryWriter


class InvokeTransaction(Transaction):
    def __init__(self):
        self.tx_type = 0xd1
        self.code = None

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.WriteVarBytes(self.code)
