"""Zensical macros for syncing docs version with pyproject metadata."""

import tomllib
from pathlib import Path
from typing import Protocol


class MissingProjectSectionError(RuntimeError):
    """Raised when pyproject.toml does not contain a [project] section."""

    def __init__(self) -> None:
        """Initialize with a clear missing-project-section message."""
        super().__init__("[project] section is missing in pyproject.toml")


class InvalidProjectVersionError(RuntimeError):
    """Raised when [project].version is missing or not a string."""

    def __init__(self) -> None:
        """Initialize with a clear invalid-version message."""
        super().__init__("[project].version must be a string in pyproject.toml")


class MacrosEnv(Protocol):
    """Minimal interface required by define_env."""

    variables: dict[str, str]


def define_env(env: MacrosEnv) -> None:
    """Define variables and macros."""
    pyproject = Path(__file__).resolve().parent / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))

    project = data.get("project")
    if not isinstance(project, dict):
        raise MissingProjectSectionError

    version = project.get("version")
    if not isinstance(version, str):
        raise InvalidProjectVersionError

    env.variables["project_version"] = version
