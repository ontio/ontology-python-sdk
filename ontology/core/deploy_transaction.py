from ontology.core.transaction import Transaction, TransactionType
from ontology.io.binary_writer import BinaryWriter


class DeployTransaction(Transaction):
    def __init__(self, code: bytearray or str, need_storage: bool, name: str = '', version: str = '', author: str = '',
                 email: str = '', description: str = '', gas_price: int = 0, gas_limit: int = 0,
                 payer: str or bytes = b''):
        super().__init__(0, TransactionType.DeployCode.value, gas_price, gas_limit, payer)
        if isinstance(code, str):
            code = bytearray.fromhex(code)
        self.__code = code
        self.__need_storage = need_storage
        self.__name = name
        self.__code_version = version
        self.__author = author
        self.__email = email
        self.__description = description

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.write_var_bytes(self.__code)
        writer.write_bool(self.__need_storage)
        writer.write_var_str(self.__name)
        writer.write_var_str(self.__code_version)
        writer.write_var_str(self.__author)
        writer.write_var_str(self.__email)
        writer.write_var_str(self.__description)
