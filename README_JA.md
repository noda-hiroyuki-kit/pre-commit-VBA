# Pre-commit VBA

[**English**](README.md)

[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENCE)

[Document](https://noda-hiroyuki-kit.github.io/pre-commit-VBA/)

## 概要

VBAコードをgitで管理するため, OfficeファイルからVBAコードを抽出するpre-commitフックです.
Pythonスクリプトとしても利用できます.

### pre-commitで, pre-commit-hookとして使用

以下のように`prek.toml`に追加してください.

```
[[repos]]
repo = "https://github.com/noda-hiroyuki-kit/pre-commit-vba"
rev = "v0.4.4"
hooks = [
  { id = "extract-vba-code" },
  { id = "check-office-file-integrity" },
]
```

### `pre_commit_vba.py`をコマンドで実行して使用

uvをインストールしたのち,
```console
uv run pre_commit_vba.py extract
```
これにより, OfficeファイルからコードをUTF-8形式で出力します.

また, Gitのreleaseブランチで作業している際に,
```console
uv run pre_commit_vba.py check
```
を実行すると, Officeファイル内のバージョンとブランチ名を比較し, 一致している場合は
```console
Version check passed.
```
を出力します.

## インストール方法

いずれの方法も`mise`を利用した手順です.
[`mise`](https://mise.jdx.dev/getting-started.html)を参考に, `mise`をインストールしてください.

### `prek`で, hookとして使用

1. `git`で管理するマクロ付きOfficeファイルのあるフォルダ (以下, vba_root_folder) に移動する.
2. `prek`をインストールする.
    1. `mise`を使って`prek`をインストールする.
        ```
        mise use prek@latest
        ```
    2. リポジトリを初期化する. スタート用の`prek.toml`が生成される.
        ```
        prek init
        ```
    3. `prek.toml`を編集し, 以下を追記する.
        ```
        [[repos]]
        repo = "https://github.com/noda-hiroyuki-kit/pre-commit-vba"
        rev = "v0.4.4"
        hooks = [
            { id = "extract-vba-code" },
            { id = "check-office-file-integrity" },
        ]
        ```
### `pre_commit_vba.py`をコマンドで実行して使用

1. `git`で管理するマクロ付きOfficeファイルのあるフォルダ (以下, vba_root_folder) に移動する.
2. `mise`で`uv`をインストールする.
    ```console
    mise use uv@latest
    ```
3. `uv`を初期化する.
    ```
    uv init --bare
    ```
4. `src/pre_commit_vba`にある`pre_commit_vba.py`をvba_root_folderにコピーする.


## 使用方法

### prekで, pre-commit-hookとして使用

1. 対象のマクロ付きOfficeファイルを`git`でステージングする.
    ```
    git add .
    ```
2. `prek`を実行する.
    ```
    prek
    ```
3. コードが展開されるので, コードをステージングして`git`で管理する.
    ```
    git add .
    ```
4. `prek`を再実行し, 更新後のステージ内容でフックが成功することを確認する.
    ```
    prek
    ```

### `pre_commit_vba.py`をコマンドで実行して使用

#### Officeファイルにあるコードを抽出する場合

vba_root_folderで, 以下のコマンドを実行します.
```console
uv run pre_commit_vba.py extract
```

#### releaseブランチ名とOffice ファイルのバージョン情報を比較チェックする場合

vba_root_folderで, 以下のコマンドを実行します.
```PowerShell
uv run pre_commit_vba.py check
```

#### コマンドラインについて

以下は, コマンド (`uv run typer src\pre_commit_vba\pre_commit_vba.py utils docs`) で生成したドキュメントです.

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

* `extract`: Extract VBA code from Office files.
* `check`: Check Office file version and detect Rubberduck Add-in references.

## `extract`

Extract VBA code from Office files.

**Usage**:

```console
$ extract [OPTIONS]
```

**Options**:

* `--target-path <str>`: [default: .]
* `--folder-suffix <str>`: [default: .VBA]
* `--export-folder <str>`: [default: export]
* `--custom-ui-folder <str>`: [default: customUI]
* `--code-folder <str>`: [default: code]
* `--version`
* `--enable-folder-annotation / --disable-folder-annotation`: [default: enable-folder-annotation]
* `--create-gitignore / --not-create-gitignore`: [default: create-gitignore]
* `--include-extension / --exclude-extension`: [default: include-extension]
* `--help`: Show this message and exit.

## `check`

Check Office file version and detect Rubberduck Add-in references.

**Usage**:

```console
$ check [OPTIONS]
```

**Options**:

* `--target-path <str>`: [default: .]
* `--version`
* `--help`: Show this message and exit.

## コミュニティ

[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)を確認してください.


## 参考情報

### pre_commit_vba.py

[Agent6-6-6/Excel-VBA-XML-Export-Pre-Commit-Hook](https://github.com/Agent6-6-6/Excel-VBA-XML-Export-Pre-Commit-Hook)

[gitのbranch名,tag名をpythonで取得する](https://qiita.com/mynkit/items/73b20fb0ad124c0ea8e9)

### tests/excel/extract/with_codes/v0.0.1-alpha/test.xlsm

[git repository office custom ui editor](https://github.com/OfficeDev/office-custom-ui-editor)

[Excel のリボンUIを業務アプリとして使う](https://qiita.com/tomochan154/items/3614b6f3ebc9ef947719)

[RubberDuckでテスト駆動開発したXLSMの配布時にコンパイラ動作を簡単切替 by @ShortArrow(さぼったろう)](https://qiita.com/ShortArrow/items/a16477a0926a68a88ead)
