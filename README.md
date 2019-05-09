<h1 align="center">Ontology Python SDK</h1>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9078ef6584424280b8d6b75556976f94)](https://www.codacy.com/app/NashMiao/ontology-python-sdk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ontio/ontology-python-sdk/&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/9078ef6584424280b8d6b75556976f94)](https://www.codacy.com/app/NashMiao/ontology-python-sdk?utm_source=github.com&utm_medium=referral&utm_content=ontio/ontology-python-sdk/&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.com/ontio/ontology-python-sdk.svg?branch=master)](https://travis-ci.com/ontio/ontology-python-sdk)
[![pypi-w](https://img.shields.io/pypi/wheel/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)
[![docs](https://img.shields.io/badge/docs-yes-brightgreen.svg)](https://apidoc.ont.io/pythonsdk/#introduction)
[![pypi-pyversions](https://img.shields.io/pypi/pyversions/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)
[![pypi-v](https://img.shields.io/pypi/v/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)

- [Introduction](#introduction)
- [Preparations](#preparations)
- [Interface](#interface)
- [Contribution](#contribution)
- [License](#license)

English | [中文](README_CN.md)

## Introduction

The Ontology official Python SDK is a comprehensive SDK which is based on `Python 3.6`. Currently, it supports wallet management, digital identity management, digital asset management, deployment and invoke smart contract, and communication with the Ontology blockchain.

## Preparations

Installation requires a `Python 3.6` or later environment.

```bash
pip install ontology-python-sdk
```

## Interface

Read more in the [API document](https://apidoc.ont.io/pythonsdk/).

## Contribution

Can I contribute patches to Ontology project?

Yes! Please open a pull request with signed-off commits. We appreciate your help!

You can also send your patches as emails to the developer mailing list. Please join the Ontology mailing list or forum and talk to us about it.

Either way, if you don't sign off your patches, we will not accept them. This means adding a line that says "Signed-off-by: Name <email>" at the end of each commit, indicating that you wrote the code and have the right to pass it on as an open source patch.

Also, please write good git commit messages.  A good commit message looks like this:

Header line: explain the commit in one line (use the imperative)

Body of commit message is a few lines of text, explaining things in more detail, possibly giving some background about the issue being fixed, etc etc.

The body of the commit message can be several paragraphs, and please do proper word-wrap and keep columns shorter than about 74 characters or so. That way "git log" will show things nicely even when it's indented.

Make sure you explain your solution and why you're doing what you're doing, as opposed to describing what you're doing. Reviewers and your future self can read the patch, but might not understand why a particular solution was implemented.

Reported-by: whoever-reported-it

Signed-off-by: Your Name <youremail@yourhost.com>

## License

The Ontology library (i.e. all code outside of the cmd directory) is licensed under the GNU Lesser General Public License v3.0, also included in our repository in the License file.
