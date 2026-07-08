---
icon: lucide/book-open
---

# リファレンス

このページは, 内部処理を整理したリファレンスです.

## CLI概要

CLIは, [`typer`](https://typer.tiangolo.com/) で実装しています. 次の 2 コマンドを提供します.

- `extract`
- `check`

## コマンド: extract

### 実行例

```console
uv run pre_commit_vba.py extract
```

### 処理

1. 実行前のステージング状態を取得します.
2. `*.xls*` を走査します. 以下を除外しています.
    - `~$` で始まる一時ファイル
    - VBAを含まないブック (zip内に `xl/vbaProject.bin` がない)
3. ブックごとに保管フォルダを再作成します. (既にある場合は削除する.)
4. Excel COM で VBA モジュールを抽出します.
5. Custom UI XML (`customUI/customUI14.xml`, `customUI/customUI.xml`) を抽出します.
6. 抽出したファイルを cp932 -> UTF-8 へ変換し, 行末を `LF` に統一します.
7. フォームモジュールの先頭部メタデータの行末空白を除去します.
8. 生成物を `git add` します.
9. 実行前のステージング状態を比較します.
    - 状態が変化していたらエラー終了します.

## コマンド: check

### 実行例

```console
uv run pre_commit_vba.py check
```

### 判定内容

1. 現在ブランチ名を取得します.
2. ブランチ名が `release/v...` または `hotfix/v...` 以外ならログを出して正常終了します.
3. セマンティックバージョンを抽出できない場合はエラー終了します.
4. 対象ブックごとに以下を検査します.
    - Excel BuiltinDocumentProperties("Document version") とブランチ名 (`v{semver}`) の一致
    - Rubberduck Addin 参照設定がないか.
5. 不一致または参照検出時はエラー終了します.
6. 対象ブックが存在しない場合は警告ログで正常終了します.

## 主要クラス

- Constants: VBE の component type 定数を保持
- SettingsCommonFolder: ブックごとの抽出先フォルダ名を決定
- SettingsFoldersHandleExcel: export/customUI/code の各フォルダパスを管理
- SettingsOptionsHandleExcel: extract 時のオプションフラグを保持
- ExcelVbaExporter: COM経由で VBA コンポーネントを export
- ExcelCustomUiExtractor: zipから customUI XML を抽出
- Utf8Converter: cp932 -> UTF-8 変換, 行末統一, フォルダ注釈反映
- ITrailingWhiteSpaceRemover 系: メタデータ部分の trailing white space 処理

## 例外と終了コード

- StagingStatusError: `git write-tree` 失敗時
- AddToStagingError: `git add` 失敗時
- NotReleaseBranchError: check 対象外ブランチ
- InvalidSemVerError: ブランチ名から semver 抽出不可
- UndefineTypeError: 未定義 VBE コンポーネント種別

CLIとしての終了コードは概ね以下のとおりです.

- 0: 正常終了 (対象なし, 対象外ブランチ含む)
- 1: 検証失敗, 外部コマンド失敗, 想定エラー発生
