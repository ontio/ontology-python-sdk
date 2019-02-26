#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.claim.claim import Claim
from ontology.claim.proof import BlockchainProof
from ontology.merkle.tx_verifier import TxVerifier
from ontology.service.sigsvr import SigSvr


class Service(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def tx_verifier(self):
        return TxVerifier(self.__sdk)

    def blockchain_proof(self):
        return BlockchainProof(self.__sdk)

    def claim(self):
        return Claim(self.__sdk)

    @staticmethod
    def sig_svr():
        return SigSvr()
