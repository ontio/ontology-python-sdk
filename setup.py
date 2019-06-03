#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

from os import path, getcwd
from setuptools import setup, find_packages

with codecs.open(path.join(getcwd(), 'README.md')) as f:
    long_description = f.read()

setup(
    name='ontology-python-sdk',
    version='2.0.4',
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
