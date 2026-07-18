# SKILL: Create and Update Zensical Documentation

This skill defines how the Copilot coding agent should create or update Zensical documentation in the `pre-commit-VBA` repository.

## Overview

Use this skill when the task is to add, revise, or reorganize documentation pages built with Zensical.
This includes editing existing Markdown files under `docs/`, adding new pages, updating navigation in `zensical.toml`, and keeping English and Japanese documentation aligned when appropriate.

## Trigger Conditions

- A request asks to create a new documentation page for the docs site.
- A request asks to update or fix existing documentation content.
- A request asks to add examples, command output, navigation entries, or bilingual documentation for the Zensical site.

## Step-by-Step Procedure

### 1. Understand the Documentation Request

- Identify whether the change is a content fix, a new page, a navigation change, or a bilingual update.
- Confirm the target audience and language scope:
  - English only
  - Japanese only
  - Both English and Japanese
- Clarify whether the task affects docs content only or also documentation configuration.

### 2. Inspect Related Documentation Files

- Read the relevant files under `docs/`.
- Check whether the page exists in both `docs/en/` and `docs/ja/`.
- If adding a page, inspect `zensical.toml` navigation before deciding where it should appear.
- Review nearby pages to match heading levels, front matter, wording, and example style.

### 3. Follow Repository Documentation Conventions

#### Docs Structure

- Main docs live under `docs/`.
- English pages live under `docs/en/`.
- Japanese pages live under `docs/ja/`.
- Shared landing information may live in `docs/index.md`.

#### Navigation

- Zensical navigation is defined in `zensical.toml`.
- When adding a new page that should appear in the sidebar, update the `project.nav` section in `zensical.toml`.
- Keep navigation order consistent with existing English and Japanese sections.

#### Content Style

- Keep changes focused and minimal.
- Match the tone and formatting used in neighboring docs pages.
- Use concrete examples when explaining commands or workflows.
- Preserve existing code fence styles such as `console`, `powershell`, `yaml`, and titled fences where already used.

#### Japanese Writing Style

When writing or editing Japanese documentation:

- Use `. ` (ASCII period followed by a space) for sentence-ending periods (句点), not `。` or `．`.
- Use `, ` (ASCII comma followed by a space) for commas within sentences (読点), not `、` or `，`.
- Apply this rule consistently across all Japanese pages under `docs/ja/`.
#### Dynamic Content and Extensions

- This docs site uses Zensical macros. Preserve macro usage such as `{{project_version}}` when relevant.
- The site enables the `Termynal` markdown extension. Use existing Termynal patterns when documenting interactive command output.
- Do not remove or break existing extension-dependent markup unless the task explicitly requires it.

### 4. Keep Language Variants Consistent

- If a page has both English and Japanese versions, update both unless the request clearly limits the change to one language.
- If only one language is changed, note the gap so reviewers can decide whether translation follow-up is needed.
- Keep page structure aligned across languages when possible, even if wording differs naturally.

### 5. Implement the Documentation Change

- Edit the minimum set of files needed.
- For new pages:
  - Create the Markdown file under the correct language directory.
  - Add front matter or icons if sibling pages use them.
  - Add the page to `zensical.toml` navigation when needed.
- For updates:
  - Preserve existing links, anchors, and document flow unless the task requires restructuring.

### 6. Validate the Documentation

Run the documentation build when the environment supports it:

```powershell
uv run zensical build --clean
```

- For docs-only changes, prioritize confirming the docs build succeeds.
- If the task also changes code samples, macros behavior, or docs-related configuration beyond page content, run the broader repository checks when available:

```powershell
uvx ruff format
uvx ruff check
uvx mypy src/
uvx tox -e 314
```

- If the environment does not have `uv` or `uvx`, record that limitation clearly in the final report.
- Check for broken relative links, incorrect file paths, and mismatched navigation entries.

### 7. Communicate the Result

- Summarize which docs files changed.
- State whether navigation was updated.
- State whether both English and Japanese pages were updated.
- Report which validation steps ran successfully and which could not run.

## Boundaries and Escalation

- Do not modify `.env`.
- Do not manually edit `uv.lock`.
- Do not make unrelated code changes while editing docs.
- Ask for confirmation before changing production-impacting configuration outside normal docs setup.
- If the requested docs change implies a behavior change in the product, ask whether implementation should be updated separately.

## References

- `AGENTS.md`
- `CONTRIBUTING.md`
- `docs/index.md`
- `docs/en/`
- `docs/ja/`
- `zensical.toml`
- `.github/workflows/docs.yml`
