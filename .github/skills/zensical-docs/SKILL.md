---
name: zensical-docs
description: Create or update Zensical documentation pages for this repository, including navigation and bilingual documentation alignment when needed.
license: MIT
---

## When to Use

Use this skill when the user asks to create, update, fix, or reorganize
documentation pages built with Zensical.

- Add a new documentation page.
- Update existing documentation content.
- Add examples, command output, or navigation entries.
- Align English and Japanese documentation.

## Process

1. Identify whether the request is a content fix, new page, navigation change,
   or bilingual update.
2. Confirm the target audience and language scope: English, Japanese, or both.
3. Read the relevant files under `docs/`.
4. Check whether the page exists in both `docs/en/` and `docs/ja/`.
5. If adding a page, inspect `docs/ja/zensical.toml` navigation.
6. Review nearby pages for heading levels, front matter, wording, and examples.
7. Edit the minimum set of files.
8. Update `project.nav` when a new page should appear in the sidebar.
9. Keep corresponding language pages and navigation aligned when applicable.
10. Validate with:

    ```powershell
    uv run scripts/docs.py build-all
    ```

11. For code samples or broader configuration changes, also run:

    ```powershell
    uv run ruff format
    uv run ruff check
    uv run mypy src/
    uv run tox
    ```

## Reference Materials and Decision Criteria

- Main docs live under `docs/`.
- English pages live under `docs/en/`.
- Japanese pages live under `docs/ja/`.
- Shared landing information may live in `docs/index.md`.
- Navigation is defined in `docs/ja/zensical.toml`.
- Match neighboring documentation tone and formatting.
- Use concrete examples and preserve existing `console`, `powershell`,
  `yaml`, and titled code fences.
- In Japanese documentation, use `. ` for sentence-ending periods and `, `
  for commas, not Japanese punctuation.
- Preserve macros such as `{{project_version}}`, the Termynal extension, links,
  and extension-dependent markup.
- Keep changes focused and minimal.
- References:
  - `.github/copilot-instructions.md`
  - `CONTRIBUTING.md`
  - `docs/index.md`
  - `docs/en/`
  - `docs/ja/`
  - `docs/ja/zensical.toml`
  - `.github/workflows/docs.yml`

## Output Format

- Summarize the documentation files changed.
- State whether navigation was updated.
- State whether English and Japanese pages were updated.
- Report validation steps that succeeded and any that could not run.

## Completion and Stop Conditions

- Check for broken relative links, incorrect file paths, and mismatched
  navigation entries.
- Do not modify `.env` or manually edit `uv.lock`.
- Do not make unrelated code changes while editing documentation.
- Ask for confirmation before changing production-impacting configuration outside
  normal documentation setup.
- If the documentation request implies a product behavior change, stop and ask
  whether implementation should be updated separately.
