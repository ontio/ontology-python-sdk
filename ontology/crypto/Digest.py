#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib


class Digest(object):
    @staticmethod
    def __sha256(byte_msg, is_hex=False):
        m = hashlib.sha256()
        m.update(byte_msg)
        if is_hex:
            return m.hexdigest()
        else:
            return m.digest()

    @staticmethod
    def ripemd160(byte_msg, is_hex=False):
        h = hashlib.new('ripemd160')
        h.update(byte_msg)
        if is_hex:
            return h.hexdigest()
        else:
            return h.digest()

    @staticmethod
    def sha256(msg: bytes, offset=0, length=0, is_hex=False):
        if offset != 0 and len(msg) > offset + length:
            msg = msg[offset:offset + length]
        return Digest.__sha256(msg, is_hex)

    @staticmethod
    def hash256(msg: bytes, is_hex=False):
        digest = Digest.sha256(Digest.sha256(msg), is_hex)
        return digest

    @staticmethod
    def hash160(msg: bytes, is_hex=False):
        digest = Digest.ripemd160(Digest.__sha256(msg), is_hex)
        return digest
