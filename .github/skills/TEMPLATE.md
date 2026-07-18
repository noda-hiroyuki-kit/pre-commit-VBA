# SKILL: <Skill Name>

This skill defines how the Copilot coding agent should handle <target task> in the `pre-commit-VBA` repository.

## Overview

Describe what this skill is for and when to use it.

## Trigger Conditions

- <Condition 1>
- <Condition 2>
- <Condition 3>

## Step-by-Step Procedure

### 1. Understand the Request

- Clarify the goal and constraints.
- Confirm expected output and acceptance criteria.

### 2. Inspect Relevant Context

- Read related files, tests, and configuration.
- Verify repository conventions in `AGENTS.md`, `CONTRIBUTING.md`, and docs contributor guidance, and prefer the command style already used in the target docs area for consistency.

### 3. Plan Minimal Changes

- Keep scope focused.
- Avoid unrelated modifications.

### 4. Implement Changes

Follow repository standards:

- Python: 3.14
- Format: `uv run ruff format`
- Lint: `uv run ruff check`
- Type check: `uv run mypy src/`
- Tests: `uv run pytest .`, `uv run pytest tests/test_pre_commit_vba.py::TestExtractCommandExistenceFiles`

### 5. Validate

Run required checks and confirm results.

### 6. Communicate Outcome

- Summarize what changed.
- Explain why.
- Provide verification steps.

## Boundaries and Escalation

- Do not modify `.env`.
- Do not manually edit `uv.lock`.
- Ask for confirmation before making major or production-impacting changes.

## References

- `AGENTS.md`
- `CONTRIBUTING.md`
- `README.md`
