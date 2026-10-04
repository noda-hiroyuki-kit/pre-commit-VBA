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

## Step 2: Install `prek` { #step-2-install-prek }

```console
mise use prek@latest
prek init
```

## Step 3: Create Configuration Files { #step-3-create-configuration-files }

1. Edit `prek.toml`.

    ???+ info "prek.toml"
        ```toml title="prek.toml"
        # Configuration file for `prek`, a git hook framework written in Rust.
        # See https://prek.j178.dev for more information.
        #:schema https://www.schemastore.org/prek.json

        [[repos]]
        repo = "https://github.com/noda-hiroyuki-kit/pre-commit-VBA"
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
prek run --all-files
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

- `prek run --all-files` passes.
- Configuration files are included in `develop`.
