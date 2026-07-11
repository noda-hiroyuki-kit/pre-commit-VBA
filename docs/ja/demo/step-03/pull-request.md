---
icon: lucide/git-pull-request
---
# 基本ファイルを `develop` にマージ

## 目的

`feature/setup-repository` の変更を `develop` に統合します.

## ブラウザでの手順

1. `Pull requests` を開きます.
2. `New pull request` をクリックします.

    ??? info "操作の画面"
        ![New-pull-request](img/new-pull-request.drawio.svg)

3. base を `develop` にします.
4. compare を `feature/setup-repository` にします.
5. `Create pull request` をクリックします.

    ??? info "操作の画面"
        ![comparing-changes](img/comparing-changes.drawio.svg)

6. PR タイトルと説明を入力します.
7. `Create pull request` をクリックします.

    ??? info "タイトルと説明の事例と操作画面"
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
        ![open a pull request](img/open-a-pull-request.drawio.svg)

8. 内容を確認して `Merge pull request` を押します.

    ??? info "操作の画面"
        ![merge pull request](img/merge-pull-request.drawio.svg){width="600"}

9. `Confirm merge` を押します.

    ??? info "操作の画面"
        ![confirm merge](img/confirm-merge.drawio.svg){width="600"}

10. `Delete branch` でリモートブランチを削除します.

    ??? info "操作の画面"
        ![delete-branch](img/delete-branch.drawio.svg){width="600"}


## ローカルでの手順

```console
git switch develop
git pull
git branch -D feature/setup-repository
```

## 確認ポイント

- `develop` に基本ファイルが入っている.
- `feature/setup-repository` がローカルに残っていない.
- `git status` が clean を示す.
