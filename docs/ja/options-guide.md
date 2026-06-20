---
icon: lucide/sliders-horizontal
---

# オプションガイド

このページは, pre_commit_vba.py のオプションを利用者視点で説明するガイドです.  
仕様一覧だけを見たい場合は [リファレンス](reference.md) を参照してください.

## まず押さえる使い分け

- extract: VBAコードを取り出して, Gitで管理しやすい形にするコマンド
- check: リリース前に「ブランチ名」と「Excelブックのバージョン」が一致しているかを確認するコマンド

## 規定値の一覧

### extract

| オプション | 規定値 |
|---|---|
| --target-path | . |
| --folder-suffix | .VBA |
| --export-folder | export |
| --custom-ui-folder | customUI |
| --code-folder | code |
| --enable-folder-annotation / --disable-folder-annotation | 有効 |
| --create-gitignore / --not-create-gitignore | 有効 |
| --include-extension / --exclude-extension | 有効 |

### check

| オプション | 規定値 |
|---|---|
| --target-path | . |

## extract オプション

### --target-path

- 何をする: Excelブックを探索する開始ディレクトリを指定します.
- いつ使う: リポジトリのルート以外にブックを置いているとき.
- 規定値: .

```console
uv run pre_commit_vba.py extract --target-path ./excel
```

### --folder-suffix

- 何をする: 生成される共通フォルダ名の末尾を変更します.
- いつ使う: チーム規約で出力フォルダ名を統一したいとき.
- 規定値: .VBA

```console
uv run pre_commit_vba.py extract --folder-suffix .src
```

### --export-folder

- 何をする: COMエクスポートされた生ファイルの格納先名を変更します.
- いつ使う: 中間成果物の保存先を明示的に分けたいとき.
- 規定値: export

```console
uv run pre_commit_vba.py extract --export-folder raw-export
```

### --custom-ui-folder

- 何をする: customUI.xml / customUI14.xml の格納先名を変更します.
- いつ使う: リボンUI定義を別名フォルダで管理したいとき.
- 規定値: customUI

```console
uv run pre_commit_vba.py extract --custom-ui-folder ribbon
```

### --code-folder

- 何をする: UTF-8に変換した最終コードの格納先名を変更します.
- いつ使う: 既存プロジェクトでコード配置先を合わせたいとき.
- 規定値: code

```console
uv run pre_commit_vba.py extract --code-folder src-vba
```

### --enable-folder-annotation / --disable-folder-annotation

- 何をする: VBA内の '@Folder("...") 注釈をサブフォルダ構造へ反映するかを切り替えます.
- いつ使う:
  - 有効化する: Rubberduckのフォルダ構成をそのまま再現したい.
  - 無効化する: すべてのコードを1フォルダに平坦化したい.
- 規定値: --enable-folder-annotation（有効）

```console
uv run pre_commit_vba.py extract --disable-folder-annotation
```

### --create-gitignore / --not-create-gitignore

- 何をする: 共通フォルダ直下に .gitignore を作るかどうかを切り替えます.
- いつ使う:
  - 作成する: 中間フォルダを誤って追跡しないようにしたい.
  - 作成しない: 既存の .gitignore 運用に合わせたい.
- 規定値: --create-gitignore（作成する）

```console
uv run pre_commit_vba.py extract --not-create-gitignore
```

### --include-extension / --exclude-extension

- 何をする: 出力フォルダ名に元ブックの拡張子を含めるかを切り替えます.
- いつ使う:
  - 含める: book.xlsm.VBA のようにブック種別を明示したい.
  - 除外する: book.VBA のように短い名前にしたい.
- 規定値: --include-extension（含める）

```console
uv run pre_commit_vba.py extract --exclude-extension
```

### --version

- 何をする: バージョンだけ表示して終了します.
- いつ使う: CIや調査時に, 実行環境のバージョン確認だけしたいとき.
- 規定値: 指定しない（通常実行）

```console
uv run pre_commit_vba.py extract --version
```

## check オプション

### --target-path

- 何をする: チェック対象のExcelブック探索ディレクトリを指定します.
- いつ使う: リリース対象ブックがサブフォルダにあるとき.
- 規定値: .

```console
uv run pre_commit_vba.py check --target-path ./release-books
```

### --version

- 何をする: バージョンだけ表示して終了します.
- いつ使う: フック環境の診断時.
- 規定値: 指定しない（通常実行）

```console
uv run pre_commit_vba.py check --version
```

## よくある使い方パターン

### 1. 標準運用（迷ったらこれ）

```console
uv run pre_commit_vba.py extract
uv run pre_commit_vba.py check
```

### 2. 出力をシンプルな1フォルダ構成にしたい

```console
uv run pre_commit_vba.py extract --disable-folder-annotation --exclude-extension
```

### 3. 既存リポジトリの命名に合わせたい

```console
uv run pre_commit_vba.py extract --folder-suffix .vba --code-folder source
```

## 運用上の注意

- extract は実行中に staging 状態の整合性を検査します. 失敗時は git diff --cached で差分を確認してください.
- check は release/v... または hotfix/v... ブランチで特に有効です.
- 一時ファイル（~$ で始まるExcelファイル）は自動で対象外になります.
