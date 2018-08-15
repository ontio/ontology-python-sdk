#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class IdentityInfo(object):
    def __init__(self, ont_id: str = "", pubic_key: str = "", encrypted_pri_key: str = "", address_u160: str = "",
                 private_key: str = "", pri_key_wif: str = ""):
        self.ont_id = ont_id
        self.pubic_key = pubic_key
        self.encrypted_pri_key = encrypted_pri_key
        self.address_u160 = address_u160
        self.private_key = private_key
        self.pri_key_wif = pri_key_wif
