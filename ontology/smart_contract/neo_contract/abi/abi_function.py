from ontology.smart_contract.neo_contract.abi.parameter import Parameter


class AbiFunction(object):

    def __init__(self, name: str, returntype: str, parameters:[]):
        self.name = name
        self.returntype = returntype
        self.parameters = parameters

    def set_params_value(self, *objs):
        if len(objs) != len(self.parameters):
            raise Exception("parameter error")
        temp = self.parameters
        self.parameters = []
        for i in range(len(objs)):
            self.parameters.append(Parameter(temp[i].name, temp[i].type))
            self.parameters[i].set_value(objs[i])

    def get_parameter(self, name):
        for p in self.parameters:
            if p.name == name:
                return p

