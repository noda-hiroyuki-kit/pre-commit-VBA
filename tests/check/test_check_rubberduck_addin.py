"""Tests for Rubberduck Addin reference detection in check command."""

from pathlib import Path
from unittest import mock

from typer.testing import CliRunner

from src.pre_commit_vba import pre_commit_vba
from src.pre_commit_vba.pre_commit_vba import (
    app,
    has_rubberduck_addin_references,
)

runner = CliRunner()

RUBBERDUCK_WORKBOOK = Path(
    Path.cwd(), "tests", "check", "withRubberduck", "WithRubberduckAddinReferences.xlsm"
)
NORMAL_WORKBOOK = Path(
    Path.cwd(),
    "tests",
    "check",
    "withoutRubberduck",
    "WithoutRubberduckAddinReferences.xlsm",
)
CHECK_DIR_WITH_RUBBERDUCK = Path("tests", "check", "withRubberduck")
CHECK_DIR_WITHOUT_RUBBERDUCK = Path("tests", "check", "withoutRubberduck")


class TestHasRubberduckAddinReferences:
    """Tests for has_rubberduck_addin_references function."""

    def test_returns_true_for_workbook_with_rubberduck_reference(self) -> None:
        """Test returns True when workbook has Rubberduck Addin reference."""
        sut = has_rubberduck_addin_references(RUBBERDUCK_WORKBOOK)
        assert sut is True  # noqa: S101

    def test_returns_false_for_workbook_without_rubberduck_reference(self) -> None:
        """Test returns False when workbook has no Rubberduck Addin reference."""
        sut = has_rubberduck_addin_references(NORMAL_WORKBOOK)
        assert sut is False  # noqa: S101


class TestCheckCommandRubberduckAddin:
    """Tests for check command Rubberduck Addin reference detection."""

    def test_check_exits_nonzero_when_rubberduck_addin_referenced(self) -> None:
        """Test check command exits 1 when Rubberduck Addin reference is detected."""
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "get_workbook_version",
                return_value="v0.0.1-alpha",
            ),
        ):
            result = runner.invoke(
                app,
                ["check", f"--target-path={CHECK_DIR_WITH_RUBBERDUCK}"],
            )
        assert result.exit_code == 1  # noqa: S101

    def test_check_exits_zero_when_no_rubberduck_addin_referenced(self) -> None:
        """Test check command exits 0 when no Rubberduck Addin reference is detected."""
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "get_workbook_version",
                return_value="v0.0.1-alpha",
            ),
        ):
            result = runner.invoke(
                app,
                ["check", f"--target-path={CHECK_DIR_WITHOUT_RUBBERDUCK}"],
            )
        assert result.exit_code == 0  # noqa: S101
