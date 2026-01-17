# Pre-commit VBA

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENCE)

## 概要

ExcelのVBAコードをgitで管理するため, ExcelファイルよりVBAコードを抽出するPythonのスクリプトです.

uvをインストールしたのち,
```console
uv run pre_commit_vba.py extract
```
でExcelファイルよりコードをutf-8形式で出力します.

また, Gitのreleaseブランチで作業している際に,
```console
uv run pre_commit_vba.py check
```
を実行すると, Excelファイルの文書のバージョンとブランチ名を比較して一致している場合は
```console
Version check passed.
```
を出力します.

## インストール方法

1. [`mise`](https://mise.jdx.dev/getting-started.html)をインストールする.
2. `git`管理するマクロ付きブックのあるフォルダ(以下, vba_root_folderという)に移動する.
3. `mise`で `uv`をインストールする.
```console
mise use uv@latest
```
4. `pre_commit_vba.py`をvba_root_folderにコピーする.

## 使用方法

### ブックにあるコードを抽出する場合

vba_root_folderにて, 以下のコマンドを実行.
```console
uv run pre_commit_vba.py extract
```

### releaseブランチ名とワークブックのバージョン情報を比較チェックする場合

vba_root_folderにて, 以下のコマンドを実行.
```PowerShell
uv run pre_commit_vba.py check
```

### コマンドラインについて

以下は, コマンド(`uv run typer pre_commit_vba.py utils docs`)にて生成したドキュメント.

---
**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `extract`: Extract VBA code from Excel workbooks.
* `check`: Check between workbook version and...

## `extract`

Extract VBA code from Excel workbooks.

**Usage**:

```console
$ extract [OPTIONS]
```

**Options**:

* `--target-path TEXT`: [default: .]
* `--folder-suffix TEXT`: [default: .VBA]
* `--export-folder TEXT`: [default: export]
* `--custom-ui-folder TEXT`: [default: customUI]
* `--code-folder TEXT`: [default: code]
* `--version`
* `--enable-folder-annotation / --disable-folder-annotation`: [default: enable-folder-annotation]
* `--create-gitignore / --not-create-gitignore`: [default: create-gitignore]
* `--help`: Show this message and exit.

## `check`

Check between workbook version and repository name.

**Usage**:

```console
$ check [OPTIONS]
```

**Options**:

* `--target-path TEXT`: [default: .]
* `--version`
* `--help`: Show this message and exit.

## 参考情報

[Agent6-6-6/Excel-VBA-XML-Export-Pre-Commit-Hook](https://github.com/Agent6-6-6/Excel-VBA-XML-Export-Pre-Commit-Hook)

[git repository office custom ui editor](https://github.com/OfficeDev/office-custom-ui-editor)

[Excel のリボンUIを業務アプリとして使う](https://qiita.com/tomochan154/items/3614b6f3ebc9ef947719)

[gitのbranch名,tag名をpythonで取得する](https://qiita.com/mynkit/items/73b20fb0ad124c0ea8e9)
