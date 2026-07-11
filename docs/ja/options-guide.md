---
icon: lucide/sliders-horizontal
---
# オプションガイド

このページは, `pre-commit-vba` のオプションを説明するガイドです.  
仕様一覧だけを見たい場合は [リファレンス](reference.md) を参照してください.

## コマンド

- `extract`: VBA コードを抽出します.
- `check`: ブランチ名とブックのバージョンを照合します.

## 規定値

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

- 何をする: Excelブックを探索するフォルダを指定します.
- いつ使う: リポジトリのルート以外にブックを置いているとき. (テストに利用するブックなど)
- 規定値: .

```console
uv run pre_commit_vba.py extract --target-path ./tests
```

### --folder-suffix

- 何をする: 生成される共通フォルダ名の末尾を変更します.
- いつ使う: チーム規約で出力フォルダ名を統一したいとき.
- 規定値: .VBA

```console
uv run pre_commit_vba.py extract --folder-suffix src
```

### --export-folder

- 何をする: エクスポートされた生ファイルの格納先名を変更します.
- いつ使う: 生ファイルの保存先を別名フォルダで管理したいとき.
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

- 何をする: git管理用の最終コードの格納先名を変更します.
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
    - 作成する: エクスポートされた生ファイルは, git管理しない.
    - 作成しない: 既存の .gitignore 運用に合わせたい. (非推奨)
    !!!Note
        GitHubでは, テキストをutf-8の文字コードとして管理する.  
        コードに漢字などが含まれている場合は, 文字化けする.
- 規定値: --create-gitignore（作成する）

```console
uv run pre_commit_vba.py extract --not-create-gitignore
```

### --include-extension / --exclude-extension

- 何をする: 出力フォルダ名に元ブックの拡張子を含めるかを切り替えます.
- いつ使う:
    - 含める: target-folderに `app.xlsm`, `app.xlam` のように拡張子のみが異なるブックが複数あるとき.
    - 除外する: target-folderに拡張子ちがいのブックがないとき.
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

### 1. 標準運用

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

## 注意

- extract は実行前後の staging 状態の変化を検査します. 1回目は コード抽出によりstaging 状態が変化するためエラーになります.
- check は release/v... または hotfix/v... ブランチでのみ有効です.
- `~$` 始まる一時ファイルは, 処理対象外です.
