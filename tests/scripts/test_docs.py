# Copyright (c) 2026 Noda Hiroyuki
"""Tests for documentation build helpers."""
# ruff: noqa: S101

from __future__ import annotations

import importlib.util
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

project_root = Path(__file__).parents[2]
docs_spec = importlib.util.spec_from_file_location(
    "project_docs",
    project_root / "scripts" / "docs.py",
)
assert docs_spec is not None
assert docs_spec.loader is not None
docs = importlib.util.module_from_spec(docs_spec)
docs_spec.loader.exec_module(docs)


def test_stage_zensical_docs_writes_language_specific_project_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Stage translated pages and write the language-specific site URL."""
    monkeypatch.chdir(tmp_path)
    docs_root = tmp_path / "docs"
    ja_root = docs_root / "ja"
    en_root = docs_root / "en"
    (ja_root / "docs").mkdir(parents=True)
    (en_root / "docs").mkdir(parents=True)
    (ja_root / "overrides").mkdir()
    (ja_root / "docs" / "index.md").write_text("# Japanese\n", encoding="utf-8")
    (en_root / "docs" / "index.md").write_text("# English\n", encoding="utf-8")
    (docs_root / "missing-translation.md").write_text(
        "Missing translation\n",
        encoding="utf-8",
    )
    (tmp_path / "macros.py").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")

    monkeypatch.setattr(docs, "docs_path", docs_root)
    monkeypatch.setattr(docs, "ja_docs_path", ja_root)
    stage_root = tmp_path / "site_zensical_src"
    monkeypatch.setattr(docs, "zensical_src_path", stage_root)
    monkeypatch.setattr(
        docs,
        "get_updated_config_content",
        lambda: {"project": {"theme": {}}, "theme": {}},
    )

    config_path = docs.stage_zensical_docs("en")

    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    assert config["project"]["site_url"] == f"{docs.site_url}en/"
    assert (stage_root / "en" / "content" / "index.md").read_text(
        encoding="utf-8",
    ) == "# English\n"


def test_make_permalink_line_avoids_duplicate_generated_slugs() -> None:
    """Give repeated headings unique generated anchors."""
    extractor = docs.VisibleTextExtractor()
    permalinks: set[str] = set()

    first = docs._make_permalink_line(  # noqa: SLF001
        "## Introduction\n",
        update_existing=False,
        visible_text_extractor=extractor,
        permalinks=permalinks,
    )
    second = docs._make_permalink_line(  # noqa: SLF001
        "## Introduction\n",
        update_existing=False,
        visible_text_extractor=extractor,
        permalinks=permalinks,
    )

    assert first == "## Introduction { #introduction }\n"
    assert second == "## Introduction { #introduction_1 }\n"


def test_add_permalinks_page_skips_headings_in_code_blocks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Do not add anchors to Markdown headings inside fenced code blocks."""
    docs_root = tmp_path / "docs" / "ja" / "docs"
    docs_root.mkdir(parents=True)
    page = docs_root / "index.md"
    page.write_text(
        "# Visible\n\n```markdown\n# Example\n```\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(docs, "ja_docs_path", tmp_path / "docs" / "ja")

    docs.add_permalinks_page(page)

    assert page.read_text(encoding="utf-8") == (
        "# Visible { #visible }\n\n```markdown\n# Example\n```\n"
    )
