"""Check branch name tests for pre-commit-vba."""

from pathlib import Path

from pre_commit_vba import get_current_branch_name, get_workbook_version


def test_get_current_branch_name() -> None:
    """Test get current branch name."""
    sut = get_current_branch_name()
    assert sut == "feature/add-match-subcommand"  # noqa: S101


def test_get_workbook_version() -> None:
    """Test get workbook version."""
    sut = get_workbook_version(Path(Path.cwd(), "tests", "test.xlsm"))
    assert sut == "v0.0.1-alpha"  # noqa: S101
