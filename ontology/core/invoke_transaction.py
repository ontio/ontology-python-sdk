#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.core.transaction import Transaction
from ontology.io.binary_writer import BinaryWriter


class InvokeTransaction(Transaction):
    def __init__(self):
        # TODO
        super(Transaction,self).__init__()
        self.tx_type = 0xd1
        self.code = None

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.write_var_bytes(self.code)
