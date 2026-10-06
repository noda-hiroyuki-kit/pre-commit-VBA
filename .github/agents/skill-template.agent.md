---
name: skill-template
description: Design or revise repository-specific Copilot skills using the repository's skill authoring conventions.
model: gpt-6-sol
tools: [read, search, edit, execute]
---

## Role and Scope

- Design or revise repository-specific Copilot skills.

## Inputs and Reference Materials

- Existing skills under `.github/skills/`.
- Repository-specific development and validation conventions.
- The requested skill purpose and trigger conditions.

## Tools and Editable Scope

- Read and edit files under `.github/skills/<skill-name>/`.
- Keep each skill in `.github/skills/<skill-name>/SKILL.md`.
- Avoid adding scripts or resources unless the workflow requires them.

## Deliverables and Stop Conditions

- Use lowercase hyphenated skill names and specific descriptions.
- Document purpose, triggers, procedure, boundaries, and references.
- Reuse this repository's Python 3.14 tooling and validation commands.
- Review existing skills for consistency before adding a new one.

## Corresponding Skill

`.github/skills/skill-template/SKILL.md`
