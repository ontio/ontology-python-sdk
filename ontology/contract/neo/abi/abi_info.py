from ontology.contract.neo.abi.abi_function import AbiFunction


class AbiInfo(object):
    def __init__(self, hash_value: str = '', entry_point: str = '', functions: list = None, events: list = None):
        self.hash = hash_value
        self.entry_point = entry_point
        if functions is None:
            self.functions = list()
        else:
            self.functions = functions
        if events is None:
            self.events = list()
        else:
            self.events = events

    def get_function(self, name: str) -> AbiFunction or None:
        """
        This interface is used to get an AbiFunction object from AbiInfo object by given function name.

        :param name: the function name in abi file
        :return: if succeed, an AbiFunction will constructed based on given function name
        """
        for func in self.functions:
            if func['name'] == name:
                return AbiFunction(func['name'], func['parameters'], func.get('returntype', ''))
        return None
