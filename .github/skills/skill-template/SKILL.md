---
name: skill-template
description: Template for authoring additional repository-specific skills in the GitHub Copilot cloud agent format.
license: MIT
---

## When to Use

Use this skill as a reference when creating or revising a repository-specific
Copilot skill.

## Process

1. Create a dedicated lowercase, hyphenated directory under `.github/skills/`.
2. Place a `SKILL.md` file in that directory.
3. Add front matter with `name`, `description`, and `license`.
4. Document the skill's purpose, triggers, procedure, boundaries, and
   references.
5. Read existing skills and review the new skill for consistency.
6. Add scripts or extra resources only when the workflow requires them.

Recommended layout:

```text
.github/skills/example-skill/
└── SKILL.md
```

Example front matter:

```yaml
---
name: example-skill
description: Explain what the skill does and when Copilot should use it.
license: MIT
---
```

## Reference Materials and Decision Criteria

- Existing skills under `.github/skills/`.
- `.github/copilot-instructions.md`
- `CONTRIBUTING.md`
- `README.md`
- Python 3.14
- Format: `uv run ruff format`
- Lint: `uv run ruff check`
- Type check: `uv run mypy src/`
- Tests and full validation: `uv run tox`
- Keep descriptions specific so Copilot can decide when to load the skill.

## Output Format

The completed skill must contain:

- YAML front matter with `name`, `description`, and `license`.
- A clear purpose and usage scope.
- Trigger conditions.
- Step-by-step procedure.
- Boundaries and escalation rules.
- References to relevant repository materials.

## Completion and Stop Conditions

- Keep skill names lowercase and use hyphens for spaces.
- Do not modify `.env`.
- Do not manually edit `uv.lock`.
- Ask for confirmation before making major or production-impacting changes.
- Stop when the skill is complete, focused, consistent with existing skills, and
  contains no unnecessary scripts or resources.
