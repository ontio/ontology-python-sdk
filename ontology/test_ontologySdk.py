from unittest import TestCase
from ontology.ont_sdk import OntologySdk


class TestOntologySdk(TestCase):
    def test_open_wallet(self):
        sdk = OntologySdk()
        a = sdk.open_wallet("./wallet/test.json")
        print(a)

    def test_open_or_create_wallet(self):
        sdk = OntologySdk()
        a = sdk.open_or_create_wallet("./test.json")

        print(a)

