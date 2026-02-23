# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add pre-commit hook (#18).  
  pre-commitフックの追加.

## [0.0.2] - 2026-02-16

### Added

- Add feature to trim trailing whitespace from VBA metadata (#12).  
  VBAコードの付加情報の行末空白削除機能を追加

### Fixed

- Fix @Folder annotation fails when parentheses are used (#4).  
  @Folderアノテーションにカッコを含むと失敗するを修正
- Fix Excel terminates unexpectedly when running the command (#6).  
  excelを使用中にコマンドを走らせると使用中のexcelが終了するのを修正
- Fix process stops with an error when the workbook contains a UserForm (#8).  
  ワークブックにユーザフォームが含まれているとエラーで停止するのを修正
- Fix process terminates with an error when running the check command while a workbook in the target directory is open in Excel (#10).  
  checkコマンドを実行するディレクトリのワークブックをEXCELで開いているときに, checkコマンドを実行するとエラーで停止するのを修正

## [0.0.1] - 2026-01-17

### Added

- Release as first version

[unreleased]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/noda-hiroyuki-kit/pre-commit-VBA/releases/tag/v0.0.1
