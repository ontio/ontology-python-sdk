from ontology.core.transaction import Transaction, TransactionType
from ontology.io.binary_writer import BinaryWriter


class DeployTransaction(Transaction):
    def __init__(self, code=None, need_storage=None, name=None, version=None, author=None, email=None,
                 description=None):
        super().__init__()
        self.__code = code
        self.__need_storage = need_storage
        self.__name = name
        self.__code_version = version
        self.__author = author
        self.__email = email
        self.__description = description
        self.__tx_type = TransactionType.DeployCode.value

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.write_var_bytes(self.__code)
        writer.write_bool(self.__need_storage)
        writer.write_var_str(self.__name)
        writer.write_var_str(self.__code_version)
        writer.write_var_str(self.__author)
        writer.write_var_str(self.__email)
        writer.write_var_str(self.__description)
