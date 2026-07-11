---
icon: lucide/folder-git-2
---
# リポジトリの基本ファイル作成

## 目的

ローカルリポジトリを作成します.  
`main` / `develop` / `feature` を準備します.

## 手順 1: クローンして移動

1. GitHub でリポジトリ URL をコピーします.  
    ![remote repository url](../../../img/demo/step-02/repository-first.drawio.svg){width="700"}
2. ターミナルで次を実行します.
    ```console
    git clone <コピーしたURL>
    cd pre-commit-vba-example
    ```

## 手順 2: `main` を準備

```console
git commit -m "first commit" --allow-empty
git branch -M main
git push -u origin main
```
??? tip
    `git status`を実行すると以下の様に表示され, `main`ブランチにいて, リモートブランチと同期できていることが確認できる.
    ```console
    PS %current working directory%> git status
    On branch main
    Your branch is up to date with 'origin/main'.

    nothing to commit, working tree clean
    ```

## 手順 3: `develop` を準備

```console
git switch -c develop
git push -u origin develop
```
??? tip
    `git status`を実行すると以下の様に表示され, `develop`ブランチにいて, リモートブランチと同期できていることが確認できる.
    ```console
    PS %current working directory%> git status
    On branch develop
    Your branch is up to date with 'origin/develop'.

    nothing to commit, working tree clean
    ```

## 手順 4: 作業ブランチを準備

```console
git switch -c feature/setup-repository
git push -u origin feature/setup-repository
```

## 手順 5: 基本ファイルを追加

1. `README.md` を作成します.

    ```markdown title="README.md"
    # pre-commit-vba-example

    This repository is a demo project for pre-commit-vba.
    ```

2. `.gitignore` を作成します.

    ```text title=".gitignore"
    ~$*
    ```

3. 次のテンプレートを配置します.
    - `.github/ISSUE_TEMPLATE/feature_request.md`  
    - `.github/ISSUE_TEMPLATE/bug_report.md`

    ??? info "本リポジトリの`.github/ISSUE_TEMPLATE/feature_request.md`"

        ```markdown title=".github/ISSUE_TEMPLATE/feature_request.md"
        --8<-- ".github/ISSUE_TEMPLATE/feature_request.md"
        ```

    ??? info "本リポジトリの`.github/ISSUE_TEMPLATE/bug_report.md`"
        ```markdown title=".github/ISSUE_TEMPLATE/bug_report.md"
        --8<-- ".github/ISSUE_TEMPLATE/bug_report.md"
        ```


4. コミットしてプッシュします.

    ```console
    git add .
    git commit -m "chore: add initial repository files"
    git push -u origin feature/setup-repository
    ```

## 確認ポイント

- `git status` が clean を示す.
- GitHub 上に 3 ブランチが存在する.
- `feature/setup-repository` に基本ファイルがある.
