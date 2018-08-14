from unittest import TestCase

from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager


class TestBinaryReader(TestCase):
    def test_ReadVarInt(self):

        writer_stream = StreamManager.GetStream()
        writer = BinaryWriter(writer_stream)
        writer.WriteByte(10)
        writer.WriteByte(b'a')
        reader_stream = StreamManager.GetStream(writer_stream.getbuffer())
        reader = BinaryReader(reader_stream)
        print(reader.ReadByte())
        b = reader.ReadByte(False)
        print(b)
        # self.assertEqual(reader.ReadVarInt(), value)


