---
icon: lucide/rocket
---
# リリース

## `main`ブランチをリリース

1. リモートリポジトリで操作する. codeビューで, 右の`release`をクリック.
    ![releaseOperation](img/releaseOperation.drawio.svg)  
2. `Create a new release`のボタンをクリック.  
    ![createNewRelease](img/createNewRelease.drawio.svg){width="600"}

    !!! note "既にリリースしたものがある場合"
         `Draft a new release`のボタンをクリック.  
         ![draftNewRelease](img/draftNewRelease.drawio.svg){width="700"}

3. 'Select tag`をクリック.  
    ![selectTag](img/selectTag.drawio.svg){width="380"}
4. インプットボックスに`v0.1.0`と入力し, `Create new tag`をクリック.  
    ![createNewTag](img/createNewTag.drawio.svg){width="300"}
5. Release titleに`v0.1.0`と入力し, Release notesを記入し, `Publish release`をクリックする.  
    ![releaseNotes](img/releaseNotes.drawio.svg){width="450"}
6. `Publish release`をクリックする.  
    ![confirmToPublish](img/confirmToPublish.drawio.svg){width="270"}

## 次の開発への移行

次の開発サイクルに入るため, `main`ブランチを`develop`ブランチにマージする.

1. baseを`develop`, compareを`main`としたプルリクエストを作成し, プルリクエストをマージする.

2. マージ後, リモートの`main`ブランチと`develop`ブランチをローカルのものと同期する.

!!! note  "`develop`<-`main`のコンフリクトの解消"
    `main`ブランチ, `develop`ブランチともプルリクエストを経由しないと変更できない保護設定をしている場合, コンフリクトを解消するには, 次のように対処する.

    1. 現在のリモートの`develop`ブランチとローカルの`develop`ブランチをローカルで同期させる。
        ```
        git switch develop
        git pull origin develop
        ```
    2. ローカルの`develop`ブランチでコンフリクトを解消する.
    3. 例えば`chore/resolve-pr82-conflict-develop-sync`のような名前のブランチを作成.  
    ```
    git switch -c chore/resolve-pr82-conflict-develop-sync
    ```
    4. リモートにプッシュする.
    5. baseを`develop` compareを`chore/resolve-pr82-conflict-develop-sync`としたプルリクエストを作成し, プルリクエストをマージする.
