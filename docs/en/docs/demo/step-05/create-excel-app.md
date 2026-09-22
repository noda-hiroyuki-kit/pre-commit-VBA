---
icon: lucide/sheet
---
# Build an Excel App

## Objective

Manage Excel workbook changes with Git.  
Confirm the execution flow of `pre-commit-vba`.

## Step 1: Create a Branch

```console
git switch develop
git pull
git switch -c feature/create-app
```

## Step 2: Write Code in Excel

1. Open `example-app.xlsm`.
2. Add procedures in the VBE.
3. Save the workbook.

## Step 3: Run `pre-commit`

```console
git add .
uv run pre-commit
```

On the first run, extraction happens, so it exits with an error.  
Therefore, run it again.

```console
uv run pre-commit
```

## Step 4: Commit and Push

```powershell
git commit -m "feat: add workbook macro"
git push origin feature/create-app
```

## Step 5: Create and Merge a PR

Create a PR on GitHub.  
Set base to `develop` and merge it.

## Checkpoints

- Extracted VBA files are updated.
- `uv run pre-commit` finally passes.
- Changes are included in `develop`.
