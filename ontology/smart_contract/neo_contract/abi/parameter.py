#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Parameter(object):

    def __init__(self, name: str, type_value: str, value=None):
        self.name = name
        self.type = type_value
        self.value = value

    def set_value(self, obj):
        self.value = obj
