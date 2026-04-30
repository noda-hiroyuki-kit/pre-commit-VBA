# 使用方法

## pre-commitで, pre-commit-hookとして使用

1. 対象のマクロブックを`git`でステージングする.
    ```
    git add .
    ```
2. uvで`pre-commit`を動作させる.
    ```
    uv run pre-commit
    ```
3. コードが展開されるので, コードをステージングし`git`で管理する.
    ```
    git add .
    ```

## `pre_commit_vba.py`をコマンドで走らせて使用

### ブックにあるコードを抽出する場合

vba_root_folderにて, 以下のコマンドを実行.
```console
uv run pre_commit_vba.py extract
```

### releaseブランチ名とワークブックのバージョン情報を比較チェックする場合

vba_root_folderにて, 以下のコマンドを実行.
```PowerShell
uv run pre_commit_vba.py check
```
