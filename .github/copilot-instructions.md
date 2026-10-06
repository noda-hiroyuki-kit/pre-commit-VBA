# Copilot instructions for pre-commit-vba

## Project overview

- This repository provides a Python 3.14 CLI and pre-commit hooks for extracting
  VBA source from Excel, Word, and PowerPoint files and checking Office-file
  integrity.
- Application code is under `src/pre_commit_vba/`.
- Automated tests are under `tests/`; Office documents and extracted VBA files
  in that tree are test fixtures and should only be changed when the test case
  itself requires it.
- User-facing documentation is maintained in both English and Japanese under
  `README.md`/`README_JA.md` and `docs/en/`/`docs/ja/`.

## Development workflow

1. Read the relevant existing implementation, tests, and documentation before
   editing.
2. Keep changes focused and follow the existing module structure, naming, and
   type annotations.
3. For behavior changes, add or update a `tests/test_*.py` test and update
   related English and Japanese documentation when applicable.
4. Do not edit generated output or binary Office fixtures unless the change
   explicitly requires it.

## Tooling and validation

- Use `uv sync` to install the locked development environment.
- Format Python with `uv run ruff format`.
- Run lint checks with `uv run ruff check`.
- Run type checks with `uv run mypy src/`.
- Run the full validation suite with `uv run tox`.
- The project uses pytest with coverage configured in `pyproject.toml`; maintain
  at least 80% coverage.
- Run the narrowest relevant checks during development, then run the full
  `uv run tox` suite before creating a pull request.
- On Windows, Office/COM-dependent behavior may require the corresponding
  Microsoft Office application and `pywin32`.

## Code and repository conventions

- Target Python 3.14 and follow the Ruff configuration in `pyproject.toml`.
- Keep public behavior and CLI output backward compatible unless the task
  explicitly changes it.
- Handle Windows-only dependencies and cleanup failures explicitly; do not
  silently swallow operational errors or add broad exception catches.
- Use Conventional Commits in English (`feat:`, `fix:`, `docs:`, `refactor:`,
  `test:`, or `chore:`).
- Use the repository's branch naming conventions: `feature/<topic>`,
  `hotfix/v<version>`, or `release/v<version>`.

## Boundaries

- Do not modify `.env` files.
- Do not manually edit `uv.lock`; update it only through the appropriate `uv`
  command when dependency changes require it.
- Do not change production or deployment configuration without explicit
  confirmation.
- Avoid unrelated refactors and do not revert existing user changes.
