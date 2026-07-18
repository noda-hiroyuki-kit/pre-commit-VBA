# SKILL: Respond to Pull Request Review Comments

This skill defines how the Copilot coding agent should handle pull request review comments in the `pre-commit-VBA` repository.

## Overview

When a reviewer leaves a comment on a pull request, follow this skill to analyze the feedback, make appropriate changes, and reply with a clear explanation of what was done.

## Trigger Conditions

- A review comment is posted on a pull request in this repository.
- A reviewer requests changes via a GitHub PR review.
- A collaborator mentions `@copilot` in a PR comment asking for a fix or clarification.

## Step-by-Step Response Procedure

### 1. Read and Understand the Review Comment

- Read the full comment carefully, including any referenced code lines.
- Identify the exact concern: bug, style violation, missing test, documentation gap, or design question.
- If the comment is ambiguous, reply asking for clarification before making any changes.

### 2. Inspect the Relevant Code

- Open the files and line ranges referenced in the comment.
- Understand the surrounding context (imports, class structure, callers, tests).
- Check whether the issue also exists in related files.

### 3. Plan the Fix

- Determine the minimal change that addresses the review concern without introducing unrelated modifications.
- If the fix is non-trivial, outline the approach in a reply comment before implementing.
- Do not make sweeping refactors unless explicitly requested by the reviewer.

### 4. Implement the Fix

Follow the project conventions below:

#### Language & Runtime

- Python 3.14
- Managed with `uv`; **never** manually edit `uv.lock`

#### Code Style

- Format with Ruff: `uvx ruff format`
- Lint with Ruff: `uvx ruff check`
- Type-check with mypy: `uvx mypy src/`

#### Tests

- Framework: `pytest`
- Test files: `test_*.py` under `tests/`
- Coverage target: ≥ 80%
- Run the full test suite before committing: `uvx tox -e 314`
- Add or update tests whenever behavior changes.

#### Commit Messages (Conventional Commits, English)

| Type | When to use |
|------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code restructuring, no behavior change |
| `test:` | Test-only changes |
| `chore:` | Build, CI, tooling changes |

#### Branch Naming

| Pattern | Purpose |
|---------|---------|
| `feature/<topic>` | New feature or improvement |
| `hotfix/v<semver>` | Critical bug fix on a release |
| `release/v<semver>` | Release preparation |

### 5. Validate Changes

Run all checks in order:

```powershell
uvx ruff format
uvx ruff check
uvx mypy src/
uvx tox -e 314
```

All checks must pass before pushing.

### 6. Commit and Push

- Use a Conventional Commits message that references the review concern.
- Example: `fix: handle empty workbook path in extract command`
- Do **not** modify `.env` files or `uv.lock` manually.

### 7. Reply to the Review Comment

Post a reply that includes:

1. **What was changed** — a brief description of the fix.
2. **Why** — the reasoning, referencing the reviewer's concern.
3. **How to verify** — which tests or commands the reviewer can run to confirm the fix.

Example reply:

> Fixed in commit `abc1234`. The empty-path guard was added to `extract_vba()` in `src/pre_commit_vba/pre_commit_vba.py`. You can verify with `uvx tox -e 314` — the new test `test_extract_empty_path` covers this case.

## Boundaries and Escalation

- **Do not** make architectural or breaking changes without reviewer confirmation.
- **Do not** modify production configuration files (e.g., `.env`, deployment settings) without explicit approval.
- **Do not** merge or close a pull request autonomously.
- If the fix requires changes across many files or touches critical logic, summarize the plan in a comment and wait for approval before proceeding.

## Reference Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent-specific project conventions |
| `CONTRIBUTING.md` | General contribution guidelines |
| `CODE_OF_CONDUCT.md` | Community standards |
| `pyproject.toml` | Project metadata and dependencies |
| `tests/` | Test suite |
