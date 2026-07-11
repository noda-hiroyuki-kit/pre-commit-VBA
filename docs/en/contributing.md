---
icon: octicons/people-16
---
# Contributing to pre-commit-vba

Thank you for contributing.  
Both code and non-code contributions are welcome.

## How to Contribute

We welcome many types of contributions, such as:

- Reporting bugs or unexpected behavior
- Proposing usability improvements
- Improving English and Japanese documentation
- Adding or improving tests
- Fixing bugs and implementing new features

## Before You Start

Please check existing issues and pull requests.

- Issues: https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues
- Pull Requests: https://github.com/noda-hiroyuki-kit/pre-commit-vba/pulls

For large changes, please discuss in an issue first.

## Development Environment

This project uses `uv`.  
The target Python version is 3.14.

```powershell
mise install
uv sync
```

## Quality Checks

Run the following before creating a PR.

```powershell
uv run ruff format
uv run ruff check
uv run mypy src/
```

Notes:

- Keep changes small and minimal.
- Follow the existing project structure and naming patterns.
- Do not edit `uv.lock` manually.
- Do not modify the `.env` file.

## Testing

```powershell
uv run pytest
uv run pytest tests/test_pre_commit_vba.py::TestExtractCommandExistenceFiles
```

- Write tests with `pytest`.
- Place them under `tests/test_*.py`.
- Add tests for new features and fixes.

## Bug Reports

Please use the bug report template.

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=bug_report.md

Include the following in your report:

- Environment information
- Steps to reproduce
- Expected and actual results
- Samples or logs

## Feature Proposals

Please use the feature request template.

- https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/new?template=feature_request.md

Include the following in your proposal:

- The problem you want to solve
- The behavior you propose
- Alternatives

## Submitting Changes

1. Create a branch from `main`.
2. Implement your changes.
3. Run quality checks and tests.
4. Include explanations and results in your PR.

Checklist:

- [ ] Added or updated tests
- [ ] `ruff`, `mypy`, and `pytest` passed
- [ ] Updated required documentation

## Conventions

Use Conventional Commits in English.

- `feat:`
- `fix:`
- `docs:`
- `refactor:`
- `test:`
- `chore:`

Recommended branch names:

- `feature/<topic>`
- `hotfix/v<semantic-version>`
- `release/v<semantic-version>`

## Code of Conduct

- [code-of-conduct](code-of-conduct.md)

## Appreciation

Thank you for every contribution.  
Contributors may be recognized in release notes, acknowledgements in repository discussions, and merged PRs.

## When You Need Help

If you are unsure where to start:

- Open a question in GitHub Issues.
- Start with documentation improvements or small bug fixes.
- Ask questions in a draft PR.
