#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def str_to_bytes(s: str) -> bytes:
    if isinstance(s, bytes):
        return s
    elif isinstance(s, str):
        return s.encode('latin-1')
    else:
        return bytes(list(s))
