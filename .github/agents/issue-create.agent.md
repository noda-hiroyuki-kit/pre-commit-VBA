---
name: issue-create
description: Create a well-structured GitHub issue for this repository when the user asks to report a bug, request a feature, or track a task.
model: gpt-5.4-mini
tools: [read, search, edit, execute]
---

## Role and Scope

- Create a well-structured GitHub issue for this repository.
- Handle bug reports, feature requests, and task tracking requests.

## Inputs and Reference Materials

- User's issue request and provided details.
- Repository issue templates.
- Existing issues for duplicate checks.

## Tools and Editable Scope

- Use the GitHub issue creation tool for the current repository.
- Read issue templates and existing issues.
- Do not modify repository files unless the user explicitly asks for a related
  change.

## Deliverables and Stop Conditions

- Follow the repository issue template and duplicate-check requirements.
- Keep issue bodies bilingual in Japanese first, followed by English.
- Do not create the issue until required information and any duplicate decision
  are resolved.
- Report the created issue number, URL, title, and selected metadata.

## Corresponding Skill

`.github/skills/issue-create/SKILL.md`
