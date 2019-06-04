"""
Copyright (C) 2018-2019 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

from ontology.io.binary_writer import BinaryWriter

from ontology.io.memory_stream import StreamManager


class TestBinaryWriter(unittest.TestCase):
    def setUp(self):
        self.stream = StreamManager.get_stream()
        self.writer = BinaryWriter(self.stream)

    def test_write_byte(self):
        values = [15, 255, 'a', 'z', b'a', 'byte']
        results = [b'0f', b'ff', b'61', b'7a', b'61', b'62']
        for i, v in enumerate(values):
            self.writer.write_byte(v)
            self.assertEqual(results[i], self.stream.hexlify())
            self.stream.clean_up()

    def test_write_uint8(self):
        values = [15, 255, 15, 255]
        results = [b'0f', b'ff', b'0f', b'ff']
        little_endian_lst = [True, True, False, False]
        for i, v in enumerate(values):
            self.writer.write_uint8(v, little_endian=little_endian_lst[i])
            self.assertEqual(results[i], self.stream.hexlify())
            self.stream.clean_up()


if __name__ == '__main__':
    unittest.main()
