
from ontology.smart_contract.native_contract.asset import Asset
from ontology.smart_contract.native_contract.ontid import OntId


class NativeVm(object):
    def __init__(self, sdk):
        self._sdk = sdk

    def asset(self):
        return Asset(self._sdk)

    def ontid(self):
        return OntId(self._sdk)
