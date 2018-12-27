from ontology.core.transaction import Transaction, TransactionType
from ontology.io.binary_writer import BinaryWriter


class DeployTransaction(Transaction):
    def __init__(self, code=None, need_storage=None, name=None, version=None, author=None, email=None,
                 description=None):
        super().__init__()
        self.code = code
        self.need_storage = need_storage
        self.name = name
        self.code_version = version
        self.author = author
        self.email = email
        self.description = description
        self.tx_type = TransactionType.DeployCode.value

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.write_var_bytes(self.code)
        writer.write_bool(self.need_storage)
        writer.write_var_str(self.name)
        writer.write_var_str(self.code_version)
        writer.write_var_str(self.author)
        writer.write_var_str(self.email)
        writer.write_var_str(self.description)
