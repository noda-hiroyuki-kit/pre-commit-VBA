# AGENTS.md

## Project Overview

- python 3.14 のCLIコマンド

## Commands

- Install dependencies: `uv sync`
- Lint: `uvx ruff check`
- Formatter: `uvx ruff format`
- Run all tests: `uvx tox -e 314`
- Type check: `uvx mypy src/`

## Code style
- Use python
- Follow Ruff rules
- Format with Ruff

## Testing

- フレームワーク: pytest
- カバレッジ目標: 80% 以上
- テストファイル: `test_*.py` を`/tests`配下に配置
- コミット前にすべてのテストを実行

## Git

- コミットメッセージ:
  - Conventional Commits 準拠
    - `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
  - 英語で記述する
- ブランチ名: `feature/xxx`, `hotfix/v(semantic versioning)`, `release/v(semantic versioning)`
- PRは必ずテストを通してから作成

## Boundaries

- `.env` ファイルを変更しない
- `uv.lock` を手動編集しない
- 重要な判断を独断で進めない。必ず確認を求める
- 本番環境の設定ファイルを変更する場合は必ず確認を求める

## Workflow

- 変更前に既存ファイルの内容を確認する
- 長時間タスクはステップ分割し、各完了後にファイル保存
- 説明には必ず具体例を含める
