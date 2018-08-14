from unittest import TestCase

from ontology.smart_contract.neo_contract.abi.build_params import BuildParams


class TestBuildParams(TestCase):
    def test_create_code_params_script(self):
        m = {}
        m["key"] = "value"
        l = []
        l.append(m)
        aa = BuildParams.create_code_params_script(l)
        print(aa.hex())
