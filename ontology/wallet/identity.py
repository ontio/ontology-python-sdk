#!/usr/bin/env python3
# -*- coding: utf-8 -*-

did_ont = "did:ont:"


class Identity(object):
    def __init__(self, ont_id: str = "", label: str = "", lock: bool = False, controls: list = None):
        if controls is None:
            controls = list()
        self.ont_id = ont_id
        self.label = label
        self.lock = lock
        self.controls = controls
        self.is_default = False
