"""Test module for pre-commit-vba script."""

import logging
import re
import typing
from collections.abc import Generator
from logging import DEBUG
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock

import pytest
from typer.testing import CliRunner

import pre_commit_vba
from pre_commit_vba import app

if TYPE_CHECKING:
    from collections.abc import Generator

from win32com.client import DispatchEx

runner = CliRunner()


class TestExtractCommandPositiveOptions:
    """Test class for extract command."""

    def extract_command_fixture(self, caplog) -> CliRunner:  # noqa: ANN001
        """Test that the extract command executes without errors."""
        caplog.set_level(DEBUG)
        return runner.invoke(
            app,
            [
                "extract",
                "--target-path",
                ".",
                "--folder-suffix",
                ".VBA",
                "--export-folder",
                "export",
                "--custom-ui-folder",
                "customUI",
                "--code-folder",
                "code",
                "--enable-folder-annotation",
                "--create-gitignore",
            ],
        )

    def test_target_path_is_current_directory(self, caplog) -> None:  # noqa: ANN001
        """Test that target_path is current directory."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert f"{Path.cwd()}".lower() in caplog.text  # noqa: S101

    def test_folder_suffix_is_vba(self, caplog) -> None:  # noqa: ANN001
        """Test that folder suffix is '.VBA'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "folder-suffix: .VBA" in caplog.text  # noqa: S101

    def test_export_folder_is_export(self, caplog) -> None:  # noqa: ANN001
        """Test that export folder is 'export'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "export-folder: export" in caplog.text  # noqa: S101

    def test_custom_ui_folder_is_custom_ui(self, caplog) -> None:  # noqa: ANN001
        """Test that custom ui folder is 'customUI'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "custom-ui-folder: customUI" in caplog.text  # noqa: S101

    def test_code_folder_is_code(self, caplog) -> None:  # noqa: ANN001
        """Test that code folder is 'code'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "code-folder: code" in caplog.text  # noqa: S101

    def test_enable_folder_annotation_is_true(self, caplog) -> None:  # noqa: ANN001
        """Test that enable-folder-annotation is True."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "enable-folder-annotation: True" in caplog.text  # noqa: S101

    def test_create_gitignore_is_true(self, caplog) -> None:  # noqa: ANN001
        """Test that create-gitignore is True."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "create-gitignore: True" in caplog.text  # noqa: S101


class TestExtractCommandExistenceFiles:
    """Test class for extract command."""

    @pytest.fixture(scope="class")
    def prepare_pre_existing_excel(self) -> typing.tuple[DispatchEx, CliRunner]:
        """Fixture to prepare pre-existing Excel workbook for testing."""
        _excel_instance = DispatchEx("Excel.Application")
        _excel_instance.Visible = False
        _excel_instance.DisplayAlerts = False
        _workbook = _excel_instance.Workbooks.Open(
            Path(Path.cwd(), "tests", "test.xlsm"),
            ReadOnly=True,
        )
        sut = self.sut()
        yield _excel_instance, sut
        _workbook.Close(SaveChanges=False)
        _excel_instance.Quit()

    def sut(self) -> CliRunner:
        """Fixture for TestExtractCommandExistenceFiles."""
        return runner.invoke(
            app,
            [
                "extract",
                "--target-path",
                "tests",
                "--folder-suffix",
                ".VBA",
                "--export-folder",
                "export",
                "--custom-ui-folder",
                "customUI",
                "--code-folder",
                "code",
                "--enable-folder-annotation",
                "--create-gitignore",
            ],
        )

    @pytest.mark.parametrize(
        "file",
        [
            f"{Path('.gitignore')}",
            f"{Path('export', 'Sheet1.cls')}",
            f"{Path('export', 'ThisWorkbook.cls')}",
            f"{Path('export', 'CustomUI.bas')}",
            f"{Path('export', 'SampleTab.bas')}",
            f"{Path('export', 'upperFolderQuotation.bas')}",
            f"{Path('export', 'upperFolderParentheses.bas')}",
            f"{Path('export', 'lowerFolderParentheses.bas')}",
            f"{Path('export', 'lowerFolderQuotation.bas')}",
            f"{Path('customUI', 'customUI14.xml')}",
            f"{Path('code', 'excel document modules', 'ブック', 'ThisWorkbook.cls')}",
            f"{Path('code', 'excel document modules', 'シート', 'Sheet1.cls')}",
            f"{Path('code', 'customUI', 'CustomUI.bas')}",
            f"{Path('code', 'customUI', 'sample_tab', 'SampleTab.bas')}",
            f"{Path('code', 'folder_annotation', 'upper', 'upperFolderQuotation.bas')}",
            f"{
                Path('code', 'folder_annotation', 'upper', 'upperFolderParentheses.bas')
            }",
            f"{
                Path('code', 'folder_annotation', 'lower', 'lowerFolderParentheses.bas')
            }",
            f"{Path('code', 'folder_annotation', 'lower', 'lowerFolderQuotation.bas')}",
            f"{Path('code', 'Tests', 'TestController.cls')}",
            f"{Path('code', 'Tests', 'domain', 'model', 'TestProductCodeModule.bas')}",
            f"{Path('code', 'domain', 'ErrorCode.cls')}",
            f"{Path('code', 'domain', 'ValidationResult.cls')}",
            f"{Path('code', 'domain', 'model', 'Product.cls')}",
            f"{Path('code', 'domain', 'model', 'ProductCode.cls')}",
            f"{Path('code', 'domain', 'model', 'ProductName.cls')}",
            f"{Path('code', 'registerForm', 'RegisterProductForm.frm')}",
            f"{Path('code', 'registerForm', 'ShowFormModule.bas')}",
            f"{Path('code', 'registerForm', 'IForm.cls')}",
        ],
    )
    def test_exists_file(
        self,
        prepare_pre_existing_excel: typing.tuple[DispatchEx, CliRunner],  # noqa: ARG002
        file: str,
    ) -> None:
        """Test that the extract command creates expected files and folders."""
        assert Path(Path.cwd(), "tests", "test.VBA", file).exists()  # noqa: S101

    def test_terminate_normal(
        self, prepare_pre_existing_excel: typing.tuple[DispatchEx, CliRunner]
    ) -> None:
        """Test that the extract command terminates normally."""
        _, sut = prepare_pre_existing_excel
        assert sut.exit_code == 0  # noqa: S101

    def test_exists_pre_existing_excel_instance(
        self, prepare_pre_existing_excel: typing.tuple[DispatchEx, CliRunner]
    ) -> None:
        """Test that the pre-existing Excel instance is not None."""
        excel_instance, _ = prepare_pre_existing_excel
        assert excel_instance is not None  # noqa: S101


class TestExtractCommandNegativeOptions:
    """Test class for extract command."""

    def extract_command_fixture(self, caplog) -> CliRunner:  # noqa: ANN001
        """Test that the extract command executes without errors."""
        caplog.set_level(DEBUG)
        return runner.invoke(
            app,
            [
                "extract",
                "--target-path",
                ".",
                "--folder-suffix",
                ".VBA",
                "--export-folder",
                "export",
                "--custom-ui-folder",
                "customUI",
                "--code-folder",
                "code",
                "--disable-folder-annotation",
                "--not-create-gitignore",
            ],
        )

    def test_enable_folder_annotation_is_false(self, caplog) -> None:  # noqa: ANN001
        """Test that enable-folder-annotation is False."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "enable-folder-annotation: False" in caplog.text  # noqa: S101

    def test_create_gitignore_is_false(self, caplog) -> None:  # noqa: ANN001
        """Test that create-gitignore is False."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "create-gitignore: False" in caplog.text  # noqa: S101


@pytest.mark.parametrize(
    "subcommand",
    [
        "extract",
        "check",
    ],
)
def test_display_version_subcommand(subcommand: str) -> None:
    """Test that the version is displayed correctly."""
    result = runner.invoke(
        app,
        [
            subcommand,
            "--version",
        ],
    )
    assert result.exit_code == 0  # noqa: S101
    text = result.output.rstrip()
    pattern = r"pre-commit-vba version: (.*)"
    match = re.search(pattern, text)
    assert match is not None, "Version string not found in output"  # noqa: S101
    sem_ver_pattern = (
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)"
        r"\.(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
        r"?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )
    assert re.match(sem_ver_pattern, match.group(1)) is not None, (  # noqa: S101
        "Version string is not in semantic versioning format"
    )


class TestCheckSubCommand:
    """Tests for check sub command."""

    def test_not_exist_workbook_outs_no_found(
        self, caplog: Generator[pytest.LogCaptureFixture]
    ) -> None:
        """Test not exist workbook in target path."""
        sut = runner.invoke(app, ["check"])
        assert sut.exit_code == 0  # noqa: S101
        assert (  # noqa: S101
            "No Excel workbooks found in the target path." in caplog.text
        )

    def test_not_a_release_branch_outs_in_feature_branch(
        self, caplog: Generator[pytest.LogCaptureFixture]
    ) -> None:
        """Test not release branch."""
        caplog.set_level(logging.INFO)
        with mock.patch.object(
            pre_commit_vba,
            "get_current_branch_name",
            return_value="feature/issue-1234",
        ):
            sut = runner.invoke(app, ["check", "--target-path", "tests"])
            assert sut.exit_code == 0  # noqa: S101
            assert "Not a release branch" in caplog.text  # noqa: S101

    def test_branch_release_v_0_0_1_0123_outs_invalid_semantic_version(
        self, caplog: Generator[pytest.LogCaptureFixture]
    ) -> None:
        """Test invalid semantic version in branch name."""
        caplog.set_level(logging.INFO)
        with mock.patch.object(
            pre_commit_vba,
            "get_current_branch_name",
            return_value="release/v0.0.1-0123",
        ):
            sut = runner.invoke(app, ["check", "--target-path", "tests"])
            assert sut.exit_code == 1  # noqa: S101
            assert "Invalid semantic version in branch name" in caplog.text  # noqa: S101

    def test_branch_release_v_0_0_1_alpha_outs_version_check_passed(
        self, caplog: Generator[pytest.LogCaptureFixture]
    ) -> None:
        """Test check ok."""
        caplog.set_level(logging.INFO)
        with mock.patch.object(
            pre_commit_vba,
            "get_current_branch_name",
            return_value="release/v0.0.1-alpha",
        ):
            sut = runner.invoke(app, ["check", "--target-path", "tests"])
            assert sut.exit_code == 0  # noqa: S101
            assert "Version check passed." in caplog.text  # noqa: S101
