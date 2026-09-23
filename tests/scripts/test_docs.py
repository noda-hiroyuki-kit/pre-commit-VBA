# Copyright (c) 2026 Noda Hiroyuki
"""Tests for documentation build helpers."""
# ruff: noqa: D103, EM101, PLR2004, PT018, S101, SLF001

from __future__ import annotations

import importlib.util
import json
import runpy
import sys
import tomllib
from pathlib import Path
from unittest.mock import Mock

import pytest
import typer

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


def test_translate_nav_translates_titled_sections_and_keeps_plain_pages() -> None:
    """Translate dict-based nav sections while leaving plain page strings intact."""
    section_names = {"デモ": {"en": "Demo"}}
    nav = ["index.md", {"デモ": ["demo/a.md", "demo/b.md"]}]

    result = docs.translate_nav(nav, "en", section_names)

    assert result == ["index.md", {"Demo": ["demo/a.md", "demo/b.md"]}]


def test_translate_nav_translates_titled_pages() -> None:
    """Translate dict-based page titles while leaving page paths intact."""
    section_names = {"ホーム": {"en": "Home"}}
    nav = [{"ホーム": "index.md"}]

    result = docs.translate_nav(nav, "en", section_names)

    assert result == [{"Home": "index.md"}]


def test_translate_nav_translates_nested_titled_sections() -> None:
    """Translate nested dict-based nav sections recursively."""
    section_names = {
        "デモ": {"en": "Demo"},
        "手順": {"en": "Steps"},
    }
    nav = [{"デモ": [{"手順": ["demo/step-01.md"]}]}]

    result = docs.translate_nav(nav, "en", section_names)

    assert result == [{"Demo": [{"Steps": ["demo/step-01.md"]}]}]


def test_translate_nav_item_aborts_on_missing_translation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Abort and warn when a nav section title has no translation for the language."""
    with pytest.raises(typer.Abort):
        docs.translate_nav_item({"デモ": []}, "en", {})
    assert "Missing nav section translation" in capsys.readouterr().out

    with pytest.raises(typer.Abort):
        docs.translate_nav_item({"デモ": []}, "fr", {"デモ": {"en": "Demo"}})


def test_get_nav_section_names_loads_yaml_table(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Load the nav section translation table from docs/nav_section_names.yml."""
    table_path = tmp_path / "nav_section_names.yml"
    table_path.write_text('"デモ":\n  en: "Demo"\n', encoding="utf-8")
    monkeypatch.setattr(docs, "nav_section_names_path", table_path)

    assert docs.get_nav_section_names() == {"デモ": {"en": "Demo"}}


def test_stage_zensical_docs_translates_nav_for_non_japanese_language(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate nav section titles when staging a non-Japanese language."""
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
    monkeypatch.setattr(docs, "zensical_src_path", tmp_path / "site_zensical_src")
    monkeypatch.setattr(
        docs,
        "get_updated_config_content",
        lambda: {
            "project": {"theme": {}, "nav": [{"デモ": ["demo/a.md"]}]},
            "theme": {},
        },
    )
    monkeypatch.setattr(
        docs,
        "get_nav_section_names",
        lambda: {"デモ": {"en": "Demo"}},
    )

    config_path = docs.stage_zensical_docs("en")

    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    assert config["project"]["nav"] == [{"Demo": ["demo/a.md"]}]


def test_stage_zensical_docs_aborts_when_nav_translation_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Stop staging when a nav section title has no translation table entry."""
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
    monkeypatch.setattr(docs, "zensical_src_path", tmp_path / "site_zensical_src")
    monkeypatch.setattr(
        docs,
        "get_updated_config_content",
        lambda: {
            "project": {"theme": {}, "nav": [{"デモ": ["demo/a.md"]}]},
            "theme": {},
        },
    )
    monkeypatch.setattr(docs, "get_nav_section_names", dict)

    with pytest.raises(typer.Abort):
        docs.stage_zensical_docs("en")


def test_make_permalink_line_avoids_duplicate_generated_slugs() -> None:
    """Give repeated headings unique generated anchors."""
    extractor = docs.VisibleTextExtractor()
    permalinks: set[str] = set()

    first = docs._make_permalink_line(
        "## Introduction\n",
        update_existing=False,
        visible_text_extractor=extractor,
        permalinks=permalinks,
    )
    second = docs._make_permalink_line(
        "## Introduction\n",
        update_existing=False,
        visible_text_extractor=extractor,
        permalinks=permalinks,
    )

    assert first == "## Introduction { #introduction }\n"
    assert second == "## Introduction { #introduction_1 }\n"


def test_make_permalink_line_registers_preserved_permalink() -> None:
    """Reserve an existing anchor before generating later anchors."""
    extractor = docs.VisibleTextExtractor()
    permalinks: set[str] = set()

    preserved = docs._make_permalink_line(
        "## Introduction { #introduction }\n",
        update_existing=False,
        visible_text_extractor=extractor,
        permalinks=permalinks,
    )
    generated = docs._make_permalink_line(
        "## Introduction\n",
        update_existing=False,
        visible_text_extractor=extractor,
        permalinks=permalinks,
    )

    assert preserved == "## Introduction { #introduction }\n"
    assert generated == "## Introduction { #introduction_1 }\n"


def test_add_permalinks_page_skips_headings_in_code_blocks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Do not add anchors to Markdown headings inside fenced code blocks."""
    docs_root = tmp_path / "docs" / "en" / "docs"
    docs_root.mkdir(parents=True)
    page = docs_root / "index.md"
    page.write_text(
        "# Visible\n\n```markdown\n# Example\n```\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(docs, "en_docs_path", tmp_path / "docs" / "en")

    docs.add_permalinks_page(page)

    assert page.read_text(encoding="utf-8") == (
        "# Visible { #visible }\n\n```markdown\n# Example\n```\n"
    )


def test_text_path_and_language_helpers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert docs.strip_markdown_links("See [guide](guide.md).") == "See guide."
    extractor = docs.VisibleTextExtractor()
    assert extractor.extract_visible_text("<p>Hello <b>world</b></p>") == "Hello world"
    extractor.handle_data("unused")
    assert extractor.text_parts[-1] == "unused"
    assert docs.split_markdown_header("---\ntitle: Test\n---\n# Heading\n\nBody") == (
        "---\ntitle: Test\n---\n# Heading",
        "Body",
    )
    assert docs.split_markdown_header("---\ntitle: Test\n---\nBody") == (
        "---\ntitle: Test\n---",
        "Body",
    )
    assert docs.split_markdown_header("Body") == ("", "Body")
    assert (
        docs.add_markdown_notice("# Heading\n\nBody", "Notice")
        == "# Heading\n\nNotice\n\nBody"
    )
    assert docs.add_markdown_notice("Body", "Notice") == "Notice\n\nBody"
    monkeypatch.setattr(docs, "non_translated_sections", ("api/",))
    assert docs.is_non_translated_path(Path("api/index.md"))
    assert not docs.is_non_translated_path(Path("guide/index.md"))
    assert docs.get_ja_url(Path("index.md")) == docs.site_url
    assert docs.get_ja_url(Path("guide/index.md")) == f"{docs.site_url}guide/"
    assert docs.get_ja_url(Path("guide.md")) == f"{docs.site_url}guide/"
    assert docs.get_zensical_theme_language("zh-hant") == "zh-Hant"
    assert docs.get_zensical_theme_language("en") == "en"
    assert docs.lang_callback(None) is None
    assert docs.lang_callback("JA") == "ja"
    absolute_lang = str(Path(Path.cwd().anchor) / "tmp" / "ja")
    for unsafe_lang in ("../docs/ja", ".", "..", "foo/bar", absolute_lang):
        with pytest.raises(typer.BadParameter, match="single path component"):
            docs.lang_callback(unsafe_lang)
    docs_root = tmp_path / "docs"
    (docs_root / "ja").mkdir(parents=True)
    (docs_root / "ja-extra").mkdir()
    (docs_root / "en").mkdir()
    (docs_root / "README.md").write_text("", encoding="utf-8")
    monkeypatch.setattr(docs, "docs_path", docs_root)
    assert docs.get_lang_paths() == sorted(docs_root.iterdir())
    assert list(docs.complete_existing_lang("j")) == ["ja", "ja-extra"]


def test_asset_and_alternate_config_helpers() -> None:
    config: dict[str, object] = {
        "theme": {"logo": "logo.svg", "favicon": "/favicon.svg"},
        "extra_css": ["style.css", "/extra.css"],
        "extra_javascript": "invalid",
    }
    docs.make_root_asset_paths(config)
    assert config == {
        "theme": {"logo": "/logo.svg", "favicon": "/favicon.svg"},
        "extra_css": ["/style.css", "/extra.css"],
        "extra_javascript": [],
    }
    config = {"theme": "invalid"}
    docs.make_root_asset_paths(config)
    assert config == {"theme": {}, "extra_css": [], "extra_javascript": []}
    alternate = [
        {"name": "ja - Japanese", "link": "/", "lang": "ja"},
        {"name": "en - English", "link": "/en/", "lang": "en"},
    ]
    source = 'title = "Docs"\nalternate = [\n  { name = "old" }\n]\nfooter = true\n'
    result = docs.update_alternate_languages(source, alternate)
    assert 'name = "ja - Japanese"' in result and 'title = "Docs"' in result
    assert "alternate = [" in result
    assert "[[alternate]]" not in result
    assert tomllib.loads(result)["alternate"] == alternate
    empty_result = docs.update_alternate_languages(source, [])
    assert "alternate = []" in empty_result
    with pytest.raises(ValueError, match="exactly one"):
        docs.update_alternate_languages('title = "Docs"\n', alternate)
    with pytest.raises(ValueError, match="exactly one"):
        docs.update_alternate_languages(
            "alternate = []\nother = 1\nalternate = []\n",
            alternate,
        )


def test_stage_translation_and_japanese_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    staged = tmp_path / "staged"
    translated = tmp_path / "translated"
    (staged / "api").mkdir(parents=True)
    translated.mkdir()
    (staged / "translated.md").write_bytes(b"# Original\r\n")
    (staged / "translation-banner.md").write_text("Banner\n", encoding="utf-8")
    (staged / "missing.md").write_bytes(b"# Missing\r\n\r\nBody\r\n")
    (staged / "api" / "skip.md").write_text("# API\n", encoding="utf-8")
    (translated / "translated.md").write_bytes(b"# Translated\r\n")
    (translated / "translation-only.md").write_bytes(b"# Translation only\r\n")
    (translated / "translation-banner.md").write_text("Do not copy\n", encoding="utf-8")
    monkeypatch.setattr(docs, "non_translated_sections", ("api/",))
    docs.stage_translated_docs(staged, translated, "Needs translation")
    assert (staged / "translated.md").read_bytes() == b"# Translated\n"
    assert (staged / "translation-only.md").read_bytes() == b"# Translation only\n"
    assert (staged / "translation-banner.md").read_text(encoding="utf-8") == "Banner\n"
    assert (staged / "missing.md").read_bytes() == (
        b"# Missing\n\nNeeds translation\n\nBody\n"
    )
    assert (staged / "api" / "skip.md").read_text(encoding="utf-8") == "# API\n"
    docs_root = tmp_path / "docs"
    ja_root = docs_root / "ja"
    (ja_root / "docs").mkdir(parents=True)
    (ja_root / "overrides").mkdir()
    (docs_root / "en" / "docs").mkdir(parents=True)
    (docs_root / "missing-translation.md").write_text("Missing\n", encoding="utf-8")
    (ja_root / "docs" / "index.md").write_text("# JA\n", encoding="utf-8")
    (tmp_path / "macros.py").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(docs, "docs_path", docs_root)
    monkeypatch.setattr(docs, "ja_docs_path", ja_root)
    monkeypatch.setattr(docs, "zensical_src_path", tmp_path / "stage")
    monkeypatch.setattr(
        docs,
        "get_updated_config_content",
        lambda: {"project": {"theme": {}}, "theme": {}},
    )
    config_path = docs.stage_zensical_docs("ja")
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    assert config["project"]["site_url"] == docs.site_url


def test_stage_translated_docs_skips_directories(
    tmp_path: Path,
) -> None:
    staged = tmp_path / "staged"
    translated = tmp_path / "translated"
    staged.mkdir()
    translated.mkdir()
    (translated / "nested").mkdir()
    (translated / "editor.bkp").write_text("temporary", encoding="utf-8")

    docs.stage_translated_docs(staged, translated, "Needs translation")

    assert not (staged / "nested").exists()
    assert not (staged / "editor.bkp").exists()


def test_config_build_and_copy_helpers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = tmp_path / "zensical.toml"
    config_path.write_text("[project]\nname = 'docs'\n", encoding="utf-8")
    monkeypatch.setattr(docs, "ja_config_path", config_path)
    assert docs.get_ja_config()["project"]["name"] == "docs"
    executable = tmp_path / "zensical.exe"
    executable.write_text("", encoding="utf-8")
    monkeypatch.setattr(docs.shutil, "which", lambda _: str(executable))
    assert docs.get_zensical_executable() == executable
    monkeypatch.setattr(docs.shutil, "which", lambda _: None)
    with pytest.raises(FileNotFoundError, match="not found"):
        docs.get_zensical_executable()
    run = Mock()
    monkeypatch.setattr(docs.subprocess, "run", run)
    monkeypatch.setattr(docs, "get_zensical_executable", lambda: executable)
    docs.build_zensical_config(config_path)
    run.assert_called_once()
    build_site = tmp_path / "stage" / "en" / "site"
    build_site.mkdir(parents=True)
    generated = build_site.parent / "zensical.toml"
    generated.write_text("[project]\nsite_dir = 'site'\n", encoding="utf-8")
    monkeypatch.setattr(docs, "stage_zensical_docs", lambda _: generated)
    build_mock = Mock()
    monkeypatch.setattr(docs, "build_zensical_config", build_mock)
    assert docs.build_zensical_lang_to_stage("en") == build_site
    build_mock.assert_called_once_with(generated)
    monkeypatch.setattr(docs, "site_path", tmp_path / "site")
    monkeypatch.setattr(docs, "zensical_src_path", tmp_path / "stage")
    (tmp_path / "stage" / "ja" / "site").mkdir(parents=True)
    (tmp_path / "stage" / "ja" / "site" / "index.html").write_text(
        "ja",
        encoding="utf-8",
    )
    docs.copy_zensical_stage_to_site("ja")
    assert (tmp_path / "site" / "index.html").read_text(encoding="utf-8") == "ja"
    (tmp_path / "stage" / "en" / "site").mkdir(parents=True)
    (tmp_path / "stage" / "en" / "site" / "index.html").write_text(
        "en",
        encoding="utf-8",
    )
    docs.copy_zensical_stage_to_site("en")
    assert (tmp_path / "site" / "en" / "index.html").read_text(encoding="utf-8") == "en"


def test_language_and_translation_commands(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "ja").mkdir()
    actual_update_languages = docs.update_languages
    monkeypatch.setattr(docs, "update_languages", Mock())
    docs.new_lang("fr")
    monkeypatch.setattr(docs, "update_languages", actual_update_languages)
    assert (tmp_path / "docs" / "fr" / "llm-prompt.md").exists()
    with pytest.raises(typer.Abort):
        docs.new_lang("fr")
    current = {"project": {"extra": {"alternate": []}}}
    monkeypatch.setattr(docs, "get_ja_config", lambda: current)
    monkeypatch.setattr(docs, "get_updated_config_content", lambda: current)
    monkeypatch.setattr(
        docs,
        "ja_config_path",
        tmp_path / "docs" / "ja" / "zensical.toml",
    )
    docs.ja_config_path.write_text("alternate = [\n]\n", encoding="utf-8")
    docs.update_languages()
    assert "up to date" in capsys.readouterr().out
    updated = {"project": {"extra": {"alternate": [{"name": "en"}]}}}
    monkeypatch.setattr(docs, "get_updated_config_content", lambda: updated)
    with pytest.raises(typer.Exit):
        docs.update_languages()
    assert 'name = "en"' in docs.ja_config_path.read_text(encoding="utf-8")
    capsys.readouterr()
    monkeypatch.setattr(docs, "get_lang_paths", lambda: [tmp_path / "docs" / "fr"])
    monkeypatch.setattr(docs, "SUPPORTED_LANGS", {"fr"})
    docs.langs_json()
    assert json.loads(capsys.readouterr().out.strip().splitlines()[-1]) == ["fr"]


def test_updated_config_cleanup_and_build_all(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    names = tmp_path / "language_names.yml"
    names.write_text("ja: Japanese\nen: English\n", encoding="utf-8")
    monkeypatch.setattr(docs, "docs_path", tmp_path)
    monkeypatch.setattr(docs, "get_ja_config", lambda: {"project": {"extra": {}}})
    for name in ("ja", "en", "draft"):
        (tmp_path / name).mkdir()
    (tmp_path / "file.md").write_text("", encoding="utf-8")
    monkeypatch.setattr(
        docs,
        "get_lang_paths",
        lambda: [
            tmp_path / "ja",
            tmp_path / "en",
            tmp_path / "draft",
            tmp_path / "file.md",
        ],
    )
    result = docs.get_updated_config_content()
    alternate = result["project"]["extra"]["alternate"]
    assert alternate[0]["link"] == "/"
    assert alternate[-1]["link"] == "/en/"
    assert alternate[-1]["lang"] == "en"
    names.write_text("en: English\n", encoding="utf-8")
    with pytest.raises(typer.Abort):
        docs.get_updated_config_content()
    forbidden = tmp_path / "en" / "docs" / "api"
    forbidden.mkdir(parents=True)
    (forbidden / "index.md").write_text("", encoding="utf-8")
    monkeypatch.setattr(docs, "non_translated_sections", ("api",))
    monkeypatch.setattr(
        docs,
        "get_lang_paths",
        lambda: [tmp_path / "ja", tmp_path / "en"],
    )
    with pytest.raises(typer.Exit):
        docs.ensure_non_translated()
    assert not forbidden.exists()
    monkeypatch.setattr(
        docs,
        "get_lang_paths",
        lambda: [tmp_path / "ja", tmp_path / "en"],
    )
    monkeypatch.setattr(docs, "update_languages", Mock())
    monkeypatch.setattr(docs.shutil, "rmtree", Mock())
    pool = Mock()
    pool.__enter__ = Mock(return_value=pool)
    pool.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(docs, "Pool", Mock(return_value=pool))
    monkeypatch.setattr(docs, "copy_zensical_stage_to_site", Mock())
    docs.build_all()
    pool.map.assert_called_once_with(docs.build_zensical_lang_to_stage, ["ja", "en"])
    assert docs.copy_zensical_stage_to_site.call_count == 2


def test_permalink_states_validation_and_delegates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert docs._update_code_block_state(
        "````\n",
        in_code_block3=False,
        in_code_block4=False,
    ) == (False, True)
    assert docs._update_code_block_state(
        "text\n",
        in_code_block3=False,
        in_code_block4=True,
    ) == (False, True)
    assert docs._update_code_block_state(
        "````\n",
        in_code_block3=False,
        in_code_block4=True,
    ) == (False, False)
    assert docs._update_code_block_state(
        "```\n",
        in_code_block3=True,
        in_code_block4=False,
    ) == (False, False)
    assert docs._update_code_block_state(
        "text\n",
        in_code_block3=True,
        in_code_block4=False,
    ) == (True, False)
    assert docs._update_code_block_state(
        "text\n",
        in_code_block3=False,
        in_code_block4=False,
    ) == (False, False)
    assert docs._detect_fence("  ``\n") is None
    assert docs._detect_fence("heading\n") is None
    extractor = docs.VisibleTextExtractor()
    permalinks = {"title"}
    assert (
        docs._make_permalink_line(
            "plain\n",
            update_existing=False,
            visible_text_extractor=extractor,
            permalinks=permalinks,
        )
        == "plain\n"
    )
    existing = "# Title { #old }\n"
    assert (
        docs._make_permalink_line(
            existing,
            update_existing=False,
            visible_text_extractor=extractor,
            permalinks=permalinks,
        )
        == existing
    )
    assert (
        docs._make_permalink_line(
            existing,
            update_existing=True,
            visible_text_extractor=extractor,
            permalinks=permalinks,
        )
        == "# Title { #title_1 }\n"
    )
    docs_root = tmp_path / "docs" / "en" / "docs"
    docs_root.mkdir(parents=True)
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    monkeypatch.setattr(docs, "en_docs_path", tmp_path / "docs" / "en")
    with pytest.raises(RuntimeError, match="inside"):
        docs.add_permalinks_page(outside)
    page = docs_root / "api.md"
    page.write_text("# API\n", encoding="utf-8")
    monkeypatch.setattr(docs, "non_translated_sections", ("api.md",))
    monkeypatch.chdir(tmp_path)
    docs.add_permalinks_page(Path("docs/en/docs/api.md"))
    assert page.read_text(encoding="utf-8") == "# API\n"
    nested_api = docs_root / "api" / "index.md"
    nested_api.parent.mkdir()
    nested_api.write_text("# Nested API\n", encoding="utf-8")
    monkeypatch.setattr(docs, "non_translated_sections", ("api/",))
    docs.add_permalinks_page(Path("docs/en/docs/api/index.md"))
    assert nested_api.read_text(encoding="utf-8") == "# Nested API\n"
    tilde_page = docs_root / "tilde.md"
    tilde_page.write_text(
        "# Visible\n\n~~~markdown\n## Hidden\n~~~\n",
        encoding="utf-8",
    )
    docs.add_permalinks_page(tilde_page)
    assert tilde_page.read_text(encoding="utf-8") == (
        "# Visible { #visible }\n\n~~~markdown\n## Hidden\n~~~\n"
    )
    page_a = tmp_path / "a.md"
    page_b = tmp_path / "b.md"
    page_a.write_text("", encoding="utf-8")
    page_b.write_text("", encoding="utf-8")
    page_mock = Mock()
    monkeypatch.setattr(docs, "add_permalinks_page", page_mock)
    docs.add_permalinks_pages([page_a, page_b], update_existing=True)
    assert page_mock.call_count == 2
    monkeypatch.setattr(docs, "en_docs_path", tmp_path)
    (tmp_path / "one.md").write_text("# One\n", encoding="utf-8")
    docs.add_permalinks()
    assert page_mock.call_count > 2


def test_callback_live_and_serve(monkeypatch: pytest.MonkeyPatch) -> None:
    docs.callback()
    assert docs.os.environ["DYLD_FALLBACK_LIBRARY_PATH"] == "/opt/homebrew/lib"
    executable = Path("zensical")
    monkeypatch.setattr(docs, "get_zensical_executable", lambda: executable)
    monkeypatch.setattr(Path, "is_file", lambda _: False)
    with pytest.raises(RuntimeError, match="could not"):
        docs.live()
    monkeypatch.setattr(Path, "is_file", lambda _: True)
    run = Mock()
    monkeypatch.setattr(docs.subprocess, "run", run)
    docs.live()
    assert run.called

    class StopServer:
        address: tuple[str, int]

        def __init__(self, server_address: tuple[str, int], *_: object) -> None:
            type(self).address = server_address

        def serve_forever(self) -> None:
            raise RuntimeError("stop")

    monkeypatch.setattr(docs, "HTTPServer", StopServer)
    monkeypatch.setattr(docs.os, "chdir", Mock())
    with pytest.raises(RuntimeError, match="stop"):
        docs.serve()
    assert StopServer.address == ("127.0.0.1", 8008)


def test_remaining_cli_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    build_stage = Mock()
    copy_stage = Mock()
    monkeypatch.setattr(docs, "build_zensical_lang_to_stage", build_stage)
    monkeypatch.setattr(docs, "copy_zensical_stage_to_site", copy_stage)
    docs.build_lang("en")
    build_stage.assert_called_once_with("en")
    copy_stage.assert_called_once_with("en")

    monkeypatch.setattr(docs, "docs_path", tmp_path)
    with pytest.raises(typer.Abort):
        docs.stage_zensical_docs("missing")

    monkeypatch.setattr(docs, "non_translated_sections", ())
    monkeypatch.setattr(docs, "get_lang_paths", list)
    docs.ensure_non_translated()

    docs_root = tmp_path / "en" / "docs"
    docs_root.mkdir(parents=True)
    forbidden_file = docs_root / "api.md"
    forbidden_file.write_text("", encoding="utf-8")
    monkeypatch.setattr(docs, "non_translated_sections", ("api.md",))
    monkeypatch.setattr(
        docs,
        "get_lang_paths",
        lambda: [tmp_path / "ja", tmp_path / "en"],
    )
    with pytest.raises(typer.Exit):
        docs.ensure_non_translated()
    assert not forbidden_file.exists()

    monkeypatch.setattr(sys, "argv", ["docs.py", "--help"])
    with pytest.raises(SystemExit):
        runpy.run_path(str(project_root / "scripts" / "docs.py"), run_name="__main__")
