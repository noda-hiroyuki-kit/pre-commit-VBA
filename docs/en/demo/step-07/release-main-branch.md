---
icon: lucide/rocket
---
# Release

## Objective

Publish the content of `main` as a GitHub Release.

## Step 1: Open the Release Page

1. Open `Releases` in the repository.
2. Click `Create a new release`.

??? info "Operation screen"
    ![releaseOperation](../../../img/demo/step-07/releaseOperation.drawio.svg)
    ![createNewRelease](../../../img/demo/step-07/createNewRelease.drawio.svg){width="600"}

??? info "If you already have released versions"
    Click the `Draft a new release` button.  
    ![draftNewRelease](../../../img/demo/step-07/draftNewRelease.drawio.svg){width="700"}

## Step 2: Create a Tag

1. Click `Select tag`.
2. Enter `v0.1.0`.
3. Click `Create new tag`.

??? info "Operation screen"
    ![selectTag](../../../img/demo/step-07/selectTag.drawio.svg){width="380"}  
    ![createNewTag](../../../img/demo/step-07/createNewTag.drawio.svg){width="300"}

## Step 3: Enter Release Information

1. Enter `v0.1.0` in Release title.
2. Enter release notes.
3. Click `Publish release`.
4. Click `Publish release`.


??? info "Operation screen"
    ![releaseNotes](../../../img/demo/step-07/releaseNotes.drawio.svg){width="450"}  
    ![confirmToPublish](../../../img/demo/step-07/confirmToPublish.drawio.svg){width="270"}

## Step 4: Return to Next Development

Create a PR from `main` to `develop`.  
After merge, sync your local repository.

```powershell
git checkout develop
git pull
```

!!! note "If conflicts occur when merging `develop` <- `main`"
    1. Update `develop` to the latest state.
    2. Resolve conflicts locally.
    3. Create a branch for conflict resolution.
    4. Push the branch.
    5. Create a PR to `develop` and merge it.

## Checkpoints

- `v0.1.0` appears in the Releases list.
- The content from `main` is returned to `develop`.
