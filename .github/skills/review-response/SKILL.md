---
name: review-response
description: Address pull request review comments in this repository one by one, with minimal approved fixes and explicit validation.
license: MIT
---

## When to Use

Use this skill when a pull request review comment needs analysis, a proposed
fix, or an implementation in this repository.

- A review comment is posted on a pull request.
- A reviewer requests changes through a pull request review.
- A collaborator mentions `@copilot` in a pull request comment asking for a fix
  or clarification.

## Process

1. Retrieve pull request context using this fallback order:
   1. Active pull request context from the available GitHub integration.
   2. Pull request data by number using GitHub API data.
   3. The pull request web page if review-thread comments are still missing.
2. Identify unresolved comments and select exactly one.
3. Copy the exact concern and referenced location.
4. Read the full comment and inspect the relevant code, callers, tests, and
   related files.
5. Identify whether the concern is a bug, style violation, missing test,
   documentation gap, or design question.
6. Propose the smallest fix and ask the user whether to adopt the comment.
7. Implement only explicitly approved changes.
8. Validate approved changes in this order:

   ```powershell
   uv run ruff format
   uv run ruff check
   uv run mypy src/
   uv run tox
   ```

9. Commit only approved changes with a Conventional Commits message.
10. Prepare the review reply and continue with the next unresolved comment.

## Reference Materials and Decision Criteria

- API responses can omit review-thread comments. When that happens, use the
  pull request web page as the source of truth for initial discovery.
- Process review comments strictly one by one; never bundle comments.
- If a comment is ambiguous, ask for clarification before proposing a change.
- Use Python 3.14 and `uv`.
- Format with Ruff, lint with Ruff, and type-check with mypy.
- Tests use pytest, live under `tests/`, and target at least 80% coverage.
- Add or update tests whenever behavior changes.
- Use Conventional Commits in English:
  `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, and `chore:`.
- Use branch names `feature/<topic>`, `hotfix/v<semver>`, or
  `release/v<semver>`.
- References:
  - `.github/copilot-instructions.md`
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md`
  - `pyproject.toml`
  - `tests/`

## Output Format

Do not post review comments directly. Return the suggested reply inside a
fenced Markdown code block, with no preface or trailing explanation.

Accepted:

```markdown
Accepted.
Addressed in commit <COMMIT_ID>.

<One concise sentence describing the implemented change and why it resolves the concern.>
```

Declined:

```markdown
Declined.
No code changes were made.

<One concise sentence explaining the intentional design choice and why current behavior is acceptable for this repository.>
```

Provide the response text in English.

## Completion and Stop Conditions

- If the user rejects a comment, do not implement it and move to the next one.
- All required checks must pass before pushing.
- Do not modify `.env` or manually edit `uv.lock`.
- Do not make architectural or breaking changes without reviewer confirmation.
- Do not merge or close pull requests autonomously.
- Wait for an administrator before merging into `develop` or `main`.
- If a fix requires many files or touches critical logic, summarize the plan and
  wait for user approval.
