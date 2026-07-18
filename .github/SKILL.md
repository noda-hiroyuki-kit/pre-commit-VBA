# SKILL Index for `pre-commit-VBA`

This file is the index for repository skills used by the Copilot coding agent.

## How to use this index

1. Identify the task category.
2. Open the corresponding skill file under `.github/skills/`.
3. Follow that file's procedure and boundaries.
4. If no skill exists, start from `.github/skills/TEMPLATE.md` and create one.

## Available skills

| Skill | File | Purpose |
|---|---|---|
| Review Comment Response | `.github/skills/review-response.md` | Handle pull request review comments and report fixes clearly |
| Zensical Documentation Authoring | `.github/skills/zensical-docs.md` | Create and update Zensical-based documentation pages for this repository |
| Skill Authoring Template | `.github/skills/TEMPLATE.md` | Base template for creating additional repository-specific skills |

## Naming convention for new skills

- Directory: `.github/skills/`
- File name: kebab-case (example: `release-check.md`)
- First heading format: `# SKILL: <Skill Name>`

## Required sections for each skill

- Overview
- Trigger Conditions
- Step-by-Step Procedure
- Boundaries and Escalation
- References
