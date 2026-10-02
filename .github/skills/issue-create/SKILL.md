---
name: issue-create
description: Create well-structured GitHub issues for this repository with duplicate checks, template alignment, and bilingual formatting.
license: MIT
---

# Create GitHub Issues

## Usage

Use this skill when the user asks to create a bug report, feature request, or other actionable GitHub issue in this repository.

## Process

1. Confirm the repository context. Ask if the owner or repository is ambiguous.
2. Select `.github/ISSUE_TEMPLATE/bug_report.md` or `.github/ISSUE_TEMPLATE/feature_request.md`. If no template fits the requested issue type, ask before choosing a fallback.
3. Gather all required details from the template. Ask concise questions for missing information and distinguish facts from assumptions.
4. Search for similar issues. If likely duplicates exist, show them and ask whether to continue.
5. Draft one issue body in Japanese, then `---`, then English. Follow the selected template's section order and keep both languages semantically equivalent.
6. Choose an appropriate issue type and labels. Set assignees only when requested or clearly implied, and do not set a milestone unless requested.
7. Create the issue only after required details and duplicate checks are complete. If creation fails, report the reason and retry once after correcting the input.

For bug reports, follow the wording and section style of issue #55. For feature requests, follow issue #47.

## References

- `CONTRIBUTING.md`
- `README.md`
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/55
- https://github.com/noda-hiroyuki-kit/pre-commit-VBA/issues/47

## Output

After creating an issue, report its number, URL, and title, and briefly summarize the template and metadata used. If creation is blocked or declined, explain why and do not claim an issue was created.

## Completion Conditions

- The issue follows the appropriate template and is bilingual in Japanese-then-English order.
- Similar existing issues were checked before creation.
- The user receives the created issue URL and selected metadata, or a clear explanation of why no issue was created.
- Do not create issues in another repository, assign non-collaborators, or close an issue unless explicitly requested.
