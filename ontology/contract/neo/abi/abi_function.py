from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.contract.neo.abi.parameter import Parameter


class AbiFunction(object):
    def __init__(self, name: str, parameters: list, return_type: str = ''):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters

    def set_params_value(self, *params):
        """
        This interface is used to set parameter value for an function in abi file.
        """
        if len(params) != len(self.parameters):
            raise Exception("parameter error")
        for i, p in enumerate(params):
            self.parameters[i] = Parameter(self.parameters[i]['name'], self.parameters[i]['type'], p)

    def get_parameter(self, param_name: str) -> Parameter:
        """
        This interface is used to get a Parameter object from an AbiFunction object
        which contain given function parameter's name, type and value.

        :param param_name: a string used to indicate which parameter we want to get from AbiFunction.
        :return: a Parameter object which contain given function parameter's name, type and value.
        """
        for p in self.parameters:
            if p.name == param_name:
                return p
        raise SDKException(ErrorCode.param_err('get parameter failed.'))
