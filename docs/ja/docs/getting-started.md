---
icon: lucide/package-open
---

# Getting Started { #getting-started }

## インストール方法 { #installation }

このページでは `mise` を使った手順を説明します. `uv` または `prek` がすでにある場合, そのツールのインストールに `mise` は不要です. `mise` は[公式手順](https://mise.jdx.dev/getting-started.html)で導入してください.

### `prek` で使う { #use-as-a-pre-commit-hook }

1. Gitで管理するマクロ付きOfficeファイルがあるフォルダへ移動します. このフォルダを `vba_root_folder` とします.
2. `prek` を導入します.
    1. `mise` で `prek` をインストールします.
        ```toml
        mise use prek@latest
        ```
    2. `prek` でリポジトリを初期化します. Gitフックが設定され, 初期状態の `prek.toml` が生成されます.
        ```console
        prek init
        ```
    3. `prek.toml` を編集し, 以下を追加します.
        ```console
        [[repos]]
        repo = "https://github.com/noda-hiroyuki-kit/pre-commit-VBA"
        rev = "v{{project_version}}"
        hooks = [
          { id = "extract-vba-code" },
          { id = "check-office-file-integrity" },
        ]
        ```

        !!! info
            `check-office-file-integrity` は旧 `check-excel-book-version` の後継IDです（`check-excel-book-version` は非推奨）.

### `pre_commit_vba.py` を直接使う { #use-pre-commit-vba-py-directly }

1. Gitで管理するマクロ付きOfficeファイルがあるフォルダへ移動します. このフォルダを `vba_root_folder` とします.
2. `mise` で `uv` をインストールします.
    ```console
    mise use uv@latest
    ```
3. `uv` を `--bare` オプション付きで初期化します.
    ```console
    uv init --bare
    ```
4. リポジトリの `src/pre_commit_vba` にある `pre_commit_vba.py` を `vba_root_folder` にコピーします.

## 使用方法 { #usage }

### `prek` で使う { #use-as-a-pre-commit-hook_1 }

1. 対象のマクロ付きOfficeファイルをステージングします.
    ```console
    git add .
    ```
2. `prek` を実行します.
    ```console
    prek
    ```
3. 抽出されたコードをGitで管理するため, ステージングします.
    ```console
    git add .
    ```
4. ステージングした変更に対してフックが成功することを確認するため, `prek` を再実行します.
    ```console
    prek
    ```

### `pre_commit_vba.py` を直接使う { #use-pre-commit-vba-py-directly_1 }

#### Officeファイルからコードを抽出する { #extract-code }

`vba_root_folder` で以下のコマンドを実行します.
```console
uv run pre_commit_vba.py extract
```

#### releaseブランチ名とOfficeファイル内のバージョンを照合する { #check-branch-name-against-version }

`vba_root_folder` で以下のコマンドを実行します. Officeファイル内のバージョンがreleaseブランチ名と一致すると, `Version check passed.` が出力されます.
```console
uv run pre_commit_vba.py check
```
