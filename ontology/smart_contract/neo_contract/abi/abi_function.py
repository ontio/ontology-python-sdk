from ontology.smart_contract.neo_contract.abi.parameter import Parameter


class AbiFunction(object):

    def __init__(self, name: str, return_type: str, parameters: list):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters

    def set_params_value(self, params: tuple):
        if len(params) != len(self.parameters):
            raise Exception("parameter error")
        temp = self.parameters
        self.parameters = []
        for i in range(len(params)):
            self.parameters.append(Parameter(temp[i]['name'], temp[i]['type']))
            self.parameters[i].set_value(params[i])

    def get_parameter(self, name):
        for p in self.parameters:
            if p.name == name:
                return p
