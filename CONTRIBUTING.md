# Contributing to pre-commit-vba

[**日本語はこちら**](CONTRIBUTING_JA.md)

Thank you for your interest in contributing.
This project welcomes code and non-code contributions, including bug reports, documentation updates, tests, and ideas for improvements.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Before You Start](#before-you-start)
- [Development Setup](#development-setup)
- [Code Style and Quality Checks](#code-style-and-quality-checks)
- [Running Tests](#running-tests)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Submitting Changes](#submitting-changes)
- [Commit and Branch Conventions](#commit-and-branch-conventions)
- [Code of Conduct](#code-of-conduct)
- [Recognition](#recognition)
- [Need Help?](#need-help)

## Ways to Contribute

You can contribute in several ways:

- Report bugs and edge cases.
- Suggest enhancements and usability improvements.
- Improve documentation in English or Japanese.
- Add or improve tests.
- Submit bug fixes and new features.

## Before You Start

Please check existing discussions before opening a new one:

- Issues: https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues
- Pull Requests: https://github.com/noda-hiroyuki-kit/pre-commit-vba/pulls

For larger changes, open an issue first so we can align on scope and direction.

## Development Setup

This project uses `uv` and targets Python 3.14.

1. Clone the repository and move into it.
2. Install dependencies:

```powershell
uv sync
```

## Code Style and Quality Checks

Run these checks before opening a pull request:

```powershell
uvx ruff format
uvx ruff check
uvx mypy src/
```

Notes:

- Keep changes focused and minimal.
- Follow existing project structure and naming patterns.
- Do not manually edit `uv.lock`.
- Do not modify `.env` files in contributions.

## Running Tests

Run the full test suite:

```powershell
uv run pytest
uv run pytest tests/test_pre_commit_vba.py::TestExtractCommandExistenceFiles
```

Tests are written with `pytest` and live under `tests/` with `test_*.py` naming.
When possible, add tests for bug fixes and new behavior.

## Reporting Bugs

Use the bug report template:

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=bug_report.md

A good bug report includes:

- Environment details (OS, Python version, how installed).
- Reproduction steps.
- Expected behavior and actual behavior.
- Sample workbook or logs if relevant.

## Suggesting Enhancements

Use the feature request template:

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=feature_request.md

Please explain:

- The problem you want to solve.
- The proposed behavior.
- Alternatives you considered.

## Submitting Changes

1. Create a branch from `main`.
2. Implement your changes.
3. Run formatters, linters, type checks, and tests.
4. Open a pull request with a clear summary, motivation, and testing notes.

Pull request checklist:

- [ ] Tests added or updated when behavior changes.
- [ ] `ruff`, `mypy`, and `pytest` pass locally.
- [ ] Documentation updated when needed.

## Commit and Branch Conventions

Use Conventional Commits in English:

- `feat:`
- `fix:`
- `docs:`
- `refactor:`
- `test:`
- `chore:`

Preferred branch naming:

- `feature/<topic>`
- `hotfix/v<semantic-version>`
- `release/v<semantic-version>`

## Code of Conduct

Please read and follow:

- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

## Recognition

Every contribution is appreciated.
Contributors may be recognized through release notes, acknowledgements in repository discussions, and merged pull requests.

## Need Help?

If you are unsure where to start:

- Open a GitHub issue with your question.
- Start with documentation improvements or small bug fixes.
- Ask for clarification in your pull request draft.
