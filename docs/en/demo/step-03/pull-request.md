---
icon: lucide/git-pull-request
---
# Merge Basic Files into `develop`

## Objective

Integrate the changes from `feature/setup-repository` into `develop`.

## Steps in Browser

1. Open `Pull requests`.
2. Click `New pull request`.

    ??? info "Operation screen"
        ![New-pull-request](../../../img/demo/step-03/new-pull-request.drawio.svg)

3. Set base to `develop`.
4. Set compare to `feature/setup-repository`.
5. Click `Create pull request`.

    ??? info "Operation screen"
        ![comparing-changes](../../../img/demo/step-03/comparing-changes.drawio.svg)

6. Enter the PR title and description.
7. Click `Create pull request`.

    ??? info "Example title/description and operation screen"
        ```text title="Title"
        chore: add initial repository files
        ```
        ```markdown title="description"
        ## Summary

        Set up the initial repository structure with the following files:

        - README.md: project description with link to pre-commit-vba
        - .gitignore: ignore rules
        - .github/ISSUE_TEMPLATE/feature_request.md: feature request template
        - .github/ISSUE_TEMPLATE/bug_report.md: bug report template
        ```
        ![open a pull request](../../../img/demo/step-03/open-a-pull-request.drawio.svg)

7. Review the content and click `Merge pull request`.

    ??? info "Operation screen"
        ![merge pull request](../../../img/demo/step-03/merge-pull-request.drawio.svg){width="600"}

8. Click `Confirm merge`.

    ??? info "Operation screen"
        ![confirm merge](../../../img/demo/step-03/confirm-merge.drawio.svg){width="600"}

9. Use `Delete branch` to remove the remote branch.

    ??? info "Operation screen"
        ![delete-branch](../../../img/demo/step-03/delete-branch.drawio.svg){width="600"}


## Local Steps

```console
git switch develop
git pull
git branch -D feature/setup-repository
```

## Checkpoints

- Basic files are included in `develop`.
- `feature/setup-repository` no longer remains locally.
- `git status` shows a clean working tree.
