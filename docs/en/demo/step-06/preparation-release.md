---
icon: lucide/sheet
---
# Prepare for Release

This procedure uses `v0.1.0` as an example.

## Objective

Run pre-release checks on a `release` branch.

## Step 1: Create a Release Branch

```console
git switch develop
git pull
git switch -c release/v0.1.0
```

## Step 2: Update Workbook Information

1. In the VBE, set Document Version to `v0.1.0`.

    Run the following in the VBE Immediate window.
        ```
        ThisWorkbook.BuiltinDocumentProperties.Item("Document Version")="v0.1.0"
        ```

2. Remove unnecessary references.

    ??? info "References"
        ![VBE](img/VBE.drawio.svg){width="650"}

3. Save the workbook.

## Step 3: Commit and Push

```powershell
git add .
git commit -m "chore: prepare release v0.1.0"
git push -u origin release/v0.1.0
```

## Step 4: Update Changelog

Update `CHANGELOG.md` and commit it.  
Push additional commits if needed.

??? info "Site for writing changelogs"
    [https://keepachangelog.com/en/1.1.0/](https://keepachangelog.com/en/1.1.0/)

## Step 5: Create a PR to `main`

Select base as `main` and compare as `release/v0.1.0`.  
Create the PR and merge it.

??? info "Created PR screen"
    ![pullRequestMergeToMain](../../../img/demo/step-06/pullRequestMergeToMain.drawio.svg){width="600"}

## Checkpoints

- `main` contains release preparation changes.
- Branch name and Document Version match.
