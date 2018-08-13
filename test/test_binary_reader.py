import unittest

from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager


class TestBinaryReader(unittest.TestCase):
    def test_read_var_int(self):
        value = 123
        writer_stream = StreamManager.GetStream()
        writer = BinaryWriter(writer_stream)
        writer.WriteVarInt(value)
        reader_stream = StreamManager.GetStream(writer_stream.getbuffer())
        reader = BinaryReader(reader_stream)
        self.assertEqual(reader.ReadVarInt(), value)
