#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

from os import path, getcwd
from setuptools import setup, find_packages

with codecs.open(path.join(getcwd(), 'description.md')) as f:
    long_description = f.read()

setup(
    name='ontology-python-sdk',
    version='1.4.0',
    description='Comprehensive Python library for the Ontology BlockChain.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ontology',
    author_email='contact@ont.io',
    maintainer='NashMiao',
    maintainer_email='wdx7266@outlook.com',
    license='GNU Lesser General Public License v3 (LGPLv3)',
    packages=find_packages(exclude=['test_*.py', 'test']),
    install_requires=[
        'pycryptodomex',
        'cryptography',
        'ecdsa',
        'base58',
        'requests',
        'websockets'
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
    ],
)
