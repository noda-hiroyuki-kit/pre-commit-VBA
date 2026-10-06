---
name: issue-create
description: Create well-structured GitHub issues for this repository with duplicate checks, template alignment, and bilingual formatting.
license: MIT
---

## When to Use

Use this skill when the user asks to create a new issue, file a bug report,
request a feature, or track a task in this repository.

## Process

1. Determine the owner and repository from the current context.
2. Identify the issue kind: bug, feature request, or task.
3. For bugs and feature requests, load the matching template:
   - `.github/ISSUE_TEMPLATE/bug_report.md`
   - `.github/ISSUE_TEMPLATE/feature_request.md`
   For tasks, draft a bilingual issue using the fallback format below and
   confirm that format with the user before creating the issue.
4. Collect all required information and ask concise follow-up questions for
   missing sections.
5. Search existing issues for likely duplicates. If likely duplicates exist,
   present them and ask whether to continue.
6. Select appropriate issue types and labels. Set assignees or milestones only
   when explicitly requested or clearly implied.
7. Draft the issue body using the selected template.
8. Create the issue with the GitHub issue creation tool.
9. Capture and report the issue number and URL.

## Reference Materials and Decision Criteria

- Preserve the selected issue template's headings, order, and intent.
- Keep user-provided facts separate from assumptions.
- Issue bodies must be bilingual in this order:
  1. Japanese
  2. `---`
  3. English
- Keep Japanese and English content semantically equivalent.
- For bug reports, follow issue #55 style:
  - Japanese: `**バグを記述してください**`, `**再現手順**`,
    `**期待されるふるまい**`, `**補足**`
  - English: `**Describe the bug**`, `**Steps to reproduce**`,
    `**Expected behavior**`, `**Additional context**`
- For feature requests, follow issue #47 style:
  - Japanese: `**この機能リクエストは、どのような課題に関連するものですか?**`,
    `**どのような解決策を希望しますか?**`, `**検討した代替案**`,
    `**付加情報**`
  - English: `**Is your feature request related to a problem? Please describe.**`,
    `**Describe the solution you'd like**`,
    `**Describe alternatives you've considered**`, `**Additional context**`
- For tasks without a dedicated template, use this fallback format:
  - Japanese: `**タスクの概要**`, `**背景・目的**`, `**完了条件**`,
    `**補足**`
  - English: `**Task summary**`, `**Background and goal**`,
    `**Acceptance criteria**`, `**Additional context**`
- Present the fallback format to the user for confirmation before creating a
  task issue.
- References:
  - `.github/copilot-instructions.md`
  - `CONTRIBUTING.md`
  - `README.md`
  - `.github/ISSUE_TEMPLATE/bug_report.md`
  - `.github/ISSUE_TEMPLATE/feature_request.md`
  - `https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/55`
  - `https://github.com/noda-hiroyuki-kit/pre-commit-vba/issues/47`

## Output Format

- Create one issue body, not separate issues per language.
- Report the created issue number, URL, title, template, labels, type,
  assignees, and suggested next action.
- If creation fails, report the exact failure reason and retry once after
  correcting the input.

## Completion and Stop Conditions

- Do not create the issue until required information and the duplicate decision
  are resolved.
- Do not create issues in another repository without explicit confirmation.
- Do not assign users who are not repository collaborators.
- Do not close an issue immediately after creation unless explicitly requested.
- If required project-specific fields are unknown, stop and ask for
  confirmation.
