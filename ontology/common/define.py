#!/usr/bin/env python3
# -*- coding: utf-8 -*-

VERSION_TRANSACTION = b'\x00'
VERSION_CONTRACT_ONT = b'\x00'
VERSION_CONTRACT_ONG = b'\x00'

NATIVE_TRANSFER = 'transfer'
NATIVE_TRANSFER_FROM = 'transferFrom'
NATIVE_APPROVE = 'approve'
NATIVE_ALLOWANCE = 'allowance'
DID_ONT = 'did:ont:'

# NeoVM invokes a smart contract return type

NEOVM_TYPE_BOOL = 1
NEOVM_TYPE_INTEGER = 2
NEOVM_TYPE_BYTE_ARRAY = 3
NEOVM_TYPE_STRING = 4
UINT256_SIZE = 32
