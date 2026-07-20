# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Sync documentation version display with `pyproject.toml` by loading `[project].version` through Zensical macros.  
  Zensical の macros で `[project].version` を読み込み、ドキュメントのバージョン表示を `pyproject.toml` と同期。
- Harmonize impact color usage in demo images across the documentation.  
  ドキュメント全体でデモ画像のインパクトカラーを統一.
- Raise the minimum `mypy` requirement from 2.1.0 to 2.2.0. ([#110])  
  `mypy` の最小要件を 2.1.0 から 2.2.0 へ引き上げ.
- Bump minimum `tox` requirement from 4.56.1 to 4.56.4. ([#111])  
  `tox` の最小要件を 4.56.1 から 4.56.4 へ引き上げ.
- Update pre-commit hooks to `ruff` v0.15.21 and `mypy` v2.2.0. ([#112])  
  pre-commit フックを `ruff` v0.15.21 と `mypy` v2.2.0 に更新.
- Raise the minimum `uv_build` requirement from 0.11.26 to 0.11.28. ([#113])  
  `uv_build` の最小要件を 0.11.26 から 0.11.28 へ引き上げ.
- Bump minimum `zensical` requirement from 0.0.46 to 0.0.50. ([#114])  
  `zensical` の最小要件を 0.0.46 から 0.0.50 へ引き上げ.
- Update docs workflow to use `uv` 0.11.28.  
  ドキュメント用ワークフローで使用する `uv` を 0.11.28 に更新.

### Fixed

- Prevent `Workbook_Open` / `Auto_Open` from executing during `extract` by disabling Excel events and macro automation while opening workbooks. ([#107])  
  `extract` 実行時にワークブックを開く際、Excel のイベントとマクロ自動実行を無効化し、`Workbook_Open` / `Auto_Open` が実行されないように修正. ([#107])

## [0.3.10] - 2026-07-12

### Added

- Add project documentation.  
  プロジェクトドキュメントを追加.

### Changed

- Normalize `.pre-commit-hooks.yaml` descriptions to scalar strings for manifest validation compatibility.  
  マニフェスト検証との互換性のため、`.pre-commit-hooks.yaml` の description をスカラー文字列に正規化.
- Raise the minimum `typer` requirement from 0.26.7 to 0.26.8. ([#95])  
  `typer` の最小要件を0.26.7から0.26.8へ引き上げ.
- Raise the minimum `uv_build` requirement from 0.11.24 to 0.11.26. ([#96])  
  `uv_build` の最小要件を0.11.24から0.11.26へ引き上げ.
- Update docs workflow to use `uv` 0.11.26.  
  ドキュメント用ワークフローで使用する `uv` を 0.11.26 に更新.

## [0.3.9] - 2026-07-06

### Changed

- Raise the minimum `uv_build` requirement from 0.11.23 to 0.11.24. ([#86])  
  `uv_build` の最小要件を0.11.23から0.11.24へ引き上げ.
- Bump minimum `ruff` requirement from 0.15.18 to 0.15.20. ([#87])  
  `ruff` の最小要件を 0.15.18 から 0.15.20 へ引き上げ.
- Bump minimum `zensical` requirement from 0.0.45 to 0.0.46. ([#88])  
  `zensical` の最小要件を 0.0.45 から 0.0.46 へ引き上げ.
- Bump minimum `tox` requirement from 4.55.1 to 4.56.1. ([#89])  
  `tox` の最小要件を 4.55.1 から 4.56.1 へ引き上げ.

## [0.3.8] - 2026-06-30

### Changed

- Raise the minimum `uv_build` requirement from 0.11.22 to 0.11.23. ([#79])  
  `uv_build` の最小要件を0.11.22から0.11.23へ引き上げ.

## [0.3.7] - 2026-06-30

### Changed

- Raise the minimum `uv_build` requirement from 0.11.21 to 0.11.22. ([#79])  
  `uv_build` の最小要件を0.11.21から0.11.22へ引き上げ.
- Bump minimum `ruff` requirement from 0.15.17 to 0.15.18. ([#80])  
  `ruff` の最小要件を 0.15.17 から 0.15.18 へ引き上げ.
- Bump minimum `pytest` requirement from 9.1.0 to 9.1.1.  
  `pytest` の最小要件を 9.1.0 から 9.1.1 へ引き上げ.

### Fixed

- Make `ExcelVbaExporter.__del__` defensive for partially initialized instances and avoid re-raising exceptions during cleanup.  
  `ExcelVbaExporter.__del__` を部分初期化インスタンスでも安全に動作するようにし, クリーンアップ時に例外を再送出しないようにした.
- Handle pytest deprecation warnings in tests by updating test-side implementation details.  
  pytest の非推奨警告に対応するため, テスト実装の詳細を更新.


## [0.3.6] - 2026-06-25

### Changed

- Raise the minimum `uv_build` requirement from 0.11.19 to 0.11.21. ([#68])  
  `uv_build` の最小要件を0.11.19から0.11.21へ引き上げ.
- Switch document generation from MkDocs Material to Zensical.  
  ドキュメント生成ツールを MkDocs Material から Zensical に変更.
- Add Dependabot cooldown settings for dependency update pull requests.  
  Dependabot の依存関係更新 PR に cooldown 設定を追加.
- Bump minimum `pytest` requirement from 9.0.3 to 9.1.0.  
  `pytest` の最小要件を 9.0.3 から 9.1.0 へ引き上げ.

## [0.3.5] - 2026-06-14

### Changed

- Bump runtime dependencies to `pywin32>=312` and `typer>=0.26.7`, and refresh development dependency minimum versions.  
  ランタイム依存関係を `pywin32>=312` と `typer>=0.26.7` に引き上げ, 開発依存関係の最小バージョンを更新.
- Raise the minimum `uv_build` requirement from 0.11.17 to 0.11.19. ([#68])  
  `uv_build` の最小要件を0.11.17から0.11.19へ引き上げ.

## [0.3.4] - 2026-06-07

### Changed

- Raise the minimum `uv_build` requirement from 0.11.16 to 0.11.17. ([#59])  
  `uv_build` の最小要件を0.11.16から0.11.17へ引き上げ.

### Fixed

- Fix YAML indentation in README examples for the `.pre-commit-config.yaml` snippets.  
  README の `.pre-commit-config.yaml` 例の YAML インデントを修正.

## [0.3.3] - 2026-06-01

### Changed

- Raise the minimum `uv_build` requirement from 0.11.15 to 0.11.16 and refresh lockfile/tooling dependencies.  
  `uv_build` の最小要件を0.11.15から0.11.16へ引き上げ, lockfile/ツール依存関係を更新.

## [0.3.2] - 2026-06-01

### Added

- Add Dependabot configuration for the uv ecosystem with weekly update checks.  
  uv エコシステム向けに、週次で更新確認する Dependabot 設定を追加.

### Fixed

- Fix runtime version constant from 0.3.0 to 0.3.2 after the v0.3.1 release.  
  v0.3.1リリース後のランタイムバージョン定数を0.3.0から0.3.2に修正.  
- Prevent runtime version drift by verifying the hard-coded CLI version against pyproject.toml in tests.  
  ハードコードしたCLIバージョンをテストで pyproject.toml と照合することで, ランタイムバージョンのずれを再発しないようにした.

## [0.3.1] - 2026-05-31

### Fixed

- Refine Rubberduck Addin reference detection to avoid false positives from inactive/module-literal patterns and align detection with `Rubberduck.x32.tlb` / `Rubberduck.x64.tlb`. ([#55])  
  非アクティブな参照やモジュール内のリテラルによる誤検知を避けるように Rubberduck Addin 参照検知を改善し, `Rubberduck.x32.tlb` / `Rubberduck.x64.tlb` に合わせて判定するようにした.

## [0.3.0] - 2026-04-20

### Changed

- Detect staged changes introduced during `extract` execution and fail when staging state changes. ([#47])  
  `extract`実行中にステージ状態の変化を検知し, ステージ状態が変わった場合は失敗するようにする.
- Detect Rubberduck Addin references in check and fail when a reference exists. ([#49])  
  checkでRubberduck Addin参照を検知し, 参照がある場合は失敗するようにする.

## [0.2.0] - 2026-04-13

### Added

- Enable `check` on hotfix/ branches as well. ([#36])  
  `check`をhotfix/ブランチでも有効にする.
- Do not create `customUI` folder when customUI files are absent([#39])  
  customUI ファイルが存在しない場合に `customUI`フォルダを作成しないようにする.

### Changed

- Include file extension in extracted folder naming. ([#43])  
  展開フォルダ名にファイル拡張子を含める

### Fixed

- Fixed bug where non-macro Excel files were also being extracted. ([#40])  
  マクロ付きでないExcelファイルも展開されてしまうバグを修正.

## [0.1.3] - 2026-03-04

### Fixed

- Update pre-commit-config.yaml version in README.md  
  README.md の pre-commit-config.yaml内のversionを更新

## [0.1.2] - 2026-03-04

### Changed

- Skip opening workbook in `check` command for non-release branches. ([#28])  
  `check`コマンドで`release/`ブランチ以外のブランチでは, ワークブックを開かないようにする.

## [0.1.1] - 2026-02-25

### Fixed

- Fix when the code contains circled numbers such as ①, it crashes with an error. ([#24])  
  コード内に①などの丸数字を含むとエラーで落ちるのを修正

## [0.1.0] - 2026-02-24

### Added

- Add pre-commit hook ([#18]).  
  pre-commitフックの追加.

## [0.0.2] - 2026-02-16

### Added

- Add feature to trim trailing whitespace from VBA metadata ([#12]).  
  VBAコードの付加情報の行末空白削除機能を追加

### Fixed

- Fix @Folder annotation fails when parentheses are used ([#4]).  
  @Folderアノテーションにカッコを含むと失敗するを修正
- Fix Excel terminates unexpectedly when running the command ([#6]).  
  excelを使用中にコマンドを走らせると使用中のexcelが終了するのを修正
- Fix process stops with an error when the workbook contains a UserForm ([#8]).  
  ワークブックにユーザフォームが含まれているとエラーで停止するのを修正
- Fix process terminates with an error when running the check command while a workbook in the target directory is open in Excel ([#10]).  
  checkコマンドを実行するディレクトリのワークブックをEXCELで開いているときに, checkコマンドを実行するとエラーで停止するのを修正

## [0.0.1] - 2026-01-17

### Added

- Release as first version

[unreleased]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.10...HEAD
[0.3.10]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.9...v0.3.10
[0.3.9]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.8...v0.3.9
[0.3.8]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.6...v0.3.7
[0.3.6]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/releases/tag/v0.0.1
[#107]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/107
[#55]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/55
[#49]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/49
[#47]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/47
[#43]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/43
[#40]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/40
[#39]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/39
[#36]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/36
[#28]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/28
[#24]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/24
[#18]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/18
[#12]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/12
[#10]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/10
[#8]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/8
[#6]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/6
[#4]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/4

[#59]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/59
[#68]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/68
[#79]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/79
[#80]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/80
[#86]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/86
[#87]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/87
[#88]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/88
[#89]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/89
[#95]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/95
[#96]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/96
[#110]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/110
[#111]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/111
[#112]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/112
[#113]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/113
[#114]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/pull/114
