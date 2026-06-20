---
icon: lucide/book-open
---

# reference

このページは, CLI仕様と内部処理を整理したリファレンスです.

## CLI概要

本スクリプトは Typer ベースのCLIで, 以下2コマンドを提供します.

- extract: ExcelブックからVBAコードとCustom UI XMLを抽出し, git staging に追加する
- check: ブランチ名とブックバージョン整合性, および Rubberduck Addin 参照を検査する

## コマンド: extract

### 実行例

```console
uv run pre_commit_vba.py extract
```

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| --target-path | . | 走査対象ディレクトリ |
| --folder-suffix | .VBA | 生成フォルダ名のサフィックス |
| --export-folder | export | COMエクスポート生ファイルの格納先 |
| --custom-ui-folder | customUI | customUI.xml / customUI14.xml の格納先 |
| --code-folder | code | UTF-8化後コードの格納先 |
| --enable-folder-annotation / --disable-folder-annotation | 有効 | `'@Folder("...")` 注釈をサブフォルダに反映 |
| --create-gitignore / --not-create-gitignore | 有効 | 共通フォルダに .gitignore を作成 |
| --include-extension / --exclude-extension | 有効 | 共通フォルダ名に元ブック拡張子を含めるか |
| --version | - | バージョン表示して終了 |

### 処理フロー

1. git write-tree で実行前の staging 状態を取得
2. `*.xls*` を走査し, 以下を除外
   - 一時ファイル (`~$` で始まるファイル)
   - VBAを含まないブック (zip内に `xl/vbaProject.bin` がない)
3. ブックごとに共通フォルダを再作成
4. Excel COM (`DispatchEx("Excel.Application")`) でVBAモジュールを export
5. zip から Custom UI XML (`customUI/customUI14.xml`, `customUI/customUI.xml`) を抽出
6. cp932 -> UTF-8 へ変換し, 行末を LF に統一
7. 必要に応じてメタデータ先頭部の trailing white space を除去
8. 生成物を `git add` で staging に追加
9. git write-tree で実行後の staging 状態を比較
10. 状態が変化していたらエラー終了

### 補足

- Frxモジュール判定は先頭が `VERSION 5` かどうかで分岐
- バイナリファイル判定は先頭チャンク内の NUL byte で実施
- `git add` / `git write-tree` は subprocess で実行し, 失敗時は専用例外を送出

## コマンド: check

### 実行例

```console
uv run pre_commit_vba.py check
```

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| --target-path | . | 走査対象ディレクトリ |
| --version | - | バージョン表示して終了 |

### 判定内容

1. 現在ブランチ名を取得 (`git rev-parse --abbrev-ref HEAD`)
2. ブランチ名が `release/v...` または `hotfix/v...` 以外なら情報ログを出して正常終了
3. セマンティックバージョンを抽出できない場合はエラー終了
4. 対象ブックごとに以下を検査
   - Rubberduck Addin 参照検出 (`xl/vbaProject.bin` 内の `rubberduck.x32.tlb` / `rubberduck.x64.tlb`)
   - Excel BuiltinDocumentProperties("Document version") とブランチ版 (`v{semver}`) の一致
5. 不一致または参照検出時はエラー終了
6. 対象ブックが存在しない場合は警告ログで正常終了

### Rubberduck 検出ロジック詳細

- `rubberduck.x32.tlb` または `rubberduck.x64.tlb` の存在を検出対象とする
- ただし, ソース文字列由来の誤検出を避けるため `rubberduck\\.x\\d+\\.tlb` リテラルを含む場合は無効扱い
- x32/x64 両方が同時に検出される場合は非アクティブ参照とみなし, エラーにしない

## 主要クラス

- Constants: VBE の component type 定数を保持
- SettingsCommonFolder: ブックごとの共通フォルダ名を決定
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

CLIとしての終了コードは概ね以下です.

- 0: 正常終了 (対象なし, 対象外ブランチ含む)
- 1: 検証失敗, 外部コマンド失敗, 想定エラー発生
