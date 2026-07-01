---
icon: lucide/house
---

# pre-commit-vba

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENCE)

`pre-commit-vba` は、Excel ブックから VBA コードを抽出して Git で管理しやすくするための Python ツールです。

## このドキュメントでできること

- インストール方法, 使い方を確認する: [getting started](getting-started.md)
- 設定項目を確認する: [オプション ガイド](options-guide.md)
- 実際の利用方法を確認する: [デモ](demo/sample-usage.md)
- 開発への参加方法を確認する: [貢献](contributing.md)
- 行動規範を確認する: [行動規範](code-of-conduct.md)
- CLI仕様, 内部処理を確認する: [リファレンス](reference.md)

## 概要

このプロジェクトは, Excel VBA プロジェクトのソース管理を効率化することを目的としています.
pre-commit フックとして実行し, コミット時に VBA コードの抽出や検証を行えるようにします.
