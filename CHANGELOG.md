# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Update `yamllint` arguments and add `dictionaries` in `cspell.json` for runtime-referenced docs/configuration files.
  実行時に参照されるドキュメント/設定ファイル向けに, `yamllint` の引数を見直し, `cspell.json` に `dictionaries` 設定を追加.

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

[unreleased]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/releases/tag/v0.0.1
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
