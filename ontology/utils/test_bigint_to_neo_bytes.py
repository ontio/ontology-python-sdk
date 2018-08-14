from unittest import TestCase
from ontology.utils import  util


class TestBigint_to_neo_bytes(TestCase):
    def test_bigint_to_neo_bytes(self):
        bs = util.bigint_to_neo_bytes(1)
        print(bs.hex())
