"""Test module for pre-commit-vba script."""

from logging import INFO
from pathlib import Path

from typer.testing import CliRunner

from pre_commit_vba import app, extract

runner = CliRunner()


def test_extract_function_exists() -> None:
    """Test that the extract function exists in pre_commit_vba module."""
    assert callable(extract)  # noqa: S101


def test_extract_command_execution(caplog) -> None:  # noqa: ANN001
    """Test that the extract command executes without errors."""
    caplog.set_level(INFO)
    result = runner.invoke(app, ["extract"])
    assert result.exit_code == 0  # noqa: S101
    assert "Hello from pre-commit-vba!" in caplog.text  # noqa: S101


def test_extract_command_with_target_path_argument(caplog) -> None:  # noqa: ANN001
    """Test that the extract command executes without errors."""
    caplog.set_level(INFO)
    result = runner.invoke(app, ["extract", "--target-path", "."])
    assert result.exit_code == 0  # noqa: S101
    assert f"{Path.cwd()}".lower() in caplog.text  # noqa: S101
