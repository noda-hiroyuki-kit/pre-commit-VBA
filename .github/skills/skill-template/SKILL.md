---
name: skill-template
description: Create or update repository-specific Copilot skills using this repository's conventions.
license: MIT
---

# Author Repository Skills

## Usage

Use this skill when creating or revising a repository-specific Copilot skill under `.github/skills/`.

## Process

1. Clarify the skill's purpose, expected users, and activation requests.
2. Create a dedicated directory containing `SKILL.md`. Use lowercase hyphenated names.
3. Add front matter with a specific `name`, a clear `description`, and `license: MIT`:

   ```yaml
   ---
   name: example-skill
   description: Explain what the skill does and when Copilot should use it.
   license: MIT
   ---
   ```

4. Use the same English section structure as repository skills: `Usage`, `Process`, `References`, `Output`, and `Completion Conditions`.
5. Give the process actionable steps. Include repository-specific boundaries, relevant validation (`uv run tox -e 3.14` for tests), and how to communicate results.
6. Keep scope focused. Add scripts or resources alongside the skill only when its workflow requires them.
7. Check all referenced paths and commands. For code changes, use the applicable format, lint, type-check, and test commands documented in `CONTRIBUTING.md`; use `uv run tox -e 3.14` for tests.

## References

- `CONTRIBUTING.md`
- `README.md`
- `.github/skills/`
- `pyproject.toml`

## Output

Summarize the created or updated skill path, its activation purpose, and any validation performed.

## Completion Conditions

- The skill has valid front matter and a clear activation description.
- The document uses the common English section structure and accurately describes its workflow.
- Referenced files and validation commands exist; no unnecessary dependencies or helper resources are introduced.
