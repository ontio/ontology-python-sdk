from ontology.smart_contract.native_contract.asset import Asset
from ontology.smart_contract.native_contract.ontid import OntId


class NativeVm(object):
    def __init__(self):
        self.asset = Asset()
        self.ontid = OntId()