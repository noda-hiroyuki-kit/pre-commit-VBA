---
icon: lucide/sliders-horizontal
---
# Options Guide

This page explains the options for `pre-commit-vba`.  
If you only want to see the specification list, refer to [Reference](reference.md).

## Commands

- `extract`: Extracts VBA code.
- `check`: Compares the branch name and the workbook version.

## Default Values

### extract

| Option | Default |
|---|---|
| --target-path | . |
| --folder-suffix | .VBA |
| --export-folder | export |
| --custom-ui-folder | customUI |
| --code-folder | code |
| --enable-folder-annotation / --disable-folder-annotation | Enabled |
| --create-gitignore / --not-create-gitignore | Enabled |
| --include-extension / --exclude-extension | Enabled |

### check

| Option | Default |
|---|---|
| --target-path | . |

## `extract` Options

### --target-path

- What it does: Specifies the folder to search for Excel workbooks.
- When to use it: When workbooks are stored outside the repository root (for example, test workbooks).
- Default: `.`

```console
uv run pre_commit_vba.py extract --target-path ./tests
```

### --folder-suffix

- What it does: Changes the suffix of the generated shared folder name.
- When to use it: When you want to standardize output folder names based on team conventions.
- Default: `.VBA`

```console
uv run pre_commit_vba.py extract --folder-suffix src
```

### --export-folder

- What it does: Changes the destination name for exported raw files.
- When to use it: When you want to manage raw file outputs in a differently named folder.
- Default: `export`

```console
uv run pre_commit_vba.py extract --export-folder raw-export
```

### --custom-ui-folder

- What it does: Changes the destination folder name for `customUI.xml` / `customUI14.xml`.
- When to use it: When you want to manage ribbon UI definitions in a differently named folder.
- Default: `customUI`

```console
uv run pre_commit_vba.py extract --custom-ui-folder ribbon
```

### --code-folder

- What it does: Changes the destination folder name for final code managed in Git.
- When to use it: When you want to align code placement with an existing project structure.
- Default: `code`

```console
uv run pre_commit_vba.py extract --code-folder src-vba
```

### --enable-folder-annotation / --disable-folder-annotation

- What it does: Toggles whether the `@Folder("...")` annotation in VBA is reflected in the subfolder structure.
- When to use it:
    - Enable: When you want to reproduce the Rubberduck folder structure as-is.
    - Disable: When you want to flatten all code into a single folder.
- Default: `--enable-folder-annotation` (enabled)

```console
uv run pre_commit_vba.py extract --disable-folder-annotation
```

### --create-gitignore / --not-create-gitignore

- What it does: Toggles whether to create `.gitignore` directly under the shared folder.
- When to use it:
    - Create: When you do not want to track exported raw files in Git.
    - Do not create: When you need to follow an existing `.gitignore` policy (not recommended).
    !!! Note
        On GitHub, text is managed as UTF-8.  
        If your code includes characters such as Kanji, text corruption can occur.
- Default: `--create-gitignore` (create)

```console
uv run pre_commit_vba.py extract --not-create-gitignore
```

### --include-extension / --exclude-extension

- What it does: Toggles whether to include the original workbook extension in the output folder name.
- When to use it:
    - Include: When multiple workbooks in the target folder differ only by extension, such as `app.xlsm` and `app.xlam`.
    - Exclude: When there are no same-name workbooks with different extensions in the target folder.
- Default: `--include-extension` (include)

```console
uv run pre_commit_vba.py extract --exclude-extension
```

### --version

- What it does: Displays only the version and exits.
- When to use it: When you only need to check the runtime version in CI or during investigation.
- Default: Not specified (normal execution)

```console
uv run pre_commit_vba.py extract --version
```

## `check` Options

### --target-path

- What it does: Specifies the directory to search for Excel workbooks to check.
- When to use it: When release-target workbooks are in a subfolder.
- Default: `.`

```console
uv run pre_commit_vba.py check --target-path ./release-books
```

### --version

- What it does: Displays only the version and exits.
- When to use it: During diagnostics of the hook environment.
- Default: Not specified (normal execution)

```console
uv run pre_commit_vba.py check --version
```

## Common Usage Patterns

### 1. Standard operation

```console
uv run pre_commit_vba.py extract
uv run pre_commit_vba.py check
```

### 2. Use a simple single-folder output structure

```console
uv run pre_commit_vba.py extract --disable-folder-annotation --exclude-extension
```

### 3. Match naming in an existing repository

```console
uv run pre_commit_vba.py extract --folder-suffix .vba --code-folder source
```

## Notes

- `extract` checks changes in staging state before and after execution. On the first run, staging changes because code is extracted, so it results in an error.
- `check` is valid only on `release/v...` or `hotfix/v...` branches.
- Temporary files starting with `~$` are excluded from processing.
