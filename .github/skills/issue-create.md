# SKILL: Create GitHub Issues

This skill defines how the Copilot coding agent should create GitHub issues in the pre-commit-VBA repository.

## Overview

Use this skill when the user asks to create a new issue.
The goal is to create a clear, actionable issue without duplicates and with correct metadata.
Issue bodies must follow the repository issue template format.
Issue bodies must be bilingual in this order:

1. Japanese
2. `---`
3. English

## Trigger Conditions

- A request explicitly asks to create an issue.
- A request asks to file a bug report, feature request, or task as a GitHub issue.
- A request provides problem details and asks to track them in GitHub.

## Step-by-Step Procedure

### 1. Confirm Repository Context

- Determine owner and repository name from current context.
- If repository context is ambiguous, ask the user to confirm before writing.

### 2. Select and Load Issue Template

- Identify issue kind first: bug or feature request.
- For bug issues, use `.github/ISSUE_TEMPLATE/bug_report.md`.
- For feature issues, use `.github/ISSUE_TEMPLATE/feature_request.md`.
- Keep section headings, order, and intent aligned with the selected template.
- If user asks for another issue type and no matching template exists, confirm a fallback format before creating.

### 3. Gather Required Inputs

- Collect all fields required by the selected issue template.
- Ask concise follow-up questions for missing required sections.
- Keep user-provided facts separate from assumptions.

### 4. Check for Duplicates Before Creating

- Search existing issues with similar keywords and scope.
- If likely duplicates are found, present them and ask whether to continue creating a new issue.
- Only create a new issue after duplicate check is complete.

### 5. Select Metadata

- List available issue types when repository supports issue types, then choose the best match.
- Choose labels that match scope and severity.
- Apply assignees only when explicitly requested or clearly implied.
- Do not set milestone unless the user asks.

### 6. Draft the Issue Body (Template + Bilingual)

- Base the body on the selected file under `.github/ISSUE_TEMPLATE`.
- Preserve template structure and fill each section with concrete, concise content.
- Do not remove template sections unless they are explicitly optional and clearly not applicable.
- Build the body in this strict order:
  - Japanese section (template-aligned headings in Japanese)
  - `---`
  - English section (original template headings in English)
- Keep Japanese and English content semantically equivalent.

### 7. Bilingual Formatting Rules

- Use one markdown body, not separate issues per language.
- The separator must be exactly `---` on its own line.
- For bug reports, follow issue #55 style:
  - Japanese: `**バグを記述してください**`, `**再現手順**`, `**期待されるふるまい**`, `**補足**`
  - Then `---`
  - English: `**Describe the bug**`, `**Steps to reproduce**`, `**Expected behavior**`, `**Additional context**`
- For feature requests, follow issue #47 style:
  - Japanese: `**この機能リクエストは、どのような課題に関連するものですか?**`, `**どのような解決策を希望しますか?**`, `**検討した代替案**`, `**付加情報**`
  - Then `---`
  - English: `**Is your feature request related to a problem? Please describe.**`, `**Describe the solution you'd like**`, `**Describe alternatives you've considered**`, `**Additional context**`

### 8. Create the Issue

- Create the issue with title, body, and selected metadata.
- Capture returned issue number and URL.
- If creation fails, report the exact failure reason and retry once after fixing input.

### 9. Report Back

- Share the created issue number, URL, and title.
- Briefly summarize template used, labels, type, assignees, and next suggested action.

## Boundaries and Escalation

- Do not create issues in a different repository without explicit user confirmation.
- Do not assign users who are not repository collaborators.
- Do not close issues immediately after creation unless the user explicitly requests that workflow.
- If issue creation requires project-specific fields that are not known, ask for confirmation before submitting.

## References

- AGENTS.md
- CONTRIBUTING.md
- README.md
- .github/ISSUE_TEMPLATE/bug_report.md
- .github/ISSUE_TEMPLATE/feature_request.md
- https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/55
- https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/47
