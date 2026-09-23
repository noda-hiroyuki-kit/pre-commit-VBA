---
icon: lucide/tool-case
---
# Set Up the Development Environment { #set-up-the-development-environment }

## Objective { #objective }

Prepare a development environment that uses `pre-commit-vba`.

## Step 1: Create a Branch { #step-1-create-a-branch }

```console
git checkout develop
git pull
git switch -c feature/setup-dev-environment
```

## Step 2: Install `uv` and `prek` { #step-2-install-uv-and-prek }

```console
mise use uv@latest
uv init --bare
uv add --dev prek
uv run prek install
```

## Step 3: Create Configuration Files { #step-3-create-configuration-files }

1. Create `.pre-commit-config.yaml`.

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
          - repo: builtin
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
                "Predeclared",
                "prek",
                "VBIDE"
            ]
        }
        ```

## Step 4: Run Hooks and Format { #step-4-run-hooks-and-format }

```powershell
git add .
uv run prek
uv run prek run --all-files
git commit -m "chore: set up development environment"
```

## Step 5: Merge into `develop` { #step-5-merge-into-develop }

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

## Checkpoints { #checkpoints }

- `uv run prek run --all-files` passes.
- Configuration files are included in `develop`.
