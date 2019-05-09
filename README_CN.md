<h1 align="center">本体 Python 软件开发工具包</h1>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9078ef6584424280b8d6b75556976f94)](https://www.codacy.com/app/NashMiao/ontology-python-sdk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ontio/ontology-python-sdk/&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/9078ef6584424280b8d6b75556976f94)](https://www.codacy.com/app/NashMiao/ontology-python-sdk?utm_source=github.com&utm_medium=referral&utm_content=ontio/ontology-python-sdk/&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.com/ontio/ontology-python-sdk.svg?branch=master)](https://travis-ci.com/ontio/ontology-python-sdk)
[![pypi-w](https://img.shields.io/pypi/wheel/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)
[![docs](https://img.shields.io/badge/docs-yes-brightgreen.svg)](https://apidoc.ont.io/pythonsdk/#introduction)
[![pypi-pyversions](https://img.shields.io/pypi/pyversions/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)
[![pypi-v](https://img.shields.io/pypi/v/ontology-python-sdk.svg)](https://pypi.org/project/ontology-python-sdk/)

- [简介](#简介)
- [准备](#准备)
- [接口](#接口)
- [参与项目](#参与项目)
- [许可证](#许可证)

[English](README.md) | 中文

## 简介

本体团队的官方 Python SDK 基于 Python 3.6 实现。目前，它支持钱包文件管理、数字身份管理、数字资产管理、智能合约的部署和调用、以及与本体区块链网络的通信。

## 准备

安装需要 `Python 3.6` 或更高版本的环境。

```bash
pip install ontology-python-sdk
```

## 接口

你可以点击[这里](https://apidoc.ont.io/pythonsdk/)访问我们的 API 文档。

## 参与项目

我可以为Ontology项目做贡献吗？

当然可以！请发起一个带有打开带有签名提交的拉取请求。我们非常感谢你您的帮助！

你还可以将补丁通过电子邮件的方式发送到开发人员邮件列表。请加入 Ontology 邮件列表或论坛，与我们讨论。

无论哪种方式，如果您不签署补丁，我们将不接受。这意味着在每次提交结束时添加一行`Signed-off-by：Name <email>`，表示你编写了代码并将其作为开源补丁传递。

另外，请写好git提交消息。一个好的提交消息如下所示：

标题行：在一行中解释提交（使用命令）

提交消息的主体是几行文本，更详细地解释事情，可能提供有关修复问题的一些背景等。

提交消息的主体可以是几个段落，请做正确的自动换行并保持列短于约74个字符左右。这样`git log`即使缩进也能很好地显示出来。

确保解释清楚你的解决方案以及为什么你正在做你正在做的事情，而不是描述你正在做的事情。审稿人和您未来的自己可以阅读补丁，但可能无法理解为什么要实施特定的解决方案。

> Reported-by: whoever-reported-it

> Signed-off-by: Your Name <youremail@yourhost.com>

## 许可证

所有Ontology的库（即cmd目录之外的所有代码）遵循 GNU Lesser General Public License v3.0 许可，该许可证文件也包含在我们的存储库中。
