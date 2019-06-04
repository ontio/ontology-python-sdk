"""
Copyright (C) 2018-2019 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

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
