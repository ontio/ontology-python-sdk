from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction


class AbiInfo(object):
    def __init__(self, hash_value: str, entrypoint: str, functions: [], events: []):
        self.hash = hash_value
        self.entrypoint = entrypoint
        self.functions = functions
        self.events = events

    def get_function(self, name: str):
        for func in self.functions:
            if func.name == name:
                return AbiFunction(func.name, func.returntype, func.parameters)
        return None
