---
icon: lucide/package-open
---

# Getting Started

## インストール方法

このページは `mise` 前提で説明します.  
`uv` がある場合は `mise` は不要です.  
`mise` は[公式手順](https://mise.jdx.dev/getting-started.html)で導入してください.

### pre-commit フックとして使う

1. ブックの管理フォルダへ移動します.  
   このフォルダを `vba_root_folder` とします.
2. `pre-commit` を導入します.
    1. `mise` で `uv` を入れます.
        ```console
        mise use uv@latest
        ```
    2. `uv` を初期化します.
        ```console
        uv init
        ```
    3. `pre-commit` を追加します.
        ```console
        uv add pre-commit
        uv run pre-commit install
        ```
    4. `.pre-commit-config.yaml` を作成します.
        ```yaml title=".pre-commit-config.yaml"
        ---
        repos:
          - repo: https://github.com/noda-hiroyuki-kit/pre-commit-vba
            rev: v0.3.9
            hooks:
              - id: extract-vba-code
              - id: check-excel-book-version
        ```

### `pre_commit_vba.py` を直接使う

1. `vba_root_folder` へ移動します.
2. `mise` で `uv` を入れます.
    ```console
    mise use uv@latest
    ```
3. `uv` を初期化します.
    ```console
    uv init
    ```
4. `pre_commit_vba.py` をコピーします.

## 使用方法

### pre-commit フックとして使う

1. マクロブック(例: sample-app.xlsm)をステージングします.
    ```console
    git add sample-app.xlsm
    ```  
2. `pre-commit` を実行します.
    ```console
    uv run pre-commit
    ```  
3. `pre-commit` を再実行します. (展開コードは前回実行時にステージングされます.)
    ```console
    uv run pre-commit
    ```

### `pre_commit_vba.py` を直接使う

#### コード抽出

```console
uv run pre_commit_vba.py extract
```

#### ブランチ名とバージョンとの照合

```console
uv run pre_commit_vba.py check
```
