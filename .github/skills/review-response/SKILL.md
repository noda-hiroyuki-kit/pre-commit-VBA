---
name: review-response
description: Address pull request review comments in this repository one by one, with minimal approved fixes and explicit validation.
license: MIT
---

# Respond to Pull Request Review Comments

## Usage

Use this skill when a reviewer or collaborator requests analysis, a fix, or clarification on a pull request in this repository.

## Process

1. Retrieve the pull request context from the active GitHub integration. If unavailable, fetch it by pull request number; use the pull request page only as a last resort for missing review threads.
2. Select one unresolved review comment. Read its full text and inspect the referenced code, related callers, tests, and configuration.
3. Explain the concern and propose the smallest focused change. Ask the user whether to adopt it; do not edit until the user explicitly approves.
4. Implement only approved changes. Follow project conventions: Python 3.14, Ruff formatting and linting, mypy type checking, and no manual edits to `uv.lock` or `.env`.
5. Add or update tests when behavior changes. Run `uv run tox -e 3.14` for the test suite; run other relevant checks when code changes require them.
6. Commit only approved changes with an English Conventional Commit message. Do not merge or close the pull request.
7. Repeat the process for the next unresolved comment only after completing the current one.

## References

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `pyproject.toml`
- `tests/`

## Output

For each comment, provide the analysis and proposed change before asking for approval. Once addressed or declined, return a concise suggested response in a fenced Markdown block, using the appropriate accepted or declined template:

```markdown
Accepted.
Addressed in commit <COMMIT_ID>.

<One concise sentence describing the implemented change and why it resolves the concern.>
```

```markdown
Declined.
No code changes were made.

<One concise sentence explaining the intentional design choice and why current behavior is acceptable for this repository.>
```

## Completion Conditions

- Each review comment is handled separately, and code is changed only after explicit user approval.
- Approved changes are focused and validated; behavior changes have appropriate tests.
- The suggested review response accurately reports the result. Do not claim uncommitted work or post the response directly.
