---
icon: lucide/rocket
---
# リリース

## 目的

`main` の内容を GitHub Release として公開します.

## 手順 1: Release 画面を開く

1. リポジトリの `Releases` を開きます.
2. `Create a new release` をクリックします.

??? info "操作画面"
    ![releaseOperation](../../../img/demo/step-07/releaseOperation.drawio.svg)
    ![createNewRelease](../../../img/demo/step-07/createNewRelease.drawio.svg){width="600"}

??? info "既にリリースしたものがある場合"
    `Draft a new release`のボタンをクリック.  
    ![draftNewRelease](../../../img/demo/step-07/draftNewRelease.drawio.svg){width="700"}

## 手順 2: タグを作成

1. `Select tag` をクリックします.
2. `v0.1.0` を入力します.
3. `Click new tag`をクリックします.

??? info "操作画面"
    ![selectTag](../../../img/demo/step-07/selectTag.drawio.svg){width="380"}  
    ![createNewTag](../../../img/demo/step-07/createNewTag.drawio.svg){width="300"}

## 手順 3: リリース情報を入力

1. Release title に `v0.1.0` を入れます.
2. Release notes を入力します.
3. `Publish release` をクリックします.
4. `Publish release` をクリックします.


??? info "操作画面"
    ![releaseNotes](../../../img/demo/step-07/releaseNotes.drawio.svg){width="450"}  
    ![confirmToPublish](../../../img/demo/step-07/confirmToPublish.drawio.svg){width="270"}

## 手順 4: 次の開発へ戻す

`main` から `develop` へ PR を作ります.  
マージ後にローカルを同期します.

```powershell
git checkout develop
git pull
```

!!! note "`develop` <- `main` で競合した場合"
    1. `develop` を最新化します.
    2. ローカルで競合を解消します.
    3. 解消用ブランチを作成します.
    4. ブランチをプッシュします.
    5. `develop` 向け PR を作ってマージします.

## 確認ポイント

- Release 一覧に `v0.1.0` が表示される.
- `develop` に `main` の内容が戻る.
