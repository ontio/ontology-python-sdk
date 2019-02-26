#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from test import sdk, password


class TestSigSvr(unittest.TestCase):
    def test_create_account(self):
        sdk.service.sig_svr().connect_to_localhost()
        result = sdk.service.sig_svr().create_account(password)
        print(result)
