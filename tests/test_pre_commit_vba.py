"""Test module for pre-commit-vba script."""

from logging import INFO

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
