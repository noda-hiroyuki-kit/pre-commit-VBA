"""Part of the mkdocs-macros-plugin project."""

import tomllib
from pathlib import Path
from typing import Protocol


class MacrosEnv(Protocol):
    """Minimal interface required by define_env."""

    variables: dict[str, str]


def define_env(env: MacrosEnv) -> None:
    """Define variables and macros."""
    pyproject = Path("pyproject.toml")
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))

    project = data.get("project")
    if not isinstance(project, dict):
        msg = "[project] section is missing in pyproject.toml"
        raise KeyError(msg)

    version = project.get("version")
    if not isinstance(version, str):
        msg = "[project].version must be a string in pyproject.toml"
        raise TypeError(msg)

    env.variables["project_version"] = version
