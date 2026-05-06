# 開発環境の構築

## 開発ブランチの作成

1. `develop`ブランチにおり, リモート リポジトリと同期できているかを確認する.
    ```powershell
    git status
    ```
    ```powershell hl_lines="2 3"
    PS %current directory%> git status
    On branch develop
    Your branch is up to date with 'origin/develop'.

    nothing to commit, working tree clean
    ```

1. `feature/setup-dev-environment`ブランチを作成する.  
    ```powershell
     git branch feature/setup-dev-environment
    ```

3. `feature/setup-dev-environment`ブランチへ移動する.
    ```powershell
    git checkout feature/setup-dev-environment
    ```
## uvをmiseを利用してインストール

```powershell
mise use uv@latest
```
`mise.toml`が生成される.

## uvを利用して, pre-commitをインストール

1. uvを初期化する.
    ```powershell
    uv init
    ```
    `pyproject.toml`, `.python-version`, `main.py`が生成される. `main.py`は不要なので削除する.

2. pre-commitをインストールする.
    ```powershell
    uv add --dev pre-commit
    ```

3. pre-commitを初期化する.
    ```powershell
    uv run pre-commit install
    ```

4. `.pre-commit-config.yaml`を作成する.
    ```yaml title=".pre-commit-config.yaml"
    ---
    repos:
      - repo: https://github.com/noda-hiroyuki-kit/pre-commit-vba
        rev: v0.3.0
        hooks:
          - id: extract-vba-code
          - id: check-excel-book-version
      - repo: https://github.com/streetsidesoftware/cspell-cli
        rev: v10.0.0
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

4. `cspell.json`を作成する.
    ```json title="cspell.json"
    {
        "version": "0.2",
        "language": "en",
        "dictionaries": [
            "python",
            "powershell"
        ],
        "ignorePaths": [
            "*.svg",
            "uv.lock"
        ],
        "words": [
            "EDITMSG"
        ]
    }
    ```

5. 全てのファイルをステージングする.
    ```powershell
    git add .
    ```

6. `pre-commit`を走らせて, ファイルを整える.
    ```powershell
    uv run pre-commit
    ```
    全てがOKとなると以下のような表示になる.
    ```powershell
    PS %current directory%>uv run pre-commit
    Extract VBA code from Excel files....................(no files to check)Skipped
    Check Excel book version.................................................Passed
    cspell...................................................................Passed
    trim trailing whitespace.................................................Passed
    fix end of files.........................................................Passed
    check toml...............................................................Passed
    check xml............................................(no files to check)Skipped
    detect destroyed symlinks................................................Passed
    check json...............................................................Passed
    mixed line ending........................................................Passed
    yamllint.................................................................Passed
    ```

8. コミットする.
9. 全てのファイルを`pre-commit`で整形し、コミットする.
    ```powershell
    uv run pre-commit run --all-files
    ```
    ```powershell
    git commit -m "chore: fixing files with pre-commit"
    ```

## `develop`ブランチにマージする.

詳細は, `feature/setup-repository`ブランチを`develop`ブランチにマージした手順を参照のこと.

1. `feature/setup-dev-environment`ブランチをリモート リポジトリにプッシュ.
    ```powershell
    git push -u origin feature/setup-dev-environment
    ```

2. ブラウザで, `feature/setup-dev-environment`ブランチを`develop`ブランチにマージするpull requestを作成する. その後, マージリクエストを作成し, マージを確定する.

3. リモート リポジトリの`feature/setup-dev-environment`ブランチを削除する.
4. ローカル リポジトリで `develop`ブランチに移動する.
    ```powershell
    git checkout develop
    ```
5. リモート リポジトリと同期する.
    ```powershell
    git pull
    ```
6. ローカル リポジトリの`feature/setup-dev-environment`ブランチを削除する.
    ```powershell
    git branch -D feature/setup-dev-environment
    ```
