#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2018-2019 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

import codecs

from os import path, getcwd
from setuptools import setup, find_packages

with codecs.open(path.join(getcwd(), 'README.md')) as f:
    long_description = f.read()

setup(
    name='ontology-python-sdk',
    version='2.1.0.RC1',
    description='Comprehensive Python library for the Ontology BlockChain.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ontology',
    author_email='contact@ont.io',
    maintainer='NashMiao',
    maintainer_email='wdx7266@outlook.com',
    license='GNU Lesser General Public License v3 (LGPLv3)',
    packages=find_packages(exclude=['test_*.py', 'tests']),
    install_requires=[
        'aiohttp>=3.5.4',
        'base58>=1.0.3',
        'cryptography>=2.6.1',
        'ecdsa>=0.13',
        'mnemonic>=0.18',
        'pycryptodomex>=3.7',
        'requests>=2.21.0',
        'websockets>=7.0'
    ],
    python_requires='>=3.6',
    platforms=["all"],
    url='https://github.com/ontio/ontology-python-sdk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
