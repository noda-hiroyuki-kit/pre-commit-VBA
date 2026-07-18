# SKILL: Respond to Pull Request Review Comments

This skill defines how the Copilot coding agent should handle pull request review comments in the `pre-commit-VBA` repository.

## Overview

When a reviewer leaves comments on a pull request, follow this skill to analyze each comment, propose a minimal fix, and proceed only after user approval.

## Trigger Conditions

- A review comment is posted on a pull request in this repository.
- A reviewer requests changes via a GitHub PR review.
- A collaborator mentions `@copilot` in a PR comment asking for a fix or clarification.

## Reliable PR Context Retrieval (Start Here)

At the beginning of review handling, fetch PR context using this fallback order.

1. Try active PR context from the available GitHub integration first.
2. If active PR data is unavailable, fetch by PR number using GitHub API data.
3. If review-thread comments are still missing, fetch the PR web page as a last resort and parse reviewer comments from that content.
4. Only after unresolved comments are identified, start one-by-one handling.

Notes:
- API responses can omit review-thread comments depending on the endpoint or view.
- If that happens, use the PR web page result as the source of truth for initial comment discovery.

## Core Rule: One Comment at a Time with User Approval

- Process review comments strictly one by one.
- For each comment, first provide analysis and a proposed change.
- Ask the user whether to adopt that review comment.
- Implement changes only when the user explicitly approves.
- If the user rejects a comment, do not implement it and move to the next comment.

## Step-by-Step Response Procedure

### 1. Select One Review Comment

- Pick a single unresolved review comment.
- Copy the exact concern and referenced location.
- Do not bundle multiple comments into one change.

### 2. Read and Understand the Comment

- Read the full comment carefully, including any referenced code lines.
- Identify the exact concern: bug, style violation, missing test, documentation gap, or design question.
- If the comment is ambiguous, ask for clarification before proposing code changes.

### 3. Inspect the Relevant Code

- Open the files and line ranges referenced in the comment.
- Understand surrounding context (imports, class structure, callers, tests).
- Check whether the same issue exists in related files.

### 4. Propose a Minimal Fix and Ask for Decision

- Propose the smallest change that addresses the concern without unrelated modifications.
- If the fix is non-trivial, include a short implementation outline.
- Ask the user: adopt or reject this review comment.
- Wait for explicit user approval before editing files.

### 5. Implement Only Approved Comments

Follow the project conventions below:

#### Language and Runtime

- Python 3.14
- Managed with `uv`; **never** manually edit `uv.lock`

#### Code Style

- Format with Ruff: `uv run ruff format`
- Lint with Ruff: `uv run ruff check`
- Type-check with mypy: `uv run mypy src/`

#### Tests

- Framework: `pytest`
- Test files: `test_*.py` under `tests/`
- Coverage target: >= 80%
- Run the full test suite before committing: `uv run pytest .`
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

### 6. Validate Approved Changes

Run all checks in order:

```powershell
uv run ruff format
uv run ruff check
uv run mypy src/
uv run pytest .
uv run pytest tests/test_pre_commit_vba.py::TestExtractCommandExistenceFiles
```

All checks must pass before pushing.

### 7. Commit and Push Approved Work

- Commit only changes for comments approved by the user.
- Use a Conventional Commits message that references the approved review concern.
- Example: `fix: handle empty workbook path in extract command`
- Do **not** modify `.env` files or `uv.lock` manually.

### 8. Prepare Review Reply for User Posting

- Do not post review comments directly from the agent.
- The user will paste the final review response in the browser.
- Always return the suggested reply inside a fenced markdown code block.
- Output only the reply text block (no preface or trailing explanation) so the user can paste it as-is.
- Provide the response text in English using one of the templates below.

Accepted template:

```markdown
Accepted.
Addressed in commit <COMMIT_ID>.

<One concise sentence describing the implemented change and why it resolves the concern.>
```

Declined template:

```markdown
Declined.
No code changes were made.

<One concise sentence explaining the intentional design choice and why current behavior is acceptable for this repository.>
```

### 9. Repeat for the Next Comment

- Move to the next unresolved comment.
- Repeat from Step 1.

## Boundaries and Escalation

- **Do not** make architectural or breaking changes without reviewer confirmation.
- **Do not** modify production configuration files (e.g., `.env`, deployment settings) without explicit approval.
- **Do not** merge or close a pull request autonomously.
- If a fix requires many files or touches critical logic, summarize the plan and wait for user approval before implementation.

## References

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent-specific project conventions |
| `CONTRIBUTING.md` | General contribution guidelines |
| `CODE_OF_CONDUCT.md` | Community standards |
| `pyproject.toml` | Project metadata and dependencies |
| `tests/` | Test suite |
