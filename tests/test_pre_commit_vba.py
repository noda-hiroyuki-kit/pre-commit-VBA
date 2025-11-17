"""Test module for pre-commit-vba script."""

from logging import INFO

from typer.testing import CliRunner

from pre_commit_vba import app, main

runner = CliRunner()


def test_main_function_exists() -> None:
    """Test that the main function exists in pre_commit_vba module."""
    assert callable(main)  # noqa: S101


def test_main_command_execution(caplog) -> None:  # noqa: ANN001
    """Test that the main command executes without errors."""
    caplog.set_level(INFO)
    result = runner.invoke(app)
    assert result.exit_code == 0  # noqa: S101
    assert "Hello from pre-commit-vba!" in caplog.text  # noqa: S101
