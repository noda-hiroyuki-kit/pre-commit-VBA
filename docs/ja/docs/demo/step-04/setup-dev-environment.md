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

## 手順 2: `uv` と `pre-commit` を入れる { #step-2-install-uv-and-pre-commit }

```console
mise use uv@latest
uv init
uv add --dev pre-commit
uv run pre-commit install
```

## 手順 3: 設定ファイルを作る { #step-3-create-configuration-files }

1. `.pre-commit-config.yaml` を作成します.

    ???+ info ".pre-commit-config.yaml"
        ```yaml title=".pre-commit-config.yaml"
        ---
        repos:
          - repo: https://github.com/noda-hiroyuki-kit/pre-commit-vba
            rev: v{{project_version}}
            hooks:
              - id: extract-vba-code
              - id: check-office-file-integrity
          - repo: https://github.com/streetsidesoftware/cspell-cli
            rev: v10.2.0
            hooks:
              - id: cspell  # Spell check changed files
              - id: cspell  # Spell check the commit message
                name: check commit message spelling
                args:
                  - --no-must-find-files
                  - --no-progress
                  - --no-summary
                stages: [commit-msg]
          - repo: https://github.com/pre-commit/pre-commit-hooks
            rev: v6.0.0
            hooks:
              - id: trailing-whitespace
                args: [--markdown-linebreak-ext=md]
              - id: end-of-file-fixer
              - id: check-toml
              - id: check-xml
              - id: destroyed-symlinks
              - id: check-json
              - id: mixed-line-ending
                args: [--fix=lf]
          - repo: https://github.com/adrienverge/yamllint.git
            rev: v1.38.0
            hooks:
              - id: yamllint
                args:
                  - --strict
                  - -d
                  - "{extends: default, rules: {indentation: {spaces: 2}}}"
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
                "Predeclared"
            ]
        }
        ```

## 手順 4: フックを実行して整形 { #step-4-run-hooks-and-format }

```powershell
git add .
uv run pre-commit
uv run pre-commit run --all-files
git commit -m "chore: set up development environment"
```

## 手順 5: `develop` にマージ { #step-5-merge-into-develop }

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

- `uv run pre-commit run --all-files` が通る.
- `develop` に設定ファイルが入っている.
