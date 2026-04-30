---
icon: lucide/rocket
---

# インストール方法

いずれの方法も`mise`を利用した方法を記載しています.  
[`mise`](https://mise.jdx.dev/getting-started.html)を参考に`mise`をインストールしてください.
`uv`が利用できる場合は, `mise`は不要です.

## pre-commitで, pre-commit-hookとして使用

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
            rev: v0.3.0
            hooks:
            - id: extract-vba-code
            - id: check-excel-book-version

        ```
## `pre_commit_vba.py`をコマンドで走らせて使用

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
