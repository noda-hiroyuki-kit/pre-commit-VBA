---
icon: lucide/package-open
---

# Getting Started { #getting-started }

## Installation { #installation }

This page explains setup using `mise`. If you already have `uv` or `prek`, you do not need `mise` to install that tool. Install `mise` using the [official instructions](https://mise.jdx.dev/getting-started.html).

### Use with `prek` { #use-as-a-pre-commit-hook }

1. Move to the folder containing the macro-enabled Office files you want to manage with Git. This folder is referred to as `vba_root_folder`.
2. Install `prek`.
    1. Install `prek` with `mise`.
        ```console
        mise use prek@latest
        ```
    2. Initialize the repository with `prek`. This sets up the Git hook and creates a starter `prek.toml`.
        ```console
        prek init
        ```
    3. Edit `prek.toml` and add the following:
        ```toml
        [[repos]]
        repo = "https://github.com/noda-hiroyuki-kit/pre-commit-vba"
        rev = "v{{project_version}}"
        hooks = [
          { id = "extract-vba-code" },
          { id = "check-office-file-integrity" },
        ]
        ```

        !!! info
            `check-office-file-integrity` is the successor of the deprecated `check-excel-book-version` id.

### Use `pre_commit_vba.py` directly { #use-pre-commit-vba-py-directly }

1. Move to the folder containing the macro-enabled Office files you want to manage with Git. This folder is referred to as `vba_root_folder`.
2. Install `uv` with `mise`.
    ```console
    mise use uv@latest
    ```
3. Initialize `uv` with `--bare`.
    ```console
    uv init --bare
    ```
4. Copy `pre_commit_vba.py` from `src/pre_commit_vba` in the repository to `vba_root_folder`.

## Usage { #usage }

### Use with `prek` { #use-as-a-pre-commit-hook_1 }

1. Stage the target macro-enabled Office files.
    ```console
    git add .
    ```
2. Run `prek`.
    ```console
    prek
    ```
3. Stage the extracted code so it can be managed with Git.
    ```console
    git add .
    ```
4. Run `prek` again to confirm that the staged changes pass the hooks.
    ```console
    prek
    ```

### Use `pre_commit_vba.py` directly { #use-pre-commit-vba-py-directly_1 }

#### Extract code from Office files { #extract-code }

Run this command in `vba_root_folder`:
```console
uv run pre_commit_vba.py extract
```

#### Check the release branch against the Office file version { #check-branch-name-against-version }

Run this command in `vba_root_folder`. If the version recorded in the Office file matches the release branch name, the command prints `Version check passed.`.
```console
uv run pre_commit_vba.py check
```
