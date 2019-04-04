#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2018 The ontology Authors
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

from ontology.io.binary_reader import BinaryReader
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager


class TestBinaryReader(unittest.TestCase):
    def test_read_var_int(self):
        value = 123
        writer_stream = StreamManager.get_stream()
        writer = BinaryWriter(writer_stream)
        writer.write_var_int(value)
        reader_stream = StreamManager.get_stream(writer_stream.getbuffer())
        reader = BinaryReader(reader_stream)
        self.assertEqual(reader.read_var_int(), value)


if __name__ == '__main__':
    unittest.main()
