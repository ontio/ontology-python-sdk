#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager


class TestBinaryReader(unittest.TestCase):
    def test_read_var_int(self):
        value = 123
        writer_stream = StreamManager.GetStream()
        writer = BinaryWriter(writer_stream)
        writer.write_var_int(value)
        reader_stream = StreamManager.GetStream(writer_stream.getbuffer())
        reader = BinaryReader(reader_stream)
        self.assertEqual(reader.read_var_int(), value)


if __name__ == '__main__':
    unittest.main()
