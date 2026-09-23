---
icon: lucide/sheet
---
# Excel アプリを構築する { #build-an-excel-app }

## 目的 { #objective }

Excel ブックの変更を Git 管理します.  
`pre-commit-vba` の実行感を確認します.

## 手順 1: ブランチを作る { #step-1-create-a-branch }

```console
git switch develop
git pull
git switch -c feature/create-app
```

## 手順 2: Excel でコードを書く { #step-2-write-code-in-excel }

1. `example-app.xlsm` を開きます.
2. VBE でプロシージャを追加します.
3. ブックを保存します.

## 手順 3: `prek` を実行 { #step-3-run-prek }

```console
git add .
uv run prek
```

初回は, コードの抽出あるため, エラーで終了します.  
そのため, 再実行します.

```console
uv run prek
```

## 手順 4: コミットしてプッシュ { #step-4-commit-and-push }

```powershell
git commit -m "feat: add workbook macro"
git push origin feature/create-app
```

## 手順 5: PR を作ってマージ { #step-5-create-and-merge-a-pr }

GitHub で PR を作成します.  
base を `develop` にしてマージします.

## 確認ポイント { #checkpoints }

- 抽出された VBA ファイルが更新される.
- `uv run prek` が最終的に通る.
- `develop` に変更が入る.
