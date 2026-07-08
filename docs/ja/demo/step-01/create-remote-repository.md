---
icon: lucide/cloud-upload
---
# リモートリポジトリの作成

## 目的

GitHub に空のリポジトリを作成します.  
この後の手順の土台になります.

## 手順

1. GitHub の組織またはプロフィールを開きます.
2. `Repositories` をクリックします.  
   ![move to repository](img/move-to-repository.drawio.svg)
3. `New` をクリックします.  
   ![repository-new-button](img/repository-new-button.drawio.svg)
4. 次の値を入力します.

    - Repository name: `pre-commit-vba-example`
    - Description: `A demo project for pre-commit-vba`
    - Visibility: `Private`
    - Add README: `Off`
    - Add .gitignore: `None`
    - Add license: `None`

5. `Create repository` をクリックします.  
   ![Create a new repository](img/create-repository.drawio.svg){width="650"}

## 確認ポイント

- リポジトリトップが表示される.
- 初期ファイルが 0 件で表示される.
- URL が `pre-commit-vba-example` で終わる.

## 補足

同名リポジトリがある場合は作成できません.  
その場合は名前を変更して再作成してください.
