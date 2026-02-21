"""Check branch name tests for pre-commit-vba."""

import re
from pathlib import Path
from unittest import mock

import pytest

from src.pre_commit_vba import pre_commit_vba
from src.pre_commit_vba.pre_commit_vba import (
    get_current_branch_name,
    get_version_from_branch_name,
    get_workbook_version,
)


def test_get_current_branch_name() -> None:
    """Test get current branch name."""
    sut = get_current_branch_name()
    result = re.match(r"(main|develop|feature|bugfix|release|hotfix|support)", sut)
    assert result is not None  # noqa: S101


def test_get_workbook_version() -> None:
    """Test get workbook version."""
    sut = get_workbook_version(Path(Path.cwd(), "tests", "test.xlsm"))
    assert sut == "v0.0.1-alpha"  # noqa: S101


class TestGetVersionFromBranchName:
    """Test class for get_version_from_branch_name."""

    def test_ok_to_release_v0_0_1_alpha(self) -> None:
        """Test get version from branch name. Ok to release v0.0.1-alpha."""
        with mock.patch.object(
            pre_commit_vba,
            "get_current_branch_name",
            return_value="release/v0.0.1-alpha",
        ):
            sut = get_version_from_branch_name()
            assert sut == "0.0.1-alpha"  # noqa: S101

    def test_raise_not_release_branch_to_feature_issue_1234(self) -> None:
        """Test get version from branch name.

        Not release branch to feature/issue-1234.
        """
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="feature/issue-1234",
            ),
            pytest.raises(pre_commit_vba.NotReleaseBranchError),
        ):
            get_version_from_branch_name()

    def test_raise_invalid_semver_to_release_v0_0_1_0123(self) -> None:
        """Test get version from branch name. Invalid semver to release v0.0.1-0123."""
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-0123",
            ),
            pytest.raises(pre_commit_vba.InvalidSemVerError),
        ):
            get_version_from_branch_name()
