"""Utilities for building and serving the project's documentation."""
# This file is derived from FastAPI's scripts/docs.py:
# https://github.com/fastapi/fastapi/blob/cba41585675ecb0e119d3ca258821659f07ec3f7/scripts/docs.py
# Copyright (c) 2018 Sebastián Ramírez              # cspell:disable-line
# Copyright (c) 2026 Noda Hiroyuki
# SPDX-License-Identifier: MIT
# See LICENSE in the repository root for the full license text.

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import tomllib
from collections.abc import Iterator  # noqa: TC003
from html.parser import HTMLParser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Pool
from pathlib import Path
from typing import Any

import tomli_w
import typer
import yaml
from slugify import slugify as py_slugify

logging.basicConfig(level=logging.INFO)

SUPPORTED_LANGS = {
    "en",
    "ja",
}


app = typer.Typer()

site_url = "https://noda-hiroyuki-kit.github.io/pre-commit-VBA/"
zensical_name = "zensical.toml"

non_translated_sections: tuple[str, ...] = ()

docs_path = Path("docs").absolute()
ja_docs_path = Path(docs_path, "ja")
en_docs_path = Path(docs_path, "en")
ja_config_path = Path(ja_docs_path, zensical_name)
site_path = Path("site").absolute()
zensical_src_path = Path("site_zensical_src").absolute()
nav_section_names_path = Path(docs_path, "nav_section_names.yml")

header_pattern = re.compile(r"^(#{1,6}) (.+?)(?:\s*\{\s*(#.*)\s*\})?\s*$")
header_with_permalink_pattern = re.compile(r"^(#{1,6}) (.+?)(\s*\{\s*#.*\s*\})\s*$")
code_block3_pattern = re.compile(r"^\s*```")
code_block4_pattern = re.compile(r"^\s*````")
minimum_fence_length = 3


# Pattern to match markdown links: [text](url) → text
md_link_pattern = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def strip_markdown_links(text: str) -> str:
    """Replace markdown links with just their visible text."""
    return md_link_pattern.sub(r"\1", text)


class VisibleTextExtractor(HTMLParser):
    """Extract visible text from a string with HTML tags."""

    def __init__(self) -> None:
        """Initialize the visible text extractor."""
        super().__init__()
        self.text_parts: list[str] = []

    def handle_data(self, data: str) -> None:
        """Collect visible text data from parsed HTML."""
        self.text_parts.append(data)

    def extract_visible_text(self, html: str) -> str:
        """Return the visible text content from an HTML fragment."""
        self.reset()
        self.text_parts = []
        self.feed(html)
        return "".join(self.text_parts).strip()


def slugify(text: str) -> str:
    """Generate a URL-safe slug from markdown-like text."""
    return str(
        py_slugify(
            text,
            replacements=[
                ("`", ""),  # `dict`s -> dicts
                ("'s", "s"),  # it's -> its
                ("'t", "t"),  # don't -> dont
                ("**", ""),  # **FastAPI**s -> FastAPIs
            ],
        ),
    )


def get_ja_config() -> dict[str, Any]:
    """Load the Japanese documentation configuration from disk."""
    return tomllib.loads(ja_config_path.read_text(encoding="utf-8"))


def get_lang_paths() -> list[Path]:
    """Return the paths for all language documentation directories."""
    return sorted(docs_path.iterdir())


def _validate_lang_value(lang: str) -> str:
    """Reject unsafe language values before they are used in filesystem paths."""
    normalized = lang.lower()
    lang_path = Path(normalized)
    if (
        lang_path.is_absolute()
        or normalized in {".", ".."}
        or len(lang_path.parts) != 1
    ):
        message = "Language must be a single path component without '.' or '..'"
        raise typer.BadParameter(message)
    return normalized


def lang_callback(lang: str | None) -> str | None:
    """Normalize a language code for CLI argument validation."""
    if lang is None:
        return None
    return _validate_lang_value(lang)


def complete_existing_lang(incomplete: str) -> Iterator[str]:
    """Yield language directories matching the current partial input."""
    lang_path: Path
    for lang_path in get_lang_paths():
        if lang_path.is_dir() and lang_path.name.startswith(incomplete):
            yield lang_path.name


@app.callback()
def callback() -> None:
    """Configure the fallback library path used by Cairo on macOS."""
    # For MacOS with Cairo
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/lib"


@app.command()
def new_lang(lang: str = typer.Argument(..., callback=lang_callback)) -> None:
    """Generate a new docs translation directory for the language LANG."""
    new_path: Path = Path("docs") / lang
    if new_path.exists():
        typer.echo(f"The language was already created: {lang}")
        raise typer.Abort
    new_path.mkdir()
    new_llm_prompt_path: Path = new_path / "llm-prompt.md"
    new_llm_prompt_path.write_text("", encoding="utf-8")
    typer.echo(f"Successfully initialized: {new_path}")
    update_languages()


@app.command()
def build_lang(
    lang: str = typer.Argument(
        ...,
        callback=lang_callback,
        autocompletion=complete_existing_lang,
    ),
) -> None:
    """Build the docs for a language."""
    build_zensical_lang_to_stage(lang)
    copy_zensical_stage_to_site(lang)
    typer.secho(f"Successfully built docs for: {lang}", fg=typer.colors.GREEN)


def split_markdown_header(markdown: str) -> tuple[str, str]:
    """Split a Markdown document into its front matter/header prefix and body.

    Returns the header prefix (including any YAML front matter) and the heading/body
    portion, preserving the original document structure for later insertion of notices.
    """
    prefix = ""
    if markdown.startswith("---\n"):
        front_matter_end = markdown.find("\n---\n", 4)
        if front_matter_end != -1:
            front_matter_end += len("\n---\n")
            prefix = markdown[:front_matter_end]
            markdown = markdown[front_matter_end:]
    if markdown.startswith("#"):
        header, separator, body = markdown.partition("\n\n")
        if separator:
            return f"{prefix}{header}", body
    if prefix:
        return prefix.rstrip("\n"), markdown
    return "", markdown


def add_markdown_notice(markdown: str, notice: str) -> str:
    """Insert a notice beneath the Markdown header, preserving YAML front matter."""
    header, body = split_markdown_header(markdown)
    if header:
        return f"{header}\n\n{notice}\n\n{body}"
    return f"{notice}\n\n{body}"


def is_non_translated_path(path: Path) -> bool:
    """Return whether a docs path should be excluded from translation checks.

    This is used to skip files that are intentionally left in English or are not
    translated for a given language stage.
    """
    src_path = path.as_posix()
    return any(src_path.startswith(section) for section in non_translated_sections)


def get_ja_url(path: Path) -> str:
    """Return the canonical Japanese documentation URL for a docs path."""
    url_path = path.with_suffix("").as_posix()
    if url_path.endswith("/index"):
        url_path = url_path.removesuffix("index")
    elif url_path != "index":
        url_path = f"{url_path}/"
    else:
        url_path = ""
    return f"{site_url}{url_path}"


def get_zensical_theme_language(lang: str) -> str:
    """Return the language code expected by the Zensical theme.

    The upstream theme uses a capitalized form for Traditional Chinese.
    """
    if lang == "zh-hant":
        return "zh-Hant"
    return lang


def stage_translated_docs(
    staged_docs_path: Path,
    lang_docs_path: Path,
    missing_translation: str,
) -> None:
    """Replace staged Japanese pages with translations where available."""
    for staged_file in staged_docs_path.rglob("*.md"):
        relative_path = staged_file.relative_to(staged_docs_path)
        translated_file = lang_docs_path / relative_path
        if translated_file.is_file():
            if relative_path.name != "translation-banner.md":
                staged_file.write_text(
                    translated_file.read_text(encoding="utf-8"),
                    encoding="utf-8",
                    newline="\n",
                )
        elif not is_non_translated_path(relative_path):
            staged_file.write_text(
                add_markdown_notice(
                    staged_file.read_text(encoding="utf-8"),
                    missing_translation,
                ),
                encoding="utf-8",
                newline="\n",
            )

    for translated_file in lang_docs_path.rglob("*"):
        if not translated_file.is_file() or translated_file.suffix == ".bkp":
            continue
        relative_path = translated_file.relative_to(lang_docs_path)
        if relative_path.name == "translation-banner.md":
            continue
        staged_file = staged_docs_path / relative_path
        staged_file.parent.mkdir(parents=True, exist_ok=True)
        if translated_file.suffix == ".md":
            staged_file.write_text(
                translated_file.read_text(encoding="utf-8"),
                encoding="utf-8",
                newline="\n",
            )
        else:
            shutil.copy2(translated_file, staged_file)


def make_root_asset_paths(project_config: dict[str, object]) -> None:
    """Make shared assets resolve from the root Japanese site."""
    theme = project_config.get("theme")
    if not isinstance(theme, dict):
        theme = {}
        project_config["theme"] = theme
    for key in ("logo", "favicon"):
        if key in theme:
            theme[key] = "/" + str(theme[key]).lstrip("/")
    for key in ("extra_css", "extra_javascript"):
        paths = project_config.get(key, [])
        if not isinstance(paths, list):
            paths = []
        project_config[key] = ["/" + str(path).lstrip("/") for path in paths]


def get_nav_section_names() -> dict[str, dict[str, str]]:
    """Load the ja→language translation table for nav section titles."""
    try:
        raw_section_names_text = nav_section_names_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        typer.echo(
            f"Could not read nav section names from {nav_section_names_path}: {exc}"
        )
        raise typer.Abort from exc
    try:
        raw_section_names = yaml.safe_load(raw_section_names_text)
    except yaml.YAMLError as exc:
        typer.echo(
            f"Could not parse nav section names from {nav_section_names_path}: {exc}"
        )
        raise typer.Abort from exc
    if not isinstance(raw_section_names, dict):
        typer.echo(
            f"Invalid nav section names in {nav_section_names_path}: "
            "expected a mapping of section names to language mappings",
        )
        raise typer.Abort

    section_names: dict[str, dict[str, str]] = {}
    for title, translations in raw_section_names.items():
        if not isinstance(title, str) or not isinstance(translations, dict):
            typer.echo(
                f"Invalid nav section names in {nav_section_names_path}: "
                "expected string titles and language mappings",
            )
            raise typer.Abort
        if any(
            not isinstance(lang, str) or not isinstance(name, str)
            for lang, name in translations.items()
        ):
            typer.echo(
                f"Invalid nav section names in {nav_section_names_path}: "
                "expected string language names and translations",
            )
            raise typer.Abort
        section_names[title] = dict(translations)
    return section_names


NavItem = str | dict[str, str | list["NavItem"]]


def translate_nav_item(
    item: NavItem,
    lang: str,
    section_names: dict[str, dict[str, str]],
) -> NavItem:
    """Translate a single nav entry's navigation title."""
    if not isinstance(item, dict):
        return item
    translated: dict[str, str | list[NavItem]] = {}
    for title, children in item.items():
        translations = section_names.get(title)
        if translations is None or lang not in translations:
            typer.echo(
                f"Missing nav title translation for: {title!r} (lang: {lang}), "
                "update it in docs/nav_section_names.yml",
            )
            raise typer.Abort
        children_value: object = children
        if isinstance(children_value, str):
            translated[translations[lang]] = children_value
        elif isinstance(children_value, list):
            translated[translations[lang]] = [
                translate_nav_item(child, lang, section_names)
                for child in children_value
            ]
        else:
            typer.echo(
                f"Invalid nav children for {title!r}: expected a string or list, "
                f"got {type(children_value).__name__}",
            )
            raise typer.Abort
    return translated


def translate_nav(
    nav: list[NavItem],
    lang: str,
    section_names: dict[str, dict[str, str]],
) -> list[NavItem]:
    """Translate nav section titles for the target language.

    Missing translations abort the build so untranslated labels are never shipped.
    """
    return [translate_nav_item(item, lang, section_names) for item in nav]


def stage_zensical_docs(lang: str) -> Path:
    """Stage the Japanese source docs tree into the Zensical output.

    The target language determines which translations overwrite the staged pages.
    """
    lang_docs_path = docs_path / lang / "docs"
    if not lang_docs_path.is_dir():
        typer.echo(f"The language translation doesn't seem to exist yet: {lang}")
        raise typer.Abort

    ja_docs_source_path = ja_docs_path / "docs"
    lang_stage_path = zensical_src_path / lang
    staged_docs_path = lang_stage_path / "content"
    shutil.rmtree(lang_stage_path, ignore_errors=True)
    shutil.copytree(ja_docs_source_path, staged_docs_path)
    shutil.copy2(Path("macros.py"), lang_stage_path / "macros.py")
    shutil.copy2(Path("pyproject.toml"), lang_stage_path / "pyproject.toml")

    missing_translation = (docs_path / "missing-translation.md").read_text(
        encoding="utf-8",
    )

    if lang != "ja":
        stage_translated_docs(
            staged_docs_path,
            lang_docs_path,
            missing_translation,
        )

    shutil.copytree(ja_docs_path / "overrides", lang_stage_path / "overrides")

    config = get_updated_config_content()
    project_config = config["project"]
    project_config["docs_dir"] = "content"
    project_config["site_dir"] = "site"
    if lang == "ja":
        project_config["site_url"] = site_url
    else:
        project_config["site_url"] = f"{site_url}{lang}/"
    config.setdefault("theme", {})
    project_config["theme"]["language"] = get_zensical_theme_language(lang)
    if lang != "ja":
        # The root Japanese build owns shared static assets; translated builds should
        # reference those root paths instead of emitting language-local copies.
        make_root_asset_paths(project_config)
        if "nav" in project_config:
            nav = project_config["nav"]
            if not isinstance(nav, list):
                typer.echo(
                    f"Invalid project.nav: expected a list, got {type(nav).__name__}",
                )
                raise typer.Abort
            project_config["nav"] = translate_nav(
                nav,
                lang,
                get_nav_section_names(),
            )
    config_path = lang_stage_path / zensical_name
    config_path.write_text(
        tomli_w.dumps(config),
        encoding="utf-8",
    )
    return config_path


def get_zensical_executable() -> Path:
    """Return the path to the executable Zensical binary."""
    executable = shutil.which("zensical")
    if executable is None:
        message = "Zensical executable was not found on PATH"
        raise FileNotFoundError(message)
    return Path(executable)


def build_zensical_config(config_path: Path) -> None:
    """Build the generated documentation site for the provided Zensical config."""
    subprocess.run(  # noqa: S603 - executable is resolved from PATH and arguments are validated
        [get_zensical_executable(), "build", "--config-file", config_path.absolute()],
        check=True,
        cwd=config_path.parent,
        shell=False,
    )


def build_zensical_lang_to_stage(lang: str) -> Path:
    """Stage a translated docs site by generating and building a language config."""
    typer.echo(f"Building Zensical docs for: {lang}")
    config_path = stage_zensical_docs(lang)
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    build_site_dist_path = Path(config_path.parent / config["project"]["site_dir"])
    shutil.rmtree(build_site_dist_path, ignore_errors=True)
    build_zensical_config(config_path)
    return build_site_dist_path


def copy_zensical_stage_to_site(lang: str) -> None:
    """Copy built language docs from staging into the final site tree."""
    build_site_dist_path = zensical_src_path / lang / "site"
    if lang == "ja":
        dist_path = site_path
    else:
        dist_path = site_path / lang
        shutil.rmtree(dist_path, ignore_errors=True)
    shutil.copytree(
        build_site_dist_path,
        dist_path,
        dirs_exist_ok=True,
    )


@app.command()
def build_all() -> None:
    """Build the full translated docs site into ./site/."""
    update_languages()
    shutil.rmtree(site_path, ignore_errors=True)
    shutil.rmtree(zensical_src_path, ignore_errors=True)
    langs = [
        lang.name
        for lang in get_lang_paths()
        if (lang.is_dir() and lang.name in SUPPORTED_LANGS)
    ]
    process_pool_size = min(4, len(langs), os.cpu_count() or 1)
    typer.echo(f"Using process pool size: {process_pool_size}")
    with Pool(process_pool_size) as p:
        p.map(build_zensical_lang_to_stage, langs)
    if "ja" in langs:
        copy_zensical_stage_to_site("ja")
    for lang in langs:
        if lang != "ja":
            copy_zensical_stage_to_site(lang)
    typer.secho("Successfully built all docs", fg=typer.colors.GREEN)


def update_alternate_languages(
    config_text: str,
    alternate: list[dict[str, str]],
) -> str:
    """Update only the alternate array while preserving the rest of the TOML."""
    if not alternate:
        alternate_text = "alternate = []"
    else:
        alternate_items = []
        for item in alternate:
            values = ", ".join(
                f"{key} = {tomli_w.dumps({key: value}).split('=', 1)[1].strip()}"
                for key, value in item.items()
            )
            alternate_items.append(f"{{ {values} }},")
        alternate_text = (
            "alternate = [\n"
            + "\n".join(f"    {item}" for item in alternate_items)
            + "\n]"
        )
    alternate_pattern = re.compile(
        r"^alternate\s*=\s*\[\n.*?^\](?=\n)",
        re.MULTILINE | re.DOTALL,
    )
    matches: list[re.Match[str]] = list(alternate_pattern.finditer(config_text))
    if len(matches) != 1:
        message = "Expected exactly one alternate array in the config"
        raise ValueError(message)
    match = matches[0]
    return config_text[: match.start()] + alternate_text + config_text[match.end() :]


@app.command()
def update_languages() -> None:
    """Update the docs config Languages section.

    Includes all the available languages.
    """
    old_config = get_ja_config()
    updated_config = get_updated_config_content()
    if old_config != updated_config:
        typer.echo("docs/ja/zensical.toml outdated")
        typer.echo("Updating docs/ja/zensical.toml")
        alternate = updated_config["project"]["extra"]["alternate"]
        config_text = ja_config_path.read_text(encoding="utf-8")
        ja_config_path.write_text(
            update_alternate_languages(config_text, alternate),
            encoding="utf-8",
        )
        raise typer.Exit(1)
    typer.echo("docs/ja/zensical.toml is up to date ✅")


@app.command()
def serve() -> None:
    """Serve a quick preview of a built site with translations.

    For development, prefer the command live.

    This is here only to preview a site with translations already built.

    Make sure you run the build-all command first.
    """
    typer.echo("Warning: this is a very simple server.")
    typer.echo(
        "For development, use the command live instead.",
    )
    typer.echo("This is here only to preview a site with translations already built.")
    typer.echo("Make sure you run the build-all command first.")
    os.chdir("site")
    server_address = ("127.0.0.1", 8008)
    server = HTTPServer(server_address, SimpleHTTPRequestHandler)
    typer.echo("Serving at: http://127.0.0.1:8008")
    server.serve_forever()


@app.command()
def live() -> None:
    """Serve the Japanese docs with live reload from the source files."""
    executable = get_zensical_executable()
    if not executable.is_file():
        message = "The Zensical executable could not be found."
        raise RuntimeError(message)
    subprocess.run(  # noqa: S603 - executable is validated and arguments are fixed
        [  # nosec S607
            executable,
            "serve",
            "--config-file",
            zensical_name,
            "--dev-addr",
            "127.0.0.1:8008",
        ],
        cwd=ja_docs_path,
        check=True,
        shell=False,
    )


def get_updated_config_content() -> dict[str, Any]:
    """Return the Japanese Zensical config with the alternate language links added."""
    config = get_ja_config()
    # Alternate links are root-relative so local previews stay on the local
    # site instead of jumping to the deployed production docs.
    languages = [{"ja": "/"}]
    new_alternate: list[dict[str, str]] = []
    #
    # Language names sourced from https://quickref.me/iso-639-1
    # Contributors may wish to update or change these, e.g. to fix capitalization.
    language_names_path = Path(docs_path, "language_names.yml")
    local_language_names: dict[str, str] = yaml.safe_load(
        language_names_path.read_text(encoding="utf-8"),
    )
    for lang_path in get_lang_paths():
        if lang_path.name == "ja" or not lang_path.is_dir():
            continue
        if lang_path.name not in SUPPORTED_LANGS:
            # Skip languages that are not yet ready
            continue
        code = lang_path.name
        languages.append({code: f"/{code}/"})
    for lang_dict in languages:
        code = next(iter(lang_dict.keys()))
        url = lang_dict[code]
        if code not in local_language_names:
            typer.echo(
                f"Missing language name for: {code}, "
                "update it in docs/language_names.yml",
            )
            raise typer.Abort
        use_name = f"{code} - {local_language_names[code]}"
        new_alternate.append({"name": use_name, "link": url, "lang": code})
    config["project"]["extra"]["alternate"] = new_alternate
    return config


@app.command()
def ensure_non_translated() -> None:
    """Ensure there are no files in the non translatable pages."""
    typer.echo("Ensuring no non translated pages")
    lang_paths = get_lang_paths()
    error_paths = []
    for lang in lang_paths:
        if lang.name == "ja":
            continue
        for non_translatable in non_translated_sections:
            non_translatable_path = lang / "docs" / non_translatable
            if non_translatable_path.exists():
                error_paths.append(non_translatable_path)
    if error_paths:
        typer.echo("Non-translated pages found, removing them:")
        for error_path in error_paths:
            typer.echo(error_path)
            if error_path.is_file():
                error_path.unlink()
            else:
                shutil.rmtree(error_path)
        raise typer.Exit(1)
    typer.echo("No non-translated pages found ✅")


@app.command()
def langs_json() -> None:
    """Output the supported languages that have corresponding directories."""
    langs = [
        lang_path.name
        for lang_path in get_lang_paths()
        if lang_path.is_dir() and lang_path.name in SUPPORTED_LANGS
    ]
    typer.echo(json.dumps(langs))


def _update_code_block_state(
    line: str,
    *,
    in_code_block3: bool,
    in_code_block4: bool,
) -> tuple[bool, bool]:
    if in_code_block4:
        return False, not code_block4_pattern.match(line)
    if in_code_block3:
        return not code_block3_pattern.match(line), False
    if code_block4_pattern.match(line):
        return False, True
    return code_block3_pattern.match(line) is not None, False


def _detect_fence(line: str) -> tuple[str, int] | None:
    """Return the fence character and length for a Markdown code fence."""
    stripped = line.lstrip()
    if not stripped:
        return None
    first_char = stripped[0]
    if first_char not in {"`", "~"}:
        return None
    fence_length = len(stripped) - len(stripped.lstrip(first_char))
    if fence_length >= minimum_fence_length:
        return first_char, fence_length
    return None


def _make_permalink_line(
    line: str,
    *,
    update_existing: bool,
    visible_text_extractor: VisibleTextExtractor,
    permalinks: set[str],
) -> str:
    match = header_pattern.match(line)
    if not match:
        return line

    hashes, title, existing_permalink = match.groups()
    if existing_permalink and not update_existing:
        permalinks.add(existing_permalink.strip().removeprefix("#"))
        return line

    slug = slugify(
        visible_text_extractor.extract_visible_text(strip_markdown_links(title)),
    )
    original_slug = slug
    count = 1
    while slug in permalinks:
        slug = f"{original_slug}_{count}"
        count += 1
    permalinks.add(slug)
    return f"{hashes} {title} {{ #{slug} }}\n"


@app.command()
def add_permalinks_page(path: Path, *, update_existing: bool = False) -> None:
    """Add or update header permalinks in specific page of En docs."""
    docs_root = (en_docs_path / "docs").resolve()
    path = path.resolve()
    if not path.is_relative_to(docs_root):
        message = f"Path must be inside {docs_root}"
        raise RuntimeError(message)
    rel_path = path.relative_to(docs_root)
    if rel_path.as_posix().startswith(non_translated_sections):
        return

    visible_text_extractor = VisibleTextExtractor()
    permalinks: set[str] = set()
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines: list[str] = []
    in_fence: tuple[str, int] | None = None
    for current_line in lines:
        fence = _detect_fence(current_line)
        if in_fence is not None:
            if (
                fence is not None
                and fence[0] == in_fence[0]
                and fence[1] >= in_fence[1]
            ):
                in_fence = None
            updated_lines.append(current_line)
            continue
        if fence is not None:
            in_fence = fence
            updated_lines.append(current_line)
            continue
        updated_lines.append(
            _make_permalink_line(
                current_line,
                update_existing=update_existing,
                visible_text_extractor=visible_text_extractor,
                permalinks=permalinks,
            ),
        )

    with path.open("w", encoding="utf-8") as f:
        f.writelines(updated_lines)


@app.command()
def add_permalinks_pages(
    pages: list[Path],
    *,
    update_existing: bool = typer.Option(
        default=False,
        help="Update existing permalinks.",
    ),
) -> None:
    """Add or update header permalinks in specific pages of English docs."""
    for md_file in pages:
        add_permalinks_page(md_file, update_existing=update_existing)


@app.command()
def add_permalinks(
    *,
    update_existing: bool = typer.Option(
        default=False,
        help="Update existing permalinks.",
    ),
) -> None:
    """Add or update header permalinks in all pages of En docs."""
    for md_file in en_docs_path.rglob("*.md"):
        add_permalinks_page(md_file, update_existing=update_existing)


if __name__ == "__main__":
    app()
