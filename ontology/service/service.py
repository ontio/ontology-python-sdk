#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.claim.claim import Claim


class Service(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def claim(self):
        return Claim(self.__sdk)
