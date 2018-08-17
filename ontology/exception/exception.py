#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class SDKException(Exception):
    def __init__(self, error_code: dict):
        super().__init__(error_code['error'], error_code['desc'])


class SDKRuntimeException(RuntimeError):
    def __init__(self, error_code: dict):
        super().__init__(error_code['error'], error_code['desc'])
