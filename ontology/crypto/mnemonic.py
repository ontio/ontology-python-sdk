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

import sys

import mnemonic

from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException


class Mnemonic(mnemonic.Mnemonic):
    def __init__(self, language: str = 'English'):
        try:
            super().__init__(language)
        except FileNotFoundError:
            self.radix = 2048
            with open('%s/%s.txt' % (self._get_directory(), language), 'r') as f:
                self.wordlist = [w.strip() for w in f.readlines()]
            if len(self.wordlist) != self.radix:
                raise SDKException(ErrorCode.other_error(
                    f'Wordlist should contain {self.radix} words, but it contains {len(self.wordlist)} words.'))
