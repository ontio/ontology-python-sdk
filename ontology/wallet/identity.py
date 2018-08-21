#!/usr/bin/env python3
# -*- coding: utf-8 -*-

did_ont = "did:ont:"


class Identity(object):
    def __init__(self, ont_id: str = "", label: str = "", lock: bool = False, controls: list = None, is_default=False):
        if controls is None:
            controls = list()
        self.ont_id = ont_id
        self.label = label
        self.lock = lock
        self.controls = controls
        self.is_default = is_default

    def __iter__(self):
        data = dict()
        data['ontid'] = self.ont_id
        data['label'] = self.label
        data['lock'] = self.lock
        data['controls'] = self.controls
        data['isDefault'] = self.is_default
        for key, value in data.items():
            yield (key, value)
