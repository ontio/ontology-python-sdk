#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.claim.claim import Claim
from ontology.sigsvr.sigsvr import SigSvr
from ontology.claim.proof import BlockchainProof
from ontology.merkle.tx_verifier import TxVerifier


class Service(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__sig_svr = None
        self.__claim = None
        self.__tx_verifier = None
        self.__blockchain_proof = None

    def tx_verifier(self):
        if self.__tx_verifier is None:
            self.__tx_verifier = TxVerifier(self.__sdk)
        return self.__tx_verifier

    def blockchain_proof(self):
        if self.__blockchain_proof is None:
            self.__blockchain_proof = BlockchainProof(self.__sdk)
        return self.__blockchain_proof

    def claim(self):
        if self.__claim is None:
            self.__claim = Claim(self.__sdk)
        return self.__claim

    @property
    def sig_svr(self):
        if self.__sig_svr is None:
            self.__sig_svr = SigSvr()
        return self.__sig_svr
