---
name: zensical-docs
description: Create or update Zensical documentation pages for this repository, including navigation and bilingual documentation alignment when needed.
license: MIT
---

# Create and Update Zensical Documentation

## Usage

Use this skill to add, revise, or reorganize Markdown documentation built with Zensical, including page content, navigation, examples, and English/Japanese variants.

## Process

1. Identify whether the request affects content, navigation, documentation configuration, or language variants. Confirm the target audience and languages when unclear.
2. Read related pages under `docs/`, check the corresponding English and Japanese pages, and inspect `zensical.toml` before changing navigation.
3. Match nearby page structure, front matter, heading levels, examples, code fences, and tone. Keep language variants aligned unless the request limits the scope.
4. Make only the changes needed. Preserve relative links, anchors, Zensical macros, and extension-dependent markup.
5. Build the documentation when the environment supports it:

   ```console
   uv run zensical build --clean
   ```

   If the change also affects product behavior or code, run the relevant checks, including `uv run tox -e 3.14` for tests.
6. Check links, file paths, and navigation entries. If only one language was changed, note the translation gap.

For Japanese pages, use `. ` for sentence-ending periods and `, ` for commas, consistent with existing repository content.

## References

- `CONTRIBUTING.md`
- `docs/index.md`
- `docs/en/`
- `docs/ja/`
- `zensical.toml`
- `.github/workflows/docs.yml`

## Output

Summarize the changed documentation files, whether navigation was updated, which languages were changed, and the results of documentation and other relevant validation.

## Completion Conditions

- Page content and navigation are consistent with repository conventions, and links and paths are checked.
- Corresponding language variants are aligned or any remaining gap is reported.
- Applicable documentation build and test checks are run, or the environmental limitation is stated clearly.
- Product behavior changes are not made implicitly as part of documentation work.
