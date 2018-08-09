
class AbiEvent(object):
    def __init__(self, name: str, return_type: str, parameters: []):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters

    def get_parameters(self):
        return self.parameters

    def set_params_value(self, *objs):
        if len(self.parameters) != len(objs):
            raise Exception("param error")
        for i in range(len(objs)):
            self.parameters[i].set_value(objs[i])

