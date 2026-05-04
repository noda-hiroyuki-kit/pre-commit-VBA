# ローカル リポジトリでの操作

## ローカルリポジトリの作成

1. ローカル リポジトリのURLをクリップボードにコピーする.  
    ![remote repository url](img/repository-first.drawio.svg)

2. ローカルリポジトリを作成するフォルダで`git clone %コピーしたリポジトリURLを貼付%`を実行する.

3. 下のコマンドを実行し, リポジトリのフォルダに移動.  
    ```powershell
    cd pre-commit-vba-example
    ```

## `main`ブランチを作成

1. 下のコマンドを実行し, 初めのコミットを行う.
```powershell
git commit -m "first commit" --allow-empty

```

2. 下のコマンドで, ブランチ名を`main`に変更する.
```powershell
git branch -M main
```

6. 下のコマンドで, リモートリポジトリにプッシュ.
```powershell
git push -u origin main
```

!!!Note
    `git status`を実行すると以下の様に表示され, `main`ブランチにいて, リモートブランチと同期できていることが確認できる.
    ```powershell
    PS %current working directory%> git status
    On branch main
    Your branch is up to date with 'origin/main'.

    nothing to commit, working tree clean
    ```

## `develop`ブランチを作成

7. 下のコマンドで, `develop`ブランチを作成.
```powershell
git branch develop
```

8. 下のコマンドで, `develop`ブランチへ移動.
```powershell
git checkout develop
```

9. 下のコマンドで, リモートリポジトリにプッシュ.
```powershell
git push -u origin develop
```

!!!Note
    `git status`を実行すると以下の様に表示され, `develop`ブランチにいて, リモートブランチと同期できていることが確認できる.
    ```powershell
    PS %current working directory%> git status
    On branch develop
    Your branch is up to date with 'origin/develop'.

    nothing to commit, working tree clean
    ```


## `feature/setup-repository`ブランチを作成


1. 下のコマンドで, `feature/setup-repository`ブランチを作成.
```powershell
git branch feature/setup-repository
```

2. 下のコマンドで, `feature/setup-repository`ブランチへ移動.
```powershell
git checkout feature/setup-repository
```

3. 下のコマンドで, リモートリポジトリにプッシュ.
```powershell
git push -u origin feature/setup-repository
```

## `feature/setup-repository`ブランチにリポジトリの基本ファイルを作成

1. `README.md`を作成し, コミットする.
    ```markdown title="README.md"
    # pre-commit-vba-example

    This repository is a demo for how to use [`pre-commit-vba`](https://github.com/noda-hiroyuki-kit/pre-commit-VBA).
    ```
    ```powershell
    git add .
    git commit -m "docs: add README with project description"
    ```

2. `.gitignore`を作成し, コミットする.

    ``` title=".gitignore"
    ~$*
    ```
    ```powershell
    git add .
    git commit -m "chore: add .gitignore"
    ```
    excelのワークブックを開くと, `~$`で始まるロックファイルが生成される.  
    ワークブックを開いたままコミットなどを容易にするため, ロックファイルを無視する設定を追加する.

3. `.github/ISSUE_TEMPLATE/feature_request.md`を作成し, コミットする.
    ```markdown title=".github/ISSUE_TEMPLATE/feature_request.md"
    --8<-- ".github/ISSUE_TEMPLATE/feature_request.md"
    ```
    ```powershell
    git add .
    git commit -m "chore: add GitHub issue template for feature requests"
    ```

4. `.github/ISSUE_TEMPLATE/bug_report.md`を作成し, コミットする.
    ```markdown title=".github/ISSUE_TEMPLATE/bug_report.md"
    --8<-- ".github/ISSUE_TEMPLATE/bug_report.md"
    ```
    ```powershell
    git add .
    git commit -m "chore: add GitHub issue template for bug reports"
    ```
5. 下のコマンドで, リモートリポジトリにプッシュ.
    ```powershell
    git push -u origin feature/setup-repository
    ```
