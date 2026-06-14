---
icon: lucide/sheet
---
# Excelブックのリリース準備

バージョン `v0.1.0`をリリースすることとして, 記述する.

## `release/v[セマンティック バージョニング]`ブランチでリリース準備

1. `develop`ブランチより, `release/v0.1.0`ブランチを作成し、切り替える.
    ```powershell
    git switch -c release/v0.1.0
    ```
2. ブックのバージョンを設定する.  
   VBEのイミディエイトウィンドウで,以下を実行する.
   ```
   ThisWorkbook.BuiltinDocumentProperties.Item("Document Version") = "v0.1.0"
   ```

    !!!ブックのバージョン  
        この操作により, ブックのファイルプロパティのバージョン番号にバージョンが設定される.  
        ![FileProperty](img/FileProperty.drawio.svg)

3. ブックのVisual Basic Editorの参照設定をリリース用に変更する.  
    Rubberduck AddInなどの標準でインストールされていないライブラリへの参照設定を外す.
    ![VBE](img/VBE.drawio.svg)

4. ブックを保存し, コミットする.
    ```powershell
    git commit -m "chore: prepare release v0.1.0"
    ```
    ```powershell
    PS %current directory%>git commit -m "chore: prepare release v0.1.0"
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

5. プッシュする.

6. `CHANGELOG.md`を作成している場合は, [変更履歴を記録する](https://keepachangelog.com/ja/1.1.0/)を参考に作成し, コミットして, プッシュする.

## プルリクエストを作成し、`main`ブランチにマージ

1.
