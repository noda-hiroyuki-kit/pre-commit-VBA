---
icon: lucide/folder-git-2
---
# Create Basic Repository Files

## Objective

Create a local repository.  
Prepare `main` / `develop` / `feature` branches.

## Step 1: Clone and Move

1. Copy the repository URL on GitHub.  
    ![remote repository url](../../../img/demo/step-02/repository-first.drawio.svg){width="700"}
2. Run the following in a terminal.
    ```console
    git clone <copied-URL>
    cd pre-commit-vba-example
    ```

## Step 2: Prepare `main`

```console
git commit -m "first commit" --allow-empty
git branch -M main
git push -u origin main
```
??? tip
    Running `git status` should show the following, which confirms that you are on the `main` branch and synced with the remote branch.
    ```console
    PS %current working directory%> git status
    On branch main
    Your branch is up to date with 'origin/main'.

    nothing to commit, working tree clean
    ```

## Step 3: Prepare `develop`

```console
git switch -c develop
git push -u origin develop
```
??? tip
    Running `git status` should show the following, which confirms that you are on the `develop` branch and synced with the remote branch.
    ```console
    PS %current working directory%> git status
    On branch develop
    Your branch is up to date with 'origin/develop'.

    nothing to commit, working tree clean
    ```

## Step 4: Prepare a Working Branch

```console
git switch -c feature/setup-repository
git push -u origin feature/setup-repository
```

## Step 5: Add Basic Files

1. Create `README.md`.

    ```markdown title="README.md"
    # pre-commit-vba-example

    This repository is a demo project for pre-commit-vba.
    ```

2. Create `.gitignore`.

    ```text title=".gitignore"
    ~$*
    ```

3. Place the following templates.
    - `.github/ISSUE_TEMPLATE/feature_request.md`  
    - `.github/ISSUE_TEMPLATE/bug_report.md`

    ??? info "`.github/ISSUE_TEMPLATE/feature_request.md` in this repository"

        ```markdown title=".github/ISSUE_TEMPLATE/feature_request.md"
        --8<-- ".github/ISSUE_TEMPLATE/feature_request.md"
        ```

    ??? info "`.github/ISSUE_TEMPLATE/bug_report.md` in this repository"
        ```markdown title=".github/ISSUE_TEMPLATE/bug_report.md"
        --8<-- ".github/ISSUE_TEMPLATE/bug_report.md"
        ```


4. Commit and push.

    ```console
    git add .
    git commit -m "chore: add initial repository files"
    git push -u origin feature/setup-repository
    ```

## Checkpoints

- `git status` shows a clean working tree.
- Three branches exist on GitHub.
- Basic files are present in `feature/setup-repository`.
