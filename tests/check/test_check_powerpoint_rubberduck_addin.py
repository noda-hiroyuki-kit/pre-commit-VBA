# Copyright (c) 2026 Noda Hiroyuki
"""Tests for PowerPoint Rubberduck Addin reference detection in check command."""

from pathlib import Path
from unittest import mock

from typer.testing import CliRunner

from src.pre_commit_vba import pre_commit_vba
from src.pre_commit_vba.pre_commit_vba import (
    app,
    has_rubberduck_addin_references,
)

runner = CliRunner()

RUBBERDUCK_PRESENTATION = Path(
    Path.cwd(),
    "tests",
    "powerpoint",
    "check",
    "withRubberduck",
    "withRubberduck.pptm",
)
NORMAL_PRESENTATION = Path(
    Path.cwd(),
    "tests",
    "powerpoint",
    "check",
    "withoutRubberduck",
    "withoutRubberduck.pptm",
)
WITHOUT_ACTIVE_RUBBERDUCK_PRESENTATION = Path(
    Path.cwd(),
    "tests",
    "powerpoint",
    "check",
    "withoutActiveRubberduckReference",
    "withoutActiveRubberduckReference.pptm",
)
CHECK_DIR_WITH_RUBBERDUCK = Path("tests", "powerpoint", "check", "withRubberduck")
CHECK_DIR_WITHOUT_RUBBERDUCK = Path(
    "tests",
    "powerpoint",
    "check",
    "withoutRubberduck",
)
CHECK_DIR_WITHOUT_ACTIVE_RUBBERDUCK = Path(
    "tests",
    "powerpoint",
    "check",
    "withoutActiveRubberduckReference",
)


class TestHasRubberduckAddinReferences:
    """Tests for has_rubberduck_addin_references function."""

    def test_returns_true_for_presentation_with_rubberduck_reference(self) -> None:
        """Test returns True when presentation has Rubberduck Addin reference."""
        sut = has_rubberduck_addin_references(RUBBERDUCK_PRESENTATION)
        assert sut is True  # noqa: S101

    def test_returns_false_for_presentation_without_rubberduck_reference(self) -> None:
        """Test returns False when presentation has no Rubberduck Addin reference."""
        sut = has_rubberduck_addin_references(NORMAL_PRESENTATION)
        assert sut is False  # noqa: S101

    def test_returns_false_for_presentation_without_active_rubberduck_reference(
        self,
    ) -> None:
        """Test returns False when presentation has no active Rubberduck reference."""
        sut = has_rubberduck_addin_references(WITHOUT_ACTIVE_RUBBERDUCK_PRESENTATION)
        assert sut is False  # noqa: S101


class TestCheckCommandRubberduckAddin:
    """Tests for check command Rubberduck Addin reference detection."""

    def test_check_exits_nonzero_when_presentation_with_rubberduck_addin_referenced(
        self,
    ) -> None:
        """Test check command exits 1 when Rubberduck Addin reference is detected."""
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "get_office_file_version",
                return_value="v0.0.1-alpha",
            ),
        ):
            result = runner.invoke(
                app,
                ["check", f"--target-path={CHECK_DIR_WITH_RUBBERDUCK}"],
            )
        assert result.exit_code == 1  # noqa: S101

    def test_check_exits_zero_when_presentation_without_rubberduck_addin_referenced(
        self,
    ) -> None:
        """Test check command exits 0 for a presentation without any reference."""
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "get_office_file_version",
                return_value="v0.0.1-alpha",
            ),
        ):
            result = runner.invoke(
                app,
                ["check", f"--target-path={CHECK_DIR_WITHOUT_RUBBERDUCK}"],
            )
        assert result.exit_code == 0  # noqa: S101

    def test_check_exits_zero_when_presentation_without_active_rubberduck_referenced(
        self,
    ) -> None:
        """Test check command exits 0 for inactive Rubberduck Addin.

        This covers the presentation with no active reference.
        """
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "get_office_file_version",
                return_value="v0.0.1-alpha",
            ),
        ):
            result = runner.invoke(
                app,
                ["check", f"--target-path={CHECK_DIR_WITHOUT_ACTIVE_RUBBERDUCK}"],
            )
        assert result.exit_code == 0  # noqa: S101
