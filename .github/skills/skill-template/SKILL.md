---
name: skill-template
description: Template for authoring additional repository-specific skills in the GitHub Copilot cloud agent format.
license: MIT
---

# Skill Authoring Template

Use this skill as a reference when creating another skill for this repository.

## Recommended Directory Layout

Create a dedicated subdirectory under `.github/skills/` and place a `SKILL.md` file inside it.

Example:

```text
.github/skills/example-skill/
└── SKILL.md
```

## Suggested Front Matter

```yaml
---
name: example-skill
description: Explain what the skill does and when Copilot should use it.
license: MIT
---
```

## Suggested Body Structure

### 1. Overview

- Describe what the skill is for.
- Explain when it should be used.

### 2. Trigger Conditions

- List the kinds of requests that should activate the skill.

### 3. Step-by-Step Procedure

- Clarify the goal and constraints.
- Read related files, tests, and configuration.
- Keep scope focused.
- Avoid unrelated modifications.
- Follow repository validation and communication expectations.

### 4. Boundaries and Escalation

- Do not modify `.env`.
- Do not manually edit `uv.lock`.
- Ask for confirmation before making major or production-impacting changes.

### 5. References

- AGENTS.md
- CONTRIBUTING.md
- README.md

## Repository Conventions to Reuse

- Python: 3.14
- Format: `uv run ruff format`
- Lint: `uv run ruff check`
- Type check: `uv run mypy src/`
- Tests: `uv run pytest .`

## Authoring Notes

- Keep skill names lowercase and use hyphens for spaces.
- Keep the description specific so Copilot can decide when to load the skill.
- Add scripts or extra resources in the same skill directory only when they are required by the workflow.
