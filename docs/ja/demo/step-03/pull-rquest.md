---
icon: lucide/git-pull-request
---
# `feature/setup-repository`ブランチを`develop`ブランチにマージ

## ブラウザでの操作

1. メニューの`Pull requests`をクリック. 右端の`New pull request`をクリック.  
    ![New-pull-request](img/new-pull-request.drawio.svg)

2. Baseを`develop`ブランチに変更, compareを`feature/setup-repository`ブランチに変更し, `Create pull request`をクリック.  
    ![comparing-changes](img/comparing-changes.drawio.svg)

3. title, descriptionを以下の様に入力し, `Create pull request`をクリックする.  
    ```markdown title="title"
    feat: set up repository initial files
    ```
    ```markdown title="description"
    ## Summary

    Set up the initial repository structure with the following files:

    - README.md: project description with link to pre-commit-vba
    - .gitignore: ignore rules
    - .github/ISSUE_TEMPLATE/feature_request.md: feature request template (JP/EN)
    - .github/ISSUE_TEMPLATE/bug_report.md: bug report template (JP/EN)
    ```
    ![open a pull request](img/open-a-pull-request.drawio.svg)

4. ここで本来はpull requestに対してレビューを実施する. 本手順では省略し, `Merge pull request`をクリック.  
    ![merge pull request](img/merge-pull-request.drawio.svg)

5. `Confirm merge`をクリックする.
    ![confirm merge](img/confirm-merge.drawio.svg)

6. merge後は, リモート リポジトリにある `feature/setup-repository`ブランチは不要なので, `Delete branch`をクリックし, ブランチを削除する.  
    ![delete-branch](img/delete-branch.drawio.svg)

## ローカル ブランチの操作

1. 以下のコマンドで, 現在`feature/setup-repository`ブランチにいることを確認
    ```powershell
    git status
    ```

    コマンド実行結果  
    ```powershell hl_lines="2"
    PS %current directory%> git status
    On branch feature/setup-repository

    nothing to commit, working tree clean
    ```

2. 以下のコマンドを実行し, `develop`ブランチに移動.
    ```powershell
    git checkout develop
    ```

3. 以下のコマンドを実行し, リモート リポジトリとローカル リポジトリを同期させる.  
    ```powershell
    git pull
    ```

4. ローカル リポジトリのブランチを確認する.
    ```powershell
    git branch
    ```  
    実行結果
    ```powershell
    PS %current directory%> git branch
    * develop
    feature/setup-repository
    main
    ```

5. 不要な`feature/setup-repository`ブランチを削除する.
    ```powershell
    git branch -D feature/setup-repository
    ```

6. ローカル リポジトリの`feature/setup-repository`ブランチが削除できているか確認する.
    ```powershell
    git branch
    ```  
    実行結果
    ```powershell
    PS %current directory%> git branch
    * develop
    main
    ```
