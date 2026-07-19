"""Test module for pre-commit-vba script."""

import csv
import logging
import multiprocessing
import re
import shutil
import subprocess
import tempfile
import tomllib
import typing
from collections.abc import Generator
from contextlib import suppress
from logging import DEBUG
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock

import pytest
from typer.testing import CliRunner

from src.pre_commit_vba import pre_commit_vba
from src.pre_commit_vba.pre_commit_vba import app

if TYPE_CHECKING:
    from collections.abc import Generator

from win32com.client import DispatchEx

runner = CliRunner()


def _project_version() -> str:
    """Read the project version from pyproject.toml."""
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject_file:
        return str(tomllib.load(pyproject_file)["project"]["version"])


def _run_extract_issue107_with_cli_runner(
    target_path: str,
    result_queue: multiprocessing.Queue,
) -> None:
    """Execute extract command through CliRunner and pass result to parent."""
    result = runner.invoke(
        app,
        [
            "extract",
            "--target-path",
            target_path,
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
    result_queue.put((result.exit_code, result.output))


def _get_excel_process_ids() -> set[int]:
    """Return running EXCEL.EXE process IDs."""
    process = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq EXCEL.EXE", "/FO", "CSV", "/NH"],  # noqa: S607
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        return set()

    process_ids: set[int] = set()
    for line in process.stdout.splitlines():
        if not line.strip() or line.startswith("INFO:"):
            continue
        row = next(csv.reader([line]), [])
        with suppress(IndexError, ValueError):
            process_ids.add(int(row[1]))
    return process_ids


def _terminate_excel_processes(process_ids: set[int]) -> None:
    """Terminate specific EXCEL.EXE process IDs."""
    for process_id in process_ids:
        subprocess.run(  # noqa: S603
            ["taskkill", "/PID", str(process_id), "/T", "/F"],  # noqa: S607
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


class TestCodeMetadataPortionIsOkInTrailingWhitespaceCheck:
    """Test class for code metadata portion in trailing whitespace check."""

    @pytest.fixture(scope="class")
    @classmethod
    def set_up(cls) -> typing.tuple[subprocess.Popen, bytes]:
        """Set up for test."""
        runner.invoke(
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
        process = subprocess.Popen(
            [  # noqa: S607
                "uv",
                "run",
                "pre-commit",
                "run",
                "trailing-whitespace",
                "--files",
                "tests/test.xlsm.VBA/code/registerForm/RegisterProductForm.frm",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            stdout_data, _ = process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout_data, _ = process.communicate()
        return process, stdout_data

    def test_process_return_code_is_zero(
        self, set_up: typing.tuple[subprocess.Popen, bytes]
    ) -> None:
        """Test that the process return code is zero."""
        process, _ = set_up
        assert process.returncode == 0  # noqa: S101

    def test_stdout_contains_passed_message(
        self, set_up: typing.tuple[subprocess.Popen, bytes]
    ) -> None:
        """Test that the stdout contains 'Passed' message."""
        _, stdout_data = set_up
        pattern = r"trim trailing whitespace.*Passed"
        assert re.search(pattern, stdout_data.decode("utf-8")) is not None  # noqa: S101


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
    @classmethod
    def prepare_pre_existing_excel(cls) -> typing.tuple[DispatchEx, CliRunner]:
        """Fixture to prepare pre-existing Excel workbook for testing."""
        _excel_instance = DispatchEx("Excel.Application")
        _excel_instance.Visible = False
        _excel_instance.DisplayAlerts = False
        _workbook = _excel_instance.Workbooks.Open(
            Path(Path.cwd(), "tests", "test.xlsm"),
            ReadOnly=True,
        )
        sut = cls.sut()
        yield _excel_instance, sut
        _workbook.Close(SaveChanges=False)
        _excel_instance.Quit()

    @classmethod
    def sut(cls) -> CliRunner:
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
        assert Path(Path.cwd(), "tests", "test.xlsm.VBA", file).exists()  # noqa: S101

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


def test_not_exists_test1_vba_folder() -> None:
    """Test that the test1.VBA folder does not exist."""
    if Path(Path.cwd(), "tests", "test1.VBA").exists():
        shutil.rmtree(Path(Path.cwd(), "tests", "test1.VBA"))
    runner.invoke(
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
    test_result = not Path(Path.cwd(), "tests", "test1.VBA").exists()
    if Path(Path.cwd(), "tests", "test1.VBA").exists():
        shutil.rmtree(Path(Path.cwd(), "tests", "test1.VBA"))
    assert test_result  # noqa: S101


def test_extract_command_does_not_timeout_on_issue107_repro_workbook() -> None:
    """Issue107: extract command should not block on Workbook_Open macro."""
    repro_workbook = Path(
        Path.cwd(),
        "tests",
        "fixtures",
        "issue107",
        "Issue107_Repro_WorkbookOpen_MsgBox.xlsm",
    )
    assert repro_workbook.exists()  # noqa: S101

    temp_root = Path(tempfile.mkdtemp(prefix="issue107-", dir=Path.cwd() / "tests"))
    target_workbook = Path(temp_root, repro_workbook.name)
    extracted_this_workbook = Path(
        temp_root,
        f"{repro_workbook.name}.VBA",
        "export",
        "ThisWorkbook.cls",
    )
    git_path = shutil.which("git")
    assert git_path is not None  # noqa: S101
    excel_process_ids_before = _get_excel_process_ids()

    process = None
    result_queue = multiprocessing.Queue()
    try:
        shutil.copy2(repro_workbook, target_workbook)
        process = multiprocessing.Process(
            target=_run_extract_issue107_with_cli_runner,
            args=(str(temp_root), result_queue),
        )
        process.start()
        process.join(timeout=15)

        if process.is_alive():
            process.terminate()
            process.join(timeout=5)
            pytest.fail("extract command timed out for Issue107 repro workbook")

        assert process.exitcode == 0  # noqa: S101
        assert not result_queue.empty()  # noqa: S101
        exit_code, output = result_queue.get()
        assert exit_code == 0, output  # noqa: S101
        assert extracted_this_workbook.is_file()  # noqa: S101
    finally:
        relative_temp_root = temp_root.relative_to(Path.cwd())
        subprocess.run(  # noqa: S603
            [git_path, "reset", "--quiet", "HEAD", "--", str(relative_temp_root)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=Path.cwd(),
        )
        if process is not None and process.is_alive():
            process.terminate()
            process.join(timeout=5)
        _terminate_excel_processes(_get_excel_process_ids() - excel_process_ids_before)
        shutil.rmtree(temp_root, ignore_errors=True)


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


def test_runtime_version_matches_pyproject() -> None:
    """Test that the runtime version matches pyproject.toml."""
    assert pre_commit_vba.__version__ == _project_version()  # noqa: S101


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
    assert match.group(1) == pre_commit_vba.__version__  # noqa: S101
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

    @pytest.fixture(scope="class")
    @classmethod
    def prepare_pre_existing_excel(cls) -> Generator:
        """Fixture to prepare pre-existing Excel workbook for testing."""
        _excel_instance = DispatchEx("Excel.Application")
        _excel_instance.Visible = False
        _excel_instance.DisplayAlerts = False
        _workbook = _excel_instance.Workbooks.Open(
            Path(Path.cwd(), "tests", "test.xlsm"),
            ReadOnly=True,
        )
        yield
        _workbook.Close(SaveChanges=False)
        _excel_instance.Quit()

    def test_not_exist_workbook_outs_no_found(
        self, caplog: Generator[pytest.LogCaptureFixture]
    ) -> None:
        """Test not exist workbook in target path."""
        caplog.set_level(logging.INFO)
        with mock.patch.object(
            pre_commit_vba,
            "get_current_branch_name",
            return_value="release/v0.0.1-alpha",
        ):
            sut = runner.invoke(app, ["check"])
            assert sut.exit_code == 0  # noqa: S101
            assert (  # noqa: S101
                "No Excel workbooks found in the target path." in caplog.text
            )

    def test_not_a_release_or_hotfix_branch_outs_in_feature_branch(
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
            assert "Branch is not a release or hotfix branch" in caplog.text  # noqa: S101

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
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "has_rubberduck_addin_references",
                return_value=False,
            ),
        ):
            sut = runner.invoke(app, ["check", "--target-path", "tests"])
            assert sut.exit_code == 0  # noqa: S101
            assert "Version check passed." in caplog.text  # noqa: S101

    def test_branch_release_v_0_0_1_alpha_outs_version_check_passed_with_temp_xl_file(
        self,
        caplog: Generator[pytest.LogCaptureFixture],
        prepare_pre_existing_excel: None,  # noqa: ARG002
    ) -> None:
        """Test check ok under the presence of temporary Excel files."""
        caplog.set_level(logging.INFO)
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="release/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "has_rubberduck_addin_references",
                return_value=False,
            ),
        ):
            sut = runner.invoke(app, ["check", "--target-path", "tests"])
            assert sut.exit_code == 0  # noqa: S101
            assert "Version check passed." in caplog.text  # noqa: S101

    def test_branch_hotfix_v_0_0_1_alpha_outs_version_check_passed(
        self, caplog: Generator[pytest.LogCaptureFixture]
    ) -> None:
        """Test check ok."""
        caplog.set_level(logging.INFO)
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_current_branch_name",
                return_value="hotfix/v0.0.1-alpha",
            ),
            mock.patch.object(
                pre_commit_vba,
                "has_rubberduck_addin_references",
                return_value=False,
            ),
        ):
            sut = runner.invoke(app, ["check", "--target-path", "tests"])
            assert sut.exit_code == 0  # noqa: S101
            assert "Version check passed." in caplog.text  # noqa: S101
