---
icon: lucide/package-open
---

# Getting Started

## Installation

This page explains setup assuming you use `mise`.  
If you already have `uv`, `mise` is not required.  
Install `mise` using the [official instructions](https://mise.jdx.dev/getting-started.html).

### Use as a pre-commit hook

1. Move to your workbook management folder.  
   This folder is referred to as `vba_root_folder`.
2. Install `pre-commit`.
    1. Install `uv` with `mise`.
        ```console
        mise use uv@latest
        ```
    2. Initialize `uv`.
        ```console
        uv init
        ```
    3. Add `pre-commit`.
        ```console
        uv add pre-commit
        uv run pre-commit install
        ```
    4. Create `.pre-commit-config.yaml`.
        ```yaml title=".pre-commit-config.yaml"
        ---
        repos:
          - repo: https://github.com/noda-hiroyuki-kit/pre-commit-vba
            rev: v{{project_version}}
            hooks:
              - id: extract-vba-code
              - id: check-excel-book-version
        ```

### Use `pre_commit_vba.py` directly

1. Move to `vba_root_folder`.
2. Install `uv` with `mise`.
    ```console
    mise use uv@latest
    ```
3. Initialize `uv`.
    ```console
    uv init
    ```
4. Copy `pre_commit_vba.py`.

## Usage

### Use as a pre-commit hook

1. Stage your macro workbook (for example, `sample-app.xlsm`).
    ```console
    git add sample-app.xlsm
    ```  
2. Run `pre-commit`.
    ```console
    uv run pre-commit
    ```  
3. Run `pre-commit` again. (Extracted code is staged from the previous run.)
    ```console
    uv run pre-commit
    ```

### Use `pre_commit_vba.py` directly

#### Extract code

```console
uv run pre_commit_vba.py extract
```

#### Check branch name against version

```console
uv run pre_commit_vba.py check
```
