"""
Copyright (C) 2018 The ontology Authors
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

from ontology.contract.native.ont import Ont
from ontology.contract.native.ong import Ong
from ontology.contract.native.ontid import OntId
from ontology.contract.native.aio_ont import AioOnt
from ontology.contract.native.aio_ong import AioOng
from ontology.contract.native.aio_ontid import AioOntId


class NativeVm(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def ont(self):
        return Ont(self.__sdk)

    def aio_ont(self):
        return AioOnt(self.__sdk)

    def aio_ong(self):
        return AioOng(self.__sdk)

    def aio_ont_id(self):
        return AioOntId(self.__sdk)

    def ong(self):
        return Ong(self.__sdk)

    def ont_id(self):
        return OntId(self.__sdk)

