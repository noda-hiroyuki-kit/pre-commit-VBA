---
icon: lucide/book-open
---

# Reference

This page is a reference that organizes the internal processing.

## CLI Overview

The CLI is implemented with [`typer`](https://typer.tiangolo.com/). It provides the following two commands.

- `extract`
- `check`

## Command: extract

### Example

```console
uv run pre_commit_vba.py extract
```

### Processing

1. Get the staging state before execution.
2. Scan supported Office files. The following are excluded.
    - Temporary files that start with `~$`
    - Office files that do not contain VBA
3. Recreate the storage folder for each Office file. (Delete it first if it already exists.)
4. Extract VBA modules via the corresponding Office COM application.
5. Extract Custom UI XML (`customUI/customUI14.xml`, `customUI/customUI.xml`).
6. Convert extracted files from cp932 to UTF-8 and normalize line endings to `LF`.
7. Remove trailing whitespace in metadata header lines of form modules.
8. Run `git add` on generated files.
9. Compare with the staging state from before execution.
    - If the state changed, exit with an error.

## Command: check

### Example

```console
uv run pre_commit_vba.py check
```

### What is validated

1. Get the current branch name.
2. If the branch name is not `release/v...` or `hotfix/v...`, output a log and exit successfully.
3. If a semantic version cannot be extracted, exit with an error.
4. For each target office files, validate the following.
    - Whether BuiltinDocumentProperties("Document version") matches the branch name (`v{semver}`)
    - Whether a Rubberduck Addin reference exists
5. If a mismatch or reference detection occurs, exit with an error.
6. If no target file exists, output a warning log and exit successfully.

## Main Classes

- Constants: Holds VBE component type constants
- SettingsCommonFolder: Determines the extraction destination folder name per file
- SettingsFoldersHandleOffice: Manages folder paths for export/customUI/code
- SettingsOptionsHandleOffice: Holds option flags used by `extract`
- ExcelVbaExporter: Exports VBA components via COM
- WordVbaExporter: Exports VBA components via COM
- PowerPointVbaExporter: Exports VBA components via COM
- CustomUiExtractor: Extracts customUI XML from zip
- Utf8Converter: Handles cp932 to UTF-8 conversion, line-ending normalization, and folder-annotation reflection
- ITrailingWhiteSpaceRemover family: Handles trailing whitespace in metadata sections

## Exceptions and Exit Codes

- StagingStatusError: When `git write-tree` fails
- AddToStagingError: When `git add` fails
- NotReleaseBranchError: Branch is out of scope for `check`
- InvalidSemVerError: Cannot extract semver from branch name
- UndefineTypeError: Undefined VBE component type

CLI exit codes are generally as follows.

- 0: Success (including no targets and out-of-scope branches)
- 1: Validation failure, external command failure, or expected error occurred
