---
icon: lucide/sheet
---
# リリースの準備

この手順は `v0.1.0` を例に説明します.

## 目的

`release` ブランチで公開前チェックを行います.

## 手順 1: リリースブランチを作る

```console
git switch develop
git pull
git switch -c release/v0.1.0
```

## 手順 2: ブック情報を更新

1. VBE で Document Version を `v0.1.0` にします.

    VBEのイミディエイトで以下を実行します.
        ```
        ThisWorkbook.BuiltinDocumentProperties("Document version")="v0.1.0"
        ```

2. 不要な参照設定を外します.

    ??? info "参照設定"
        ![VBE](img/VBE.drawio.svg){width="650"}

3. ブックを保存します.

## 手順 3: コミットしてプッシュ

```powershell
git add .
git commit -m "chore: prepare release v0.1.0"
git push -u origin release/v0.1.0
```

<!-- termynal -->
```
$ git commit -m "chore: prepare release v0.1.0"
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

## 手順 4: 変更履歴を更新

`CHANGELOG.md` を更新してコミットします.  
必要なら追加でプッシュします.

??? info "変更履歴を記録するのサイト"
    [https://keepachangelog.com/ja/1.1.0/](https://keepachangelog.com/ja/1.1.0/)

## 手順 5: `main` 向け PR を作る

base は `main`, compare は `release/v0.1.0` を選びます.  
PR を作成してマージします.

??? info "作成したPRの画面"
    ![pullRequestMergeToMain](../../../img/demo/step-06/pullRequestMergeToMain.drawio.svg){width="600"}

## 確認ポイント

- `main` にリリース準備の変更が入る.
- ブランチ名と Document Version が一致する.
