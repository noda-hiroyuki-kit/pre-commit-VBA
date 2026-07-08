---
icon: octicons/people-16
---
# pre-commit-vba への貢献

貢献ありがとうございます.  
コード・非コード双方の貢献を歓迎します.

## 貢献の方法

以下のようなさまざまな方法の貢献を歓迎します.

- バグや予期しない動作を報告する
- 使いやすさの改善案を提案する
- 英語・日本語のドキュメント改善
- テストの追加・改善
- バグ修正・新機能実装

## 始める前に

既存の Issue と PR を確認してください.

- Issues: https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues
- Pull Requests: https://github.com/noda-hiroyuki-kit/pre-commit-vba/pulls

大きな変更は先に Issue で相談してください.

## 開発環境

このプロジェクトは `uv` を使います.  
対象 Python は 3.14 です.

```powershell
mise install
uv sync
```

## 品質チェック

PR 前に次を実行してください.

```powershell
uv run ruff format
uv run ruff check
uv run mypy src/
```

注意点：

- 変更は小分けにして最小限にしてください.
- 既存のプロジェクト構造と命名パターンに従ってください.
- `uv.lock` を手動編集しないでください.
- `.env` ファイルは変更しないでください.

## テスト

```powershell
uv run pytest
uv run pytest tests/test_pre_commit_vba.py::TestExtractCommandExistenceFiles
```

- テストは `pytest` で書いてください.
- `tests/test_*.py` に置いてください.
- 新機能と修正にはテストを追加してください.

## バグ報告

バグ報告テンプレートを使用してください.

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=bug_report.md

報告には次を含めてください.

- 環境情報
- 再現手順
- 期待値と実際の結果
- サンプルやログ

## 機能提案

機能リクエストテンプレートを使用してください.

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=feature_request.md

提案には次を含めてください.

- 解決したい問題
- 提案する動作
- 代替案

## 変更の提出

1. `main` からブランチをつくってください.
2. 変更を実装してください.
3. 品質チェックとテストを実行してください.
4. PR に説明と結果を記載してください.

チェックリスト:

- [ ] テストを追加または更新した
- [ ] `ruff` `mypy` `pytest` が通った
- [ ] 必要な文書を更新した

## 規約

Conventional Commits を英語で使用してください.

- `feat:`
- `fix:`
- `docs:`
- `refactor:`
- `test:`
- `chore:`

推奨ブランチ名:

- `feature/<topic>`
- `hotfix/v<semantic-version>`
- `release/v<semantic-version>`

## 行動規範

- [code-of-conduct](code-of-conduct.md)

## 謝意

すべての貢献に感謝します.  
貢献者はリリースノート, リポジトリディスカッションでの謝辞, マージされたPRなどで認識される可能性があります.

## 困ったときは

どこから始めればよいかわからない場合：

- GitHub Issue で質問を開いてください.
- ドキュメント改善や小さなバグ修正から始めてください.
- Draft PR で質問してください.
