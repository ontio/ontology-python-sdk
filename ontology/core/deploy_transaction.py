from ontology.core.transaction import Transaction
from ontology.io.binary_writer import BinaryWriter


class DeployTransaction(Transaction):
    def __init__(self, code = None, need_storage = None, name = None, version = None, author = None, email = None, description = None):
        self.code = code
        self.need_storage = need_storage
        self.name = name
        self.code_version = version
        self.author = author
        self.email = email
        self.description = description
        self.tx_type = 0xd0

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.WriteVarBytes(self.code)
        writer.WriteBool(self.need_storage)
        writer.WriteVarString(self.name)
        writer.WriteVarString(self.code_version)
        writer.WriteVarString(self.author)
        writer.WriteVarString(self.email)
        writer.WriteVarString(self.description)

