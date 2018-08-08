import json

from ontology.smart_contract.neo_contract.abi.Struct import Struct


class Parameter(object):

    def __init__(self, name: str, type: str, value=None):
        self.name = name
        self.type = type
        self.value = value

    def set_value(self, obj):
        self.value = obj

