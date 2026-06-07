---
icon: lucide/package-open
---

# getting-started

## インストール方法

いずれの方法も`mise`を利用した方法を記載しています.  
[`mise`](https://mise.jdx.dev/getting-started.html)を参考に`mise`をインストールしてください.
`uv`が利用できる場合は, `mise`は不要です.

### pre-commitで, pre-commit-hookとして使用

1. `git`管理するマクロ付きブックのあるフォルダ(以下, vba_root_folderという)に移動する.
2. `.pre-commit`をインストールする.
    1. `uv`を`mise`を使ってインストールする.
        ```
        mise use uv@latest
        ```
    2. `uv`を初期化する.
        ```
        uv init
        ```
    3. `pre-commit`をインストールする.
        ```
        uv add pre-commit
        uv run pre-commit install
        ```
    4. `.pre-commit-config.yaml`を作成し, 以下を記載する.
        ```
        ---
        repos:
        - repo: https://github.com/noda-hiroyuki-kit/pre-commit-vba
            rev: v0.3.3
            hooks:
            - id: extract-vba-code
            - id: check-excel-book-version

        ```
### `pre_commit_vba.py`をコマンドで走らせて使用

1. `git`管理するマクロ付きブックのあるフォルダ(以下, vba_root_folderという)に移動する.
2. `mise`で `uv`をインストールする.
    ```console
    mise use uv@latest
    ```
3. `uv`を初期化する.
    ```
    uv init
    ```
3. `src/pre_commit_vba`にある`pre_commit_vba.py`をvba_root_folderにコピーする.

## 使用方法

### pre-commitで, pre-commit-hookとして使用

1. 対象のマクロブックを`git`でステージングする.
    ```
    git add .
    ```
2. uvで`pre-commit`を動作させる.
    ```
    uv run pre-commit
    ```
3. コードが展開されるので, コードをステージングし`git`で管理する.
    ```
    git add .
    ```

### `pre_commit_vba.py`をコマンドで走らせて使用

#### ブックにあるコードを抽出する場合

vba_root_folderにて, 以下のコマンドを実行.
```console
uv run pre_commit_vba.py extract
```

#### releaseブランチ名とワークブックのバージョン情報を比較チェックする場合

vba_root_folderにて, 以下のコマンドを実行.
```PowerShell
uv run pre_commit_vba.py check
```
