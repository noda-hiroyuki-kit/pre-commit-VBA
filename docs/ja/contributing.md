---
icon: octicons/people-16
---
# pre-commit-vbaへの貢献

このプロジェクトに貢献していただきありがとうございます.
このプロジェクトはコード・非コード双方の貢献を歓迎します. バグ報告, ドキュメント改善, テスト, アイデア提案など, さまざまな形の貢献をお受けしています.

## 貢献の方法

以下のようなさまざまな方法で貢献できます.

- バグや予期しない動作を報告する
- 使いやすさの改善案を提案する
- 英語・日本語のドキュメント改善
- テストの追加・改善
- バグ修正・新機能実装

## 始める前に

新しい Issue や PR を開く前に, 既存の議論を確認してください.

- Issues: https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues
- Pull Requests: https://github.com/noda-hiroyuki-kit/pre-commit-vba/pulls

大きな変更の場合は, 先に Issue を開いてスコープと方向性について相談してください.

## 開発環境のセットアップ

このプロジェクトは `uv` を使用し, Python 3.14 をターゲットにしています.

1. リポジトリをクローンしてディレクトリに移動します.
2. 依存関係をインストールします.

```powershell
mise install
uv sync
```

## コード品質チェック

PR を開く前に, 以下のチェックを実行してください.

```powershell
uvx ruff format
uvx ruff check
uvx mypy src/
```

注意点：

- 変更は小分けにして最小限にしてください.
- 既存のプロジェクト構造と命名パターンに従ってください.
- `uv.lock` を手動編集しないでください.
- `.env` ファイルは変更しないでください.

## テストの実行

テストスイート全体を実行します.

```powershell
uv run pytest
uv run pytest tests/test_pre_commit_vba.py::TestExtractCommandExistenceFiles
```

テストは `pytest` で記述され, `tests/` ディレクトリの `test_*.py` ファイルにあります.
可能な限り, バグ修正と新しい機能にはテストを追加してください.

## バグ報告

バグ報告テンプレートを使用してください.

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=bug_report.md

良いバグ報告には以下の情報を含めてください.

- 環境情報（OS, Python バージョン, インストール方法）
- 再現手順
- 期待される動作と実際の動作
- ワークブックサンプルやログ

## 機能提案

機能リクエストテンプレートを使用してください.

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=feature_request.md

以下の内容を含めて説明してください.

- 解決したい問題
- 提案する動作
- 検討した代替案

## 変更の提出

1. `main` ブランチから新しいブランチを作成します.
2. 変更を実装します.
3. フォーマッター, リンター, 型チェック, テストを実行します.
4. PR を開き, 明確な説明, 動機, テスト実施内容を記載してください.

PR チェックリスト：

- [ ] 動作変更時にテストを追加・更新している
- [ ] `ruff`, `mypy`, `pytest` がローカルで通過している
- [ ] 必要に応じてドキュメントを更新している

## コミット・ブランチ規約

Conventional Commits を英語で使用してください.

- `feat:` （機能追加）
- `fix:` （バグ修正）
- `docs:` （ドキュメント）
- `refactor:` （リファクタリング）
- `test:` （テスト）
- `chore:` （その他）

推奨ブランチ名：

- `feature/<topic>`
- `hotfix/v<semantic-version>`
- `release/v<semantic-version>`

## 行動規範

以下を読んで従ってください.

- [`code-of-conduct`](code-of-conduct.md)

## 謝意

すべての貢献に感謝します.
貢献者はリリースノート, リポジトリディスカッションでの謝辞, マージされたPRなどで認識される可能性があります.

## 困ったときは

どこから始めればよいかわからない場合：

- GitHub Issue で質問を開いてください.
- ドキュメント改善や小さなバグ修正から始めてください.
- PR ドラフトで質問してください.
