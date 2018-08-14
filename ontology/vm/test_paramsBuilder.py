from unittest import TestCase

from ontology.vm.params_builder import ParamsBuilder


class TestParamsBuilder(TestCase):
    def test_emit_push_integer(self):
        pb = ParamsBuilder()
        pb.emit_push_integer(100)
        a = pb.to_array()
        print(a.hex())
