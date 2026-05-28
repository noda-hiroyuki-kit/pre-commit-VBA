# Excelのアプリを構築する.
1. `develop`ブランチにおり, リモート リポジトリと同期できているかを確認する.
    ```powershell
    git status
    ```
    ```powershell hl_lines="2 3"
    PS %current directory%> git status
    On branch develop
    Your branch is up to date with 'origin/develop'.

    nothing to commit, working tree clean
    ```

1. `feature/create-app`ブランチを作成する.  
    ```powershell
     git branch feature/create-app
    ```

3. `feature/create-app`ブランチへ移動する.
    ```powershell
    git checkout feature/create-app
    ```

## EXCELのアプリを構築(`feature/*`ブランチでの`pre-commit-vba`の利用)

1. EXCELのVBEでマクロを含むコードを記述し, ブックを保存.  
    デモリポジトリの場合は, ブック名は, `example-app.xlsm`である.

2. ブックをステージングする.
    ```powershell
    git add .
    ```

3. `uv run pre-commit-vba`を実行し, コードを抽出する.
    ```powershell
    uv run pre-commit
    ```
    ```powershell
    PS %current directory%>uv run pre-commit
    Extract VBA code from Excel files........................................Failed
    - hook id: extract-vba-code
    - exit code: 1

    INFO:pre_commit_vba.pre_commit_vba:customUI14.xml does not exists in example-app.xlsm
    INFO:pre_commit_vba.pre_commit_vba:customUI.xml does not exists in example-app.xlsm
    ERROR:pre_commit_vba.pre_commit_vba:Staging state changed during extract command. Review staged changes
    with 'git diff --cached', re-stage any updated files if needed, and then re-run the command.

    Check Excel book version.................................................Passed
    cspell...............................................(no files to check)Skipped
    trim trailing whitespace.............................(no files to check)Skipped
    fix end of files.....................................(no files to check)Skipped
    check toml...........................................(no files to check)Skipped
    check xml............................................(no files to check)Skipped
    detect destroyed symlinks................................................Passed
    check json...........................................(no files to check)Skipped
    mixed line ending....................................(no files to check)Skipped
    yamllint.............................................(no files to check)Skipped
    ```

    !!!pre-commit-vbaの動作  
        `pre-commit-vba`を実行するとブックの中のコードが抽出されて、ステージングされる.  
         `pre-commit-vba`の開始時にはコードがステージングされていないため, `pre-commit-vba`のチェックがコードに適用されていない.  
        2回目の`pre-commit`動作で, コードへのチェックが実施される.

4. `uv run pre-commit-vba`を実行し, コードをチェックする.

    ```powershell
    uv run pre-commit
    ```
    ```powershell
    PS %current directory%>uv run pre-commit
    Extract VBA code from Excel files........................................Passed
    Check Excel book version.................................................Passed
    cspell...................................................................Passed
    trim trailing whitespace.................................................Passed
    fix end of files.........................................................Passed
    check toml...........................................(no files to check)Skipped
    check xml............................................(no files to check)Skipped
    detect destroyed symlinks................................................Passed
    check json...........................................(no files to check)Skipped
    mixed line ending........................................................Passed
    yamllint.............................................(no files to check)Skipped
    ```
    !!!よくあるエラーへの対応
        エラーが出ている場合は以下を参考にコードを修正し、ブックを保存して, ブックをステージングし, 再度 `uv run pre-commit` を実行する.

        - `cspell`
            - スペルミスの場合は, コードを修正する.
            - スペルがあっている場合は, `cspell.json`の"words"に追加する.
        - `trim trailing whitespace`
            - コードの改行部分に, VBEは前コードと同じインデントを自動で挿入する. そこのインデントを削除する.  
            - `example-app.xlsm`には, `TrailingWhitespaceModule`モジュールを用意している. `CleanAllModulesInWorkbook`プロシージャを実行するとブック内の全てのコードから抵触する末尾のスペースを削除する.

5. コミットする.

    ```powershell
    git commit -m "feat:何かの機能を追加"
    ```
    ```powershell
    PS %current directory%>git commit -m "feat:何かの機能を追加"
    Extract VBA code from Excel files........................................Passed
    Check Excel book version.................................................Passed
    cspell...................................................................Passed
    trim trailing whitespace.................................................Passed
    fix end of files.........................................................Passed
    check toml...........................................(no files to check)Skipped
    check xml............................................(no files to check)Skipped
    detect destroyed symlinks................................................Passed
    check json...........................................(no files to check)Skipped
    mixed line ending........................................................Passed
    yamllint.............................................(no files to check)Skipped
    ```

6. 開発が完了したら, プッシュする.
    ```powershell
    git push origin feature/create-app
    ```

7. `feature/create-app`を`develop`ブランチにマージするプルリクエストを作成する. このプルリクエストを通じて, `develop`ブランチにマージする.
