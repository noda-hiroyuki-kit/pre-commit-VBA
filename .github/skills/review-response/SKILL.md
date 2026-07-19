---
name: review-response
description: Address pull request review comments in this repository one by one, with minimal approved fixes and explicit validation.
license: MIT
---

# Respond to Pull Request Review Comments

Use this skill when a pull request review comment needs analysis, a proposed fix, or an implementation in this repository.

## Trigger Conditions

- A review comment is posted on a pull request in this repository.
- A reviewer requests changes via a GitHub pull request review.
- A collaborator mentions `@copilot` in a pull request comment asking for a fix or clarification.

## Reliable PR Context Retrieval

At the beginning of review handling, fetch pull request context using this fallback order.

1. Try active pull request context from the available GitHub integration first.
2. If active pull request data is unavailable, fetch by pull request number using GitHub API data.
3. If review-thread comments are still missing, fetch the pull request web page as a last resort and parse reviewer comments from that content.
4. Only after unresolved comments are identified, start one-by-one handling.

Notes:

- API responses can omit review-thread comments depending on the endpoint or view.
- If that happens, use the pull request web page result as the source of truth for initial comment discovery.

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
- Understand surrounding context such as imports, structure, callers, and tests.
- Check whether the same issue exists in related files.

### 4. Propose a Minimal Fix and Ask for Decision

- Propose the smallest change that addresses the concern without unrelated modifications.
- If the fix is non-trivial, include a short implementation outline.
- Ask the user to adopt or reject the review comment.
- Wait for explicit user approval before editing files.

### 5. Implement Only Approved Comments

Follow the project conventions below.

#### Language and Runtime

- Python 3.14
- Managed with `uv`; never manually edit `uv.lock`

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

#### Commit Messages

- Use Conventional Commits in English.
- `feat:` for new features.
- `fix:` for bug fixes.
- `docs:` for documentation-only changes.
- `refactor:` for code restructuring without behavior changes.
- `test:` for test-only changes.
- `chore:` for build, CI, or tooling changes.

#### Branch Naming

- `feature/<topic>` for new features or improvements.
- `hotfix/v<semver>` for critical release fixes.
- `release/v<semver>` for release preparation.

### 6. Validate Approved Changes

Run all checks in order.

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
- Do not modify `.env` files or `uv.lock` manually.

### 8. Prepare Review Reply for User Posting

- Do not post review comments directly from the agent.
- The user will paste the final review response in the browser.
- Always return the suggested reply inside a fenced Markdown code block.
- Output only the reply text block, with no preface or trailing explanation, so the user can paste it as-is.
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

- Do not make architectural or breaking changes without reviewer confirmation.
- Do not modify production configuration files such as `.env` or deployment settings without explicit approval.
- Do not merge or close a pull request autonomously.
- Merges into `develop` and `main` require administrator privileges.
- Wait for a repository administrator to perform the final merge into `develop` or `main`.
- If a fix requires many files or touches critical logic, summarize the plan and wait for user approval before implementation.

## References

- AGENTS.md
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- pyproject.toml
- tests/
