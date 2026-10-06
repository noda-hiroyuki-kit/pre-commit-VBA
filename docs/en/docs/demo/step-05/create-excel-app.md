---
icon: lucide/sheet
---
# Build an Excel App { #build-an-excel-app }

## Objective { #objective }

Manage Excel workbook changes with Git.  
Confirm the execution flow of `pre-commit-vba`.

## Step 1: Create a Branch { #step-1-create-a-branch }

```console
git switch develop
git pull
git switch -c feature/create-app
```

## Step 2: Write Code in Excel { #step-2-write-code-in-excel }

1. Open `example-app.xlsm`.
2. Add procedures in the VBE.
3. Save the workbook.

## Step 3: Run `prek` { #step-3-run-prek }

```console
git add .
prek
```

On the first run, the hook extracts the code and exits with an error because the extracted files have changed. Stage the extracted code, then run the hook again.

```console
git add .
prek
```

## Step 4: Commit and Push { #step-4-commit-and-push }

```powershell
git commit -m "feat: add workbook macro"
git push origin feature/create-app
```

## Step 5: Create and Merge a PR { #step-5-create-and-merge-a-pr }

Create a PR on GitHub.  
Set base to `develop` and merge it.

## Checkpoints { #checkpoints }

- Extracted VBA files are updated.
- `prek` finally passes.
- Changes are included in `develop`.
