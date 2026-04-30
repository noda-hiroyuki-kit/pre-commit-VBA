---
icon: lucide/house
---

# pre-commit-vba

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENCE)

## 概要

ExcelのVBAコードをgitで管理するため, ExcelファイルよりVBAコードを抽出するpre-commit フックです.  
Pythonのスクリプトとしても利用可能です.  

### pre-commitで, pre-commit-hookとして使用

以下のように`.pre-commit-config.yaml`に追加してください.

```
  - repo: https://github.com/noda-hiroyuki-kit/pre-commit-vba
    rev: v0.3.0
    hooks:
      - id: extract-vba-code
      - id: check-excel-book-version
```

### `pre_commit_vba.py`をコマンドで走らせて使用

uvをインストールしたのち,
```console
uv run pre_commit_vba.py extract
```
でExcelファイルよりコードをutf-8形式で出力します.

また, `Git`の`release/v[セマンティック バージョニング]` または, `hotfix/v[セマンティック バージョニング]`ブランチで作業している際に,
```console
uv run pre_commit_vba.py check
```
を実行すると, Excelファイルの文書のバージョンとブランチ名を比較して一致している場合は
```console
Version check passed.
```
を出力します.
