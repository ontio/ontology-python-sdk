#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.core.transaction import Transaction, TransactionType
from ontology.io.binary_writer import BinaryWriter


class InvokeTransaction(Transaction):
    def __init__(self):
        super().__init__()
        self.tx_type = TransactionType.InvokeCode.value
        self.code = None

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.write_var_bytes(self.code)
