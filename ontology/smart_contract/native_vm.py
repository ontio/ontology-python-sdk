
from ontology.smart_contract.native_contract.asset import Asset
from ontology.smart_contract.native_contract.ontid import OntId


class NativeVm(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def asset(self):
        return Asset(self.__sdk)

    def ontid(self):
        return OntId(self.__sdk)
