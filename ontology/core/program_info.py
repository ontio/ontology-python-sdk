#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ProgramInfo(object):

    def __init__(self):
        self.pubkeys = []
        self.m = 0

    def set_pubkey(self, pubkeys: []):
        self.pubkeys = pubkeys

    def set_m(self, m):
        self.m = m
