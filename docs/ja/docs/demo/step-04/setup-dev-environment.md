---
icon: lucide/tool-case
---
# 開発環境の構築 { #set-up-the-development-environment }

## 目的 { #objective }

`pre-commit-vba` を使う開発環境を準備します.

## 手順 1: ブランチを作る { #step-1-create-a-branch }

```console
git checkout develop
git pull
git switch -c feature/setup-dev-environment
```

## 手順 2: `prek` を入れる { #step-2-install-prek }

```console
mise use prek@latest
prek init
```

## 手順 3: 設定ファイルを作る { #step-3-create-configuration-files }

1. `prek.toml` を編集します.

    ???+ info "prek.toml"
        ```toml title="prek.toml"
        # Configuration file for `prek`, a git hook framework written in Rust.
        # See https://prek.j178.dev for more information.
        #:schema https://www.schemastore.org/prek.json

        default_install_hook_types = ["pre-commit", "commit-msg"]

        [[repos]]
        repo = "https://github.com/noda-hiroyuki-kit/pre-commit-vba"
        rev = "v{{project_version}}"
        hooks = [
          { id = "extract-vba-code" },
          { id = "check-office-file-integrity" },
        ]

        [[repos]]
        repo = "https://github.com/streetsidesoftware/cspell-cli"
        rev = "v10.2.0"

        [[repos.hooks]]
        id = "cspell"
        name = "Spell check changed files"

        [[repos.hooks]]
        id = "cspell"
        name = "check commit message spelling"
        args = ["--no-must-find-files", "--no-progress", "--no-summary"]
        stages = ["commit-msg"]

        [[repos]]
        repo = "builtin"
        hooks = [
          { id = "trailing-whitespace", args = ["--markdown-linebreak-ext=md"] },
          { id = "end-of-file-fixer" },
          { id = "check-toml" },
          { id = "check-xml" },
          { id = "destroyed-symlinks" },
          { id = "check-json" },
          { id = "mixed-line-ending", args = ["--fix=lf"] },
        ]

        [[repos]]
        repo = "https://github.com/adrienverge/yamllint.git"
        rev = "v1.38.0"
        hooks = [
          { id = "yamllint", args = ["--strict", "-d", "{extends: default, rules: {indentation: {spaces: 2}}}"] },
        ]
        ```

2. `cspell.json` を作成します.

    ???+ info "cspell.json"
        ```json title="cspell.json"
        {
            "version": "0.2",
            "language": "en",
            "dictionaries": [
                "python",
                "powershell"
            ],
            "ignorePaths": [
                "**/*.svg",
                "uv.lock"
            ],
            "words": [
                "EDITMSG",
                "Predeclared",
                "prek",
                "VBIDE"
            ]
        }
        ```

## 手順 4: フックを設定 { #step-4-set-hooks }

```powershell
prek install
```

## 手順 5: フックを実行して整形 { #step-5-run-hooks-and-format }

```powershell
git add .
prek run --all-files
```

フックがファイルを変更した場合は変更内容を確認し, すべてのフックが成功するまで `git add .` と `prek run --all-files` を繰り返します. 成功した後にコミットします.

```powershell
git commit -m "chore: set up development environment"
```

## 手順 6: `develop` にマージ { #step-6-merge-into-develop }

```powershell
git push -u origin feature/setup-dev-environment
```

その後, GitHub で PR を作成して `develop` にマージします.  
マージ後にローカルを同期します.

```console
git switch develop
git pull
git branch -D feature/setup-dev-environment
```

## 確認ポイント { #checkpoints }

- `prek run --all-files` が通る.
- `develop` に設定ファイルが入っている.
