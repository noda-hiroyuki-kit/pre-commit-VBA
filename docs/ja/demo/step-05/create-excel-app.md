---
icon: lucide/sheet
---
# Excel アプリを構築する

## 目的

Excel ブックの変更を Git 管理します.  
`pre-commit-vba` の実行感を確認します.

## 手順 1: ブランチを作る

```console
git switch develop
git pull
git switch -c feature/create-app
```

## 手順 2: Excel でコードを書く

1. `example-app.xlsm` を開きます.
2. VBE でプロシージャを追加します.
3. ブックを保存します.

## 手順 3: `pre-commit` を実行

```console
git add .
uv run pre-commit
```

初回は, コードの抽出あるため, エラーで終了します.  
そのため, 再実行します.

```console
uv run pre-commit
```

## 手順 4: コミットしてプッシュ

```powershell
git commit -m "feat: add workbook macro"
git push origin feature/create-app
```

## 手順 5: PR を作ってマージ

GitHub で PR を作成します.  
base を `develop` にしてマージします.

## 確認ポイント

- 抽出された VBA ファイルが更新される.
- `uv run pre-commit` が最終的に通る.
- `develop` に変更が入る.
