---
icon: lucide/tool-case
---
# Set Up the Development Environment

## Objective

Prepare a development environment that uses `pre-commit-vba`.

## Step 1: Create a Branch

```console
git checkout develop
git pull
git switch -c feature/setup-dev-environment
```

## Step 2: Install `uv` and `pre-commit`

```console
mise use uv@latest
uv init
uv add --dev pre-commit
uv run pre-commit install
```

## Step 3: Create Configuration Files

1. Create `.pre-commit-config.yaml`.

    ???+ info ".pre-commit-config.yaml"
        ```yaml title=".pre-commit-config.yaml"
        ---
        repos:
          - repo: https://github.com/noda-hiroyuki-kit/pre-commit-vba
            rev: v0.3.10
            hooks:
              - id: extract-vba-code
              - id: check-excel-book-version
          - repo: https://github.com/streetsidesoftware/cspell-cli
            rev: v10.0.1
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

2. Create `cspell.json`.

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

## Step 4: Run Hooks and Format

```powershell
git add .
uv run pre-commit
uv run pre-commit run --all-files
git commit -m "chore: set up development environment"
```

## Step 5: Merge into `develop`

```powershell
git push -u origin feature/setup-dev-environment
```

After that, create a PR on GitHub and merge it into `develop`.  
After merge, sync your local repository.

```console
git switch develop
git pull
git branch -D feature/setup-dev-environment
```

## Checkpoints

- `uv run pre-commit run --all-files` passes.
- Configuration files are included in `develop`.
