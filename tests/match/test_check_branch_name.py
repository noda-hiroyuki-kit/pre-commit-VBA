"""Check branch name tests for pre-commit-vba."""

from pre_commit_vba import get_current_branch_name


def test_get_current_branch_name() -> None:
    """Test get current branch name."""
    sut = get_current_branch_name()
    assert sut == "feature/add-match-subcommand"  # noqa: S101
