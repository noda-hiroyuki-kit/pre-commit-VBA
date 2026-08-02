"""Test module for pre-commit-vba script."""

import csv
import importlib.util
import locale
import logging
import multiprocessing
import queue
import re
import runpy
import shutil
import subprocess
import tempfile
import tomllib
import typing
from collections.abc import Callable, Generator
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
    from collections.abc import Callable, Generator

try:
    from win32com.client import DispatchEx
except ModuleNotFoundError:
    DispatchEx = None

runner = CliRunner()


class TestWindowsOnlyImportError:
    """Tests for WindowsOnlyImportError message."""

    def test_message_is_windows_only_hint(self) -> None:
        """Error message should guide users to Windows/pywin32 setup."""
        error = pre_commit_vba.WindowsOnlyImportError()
        expected = (
            "pre-commit-vba requires pywin32 (Windows only). "
            "Install it on Windows or run this hook on a Windows runner."
        )
        assert str(error) == expected  # noqa: S101

    def test_get_dispatch_ex_raises_when_dispatch_ex_is_missing(self) -> None:
        """get_dispatch_ex should raise when pywin32 import is unavailable."""
        with (
            mock.patch.object(pre_commit_vba, "DispatchEx", None),
            pytest.raises(pre_commit_vba.WindowsOnlyImportError),
        ):
            pre_commit_vba.get_dispatch_ex()

    def test_dispatch_ex_is_none_when_win32com_client_import_fails(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Module import fallback should set DispatchEx to None."""
        original_import = __import__

        def _patched_import(
            name: str,
            globals_dict: dict[str, object] | None = None,
            locals_dict: dict[str, object] | None = None,
            from_list: tuple[str, ...] = (),
            level: int = 0,
        ) -> object:
            if name == "win32com.client":
                raise ModuleNotFoundError(name)
            return original_import(name, globals_dict, locals_dict, from_list, level)

        monkeypatch.setattr("builtins.__import__", _patched_import)

        module_path = Path(pre_commit_vba.__file__)
        module_name = "_test_pre_commit_vba_missing_win32com"
        spec = importlib.util.spec_from_file_location(module_name, module_path)

        assert spec is not None  # noqa: S101
        assert spec.loader is not None  # noqa: S101

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert module.DispatchEx is None  # noqa: S101


class TestMainEntryPoint:
    """Tests for module main entry point behavior."""

    def test_module_main_invokes_app(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Running module as __main__ should call app()."""
        invoked = {"called": False}

        class _FakeTyperApp:
            def __init__(self, *_args: object, **_kwargs: object) -> None:
                pass

            def command(
                self,
                *_args: object,
                **_kwargs: object,
            ) -> Callable[[object], object]:
                def _decorator(func: object) -> object:
                    return func

                return _decorator

            def __call__(self) -> None:
                invoked["called"] = True

        module_path = Path(pre_commit_vba.__file__)
        monkeypatch.setattr("typer.Typer", _FakeTyperApp)

        runpy.run_path(str(module_path), run_name="__main__")

        assert invoked["called"] is True  # noqa: S101


class TestSettingsCommonFolder:
    """Tests for SettingsCommonFolder path generation."""

    def test_common_folder_uses_stem_when_include_extension_is_false(self) -> None:
        """When include_extension is False, extension should be excluded."""
        settings = pre_commit_vba.SettingsCommonFolder(
            Path("tests/sample.workbook.xlsm"),
            ".VBA",
            include_extension=False,
        )

        expected = Path("tests", "sample.VBA")
        assert settings.common_folder == expected  # noqa: S101


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


def _run_check_issue107_with_cli_runner(
    target_path: str,
    result_queue: multiprocessing.Queue,
) -> None:
    """Execute check command through CliRunner and pass result to parent."""
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
        result = runner.invoke(app, ["check", "--target-path", target_path])
    result_queue.put((result.exit_code, result.output))


def _get_excel_process_ids() -> set[int]:
    """Return running EXCEL.EXE process IDs."""
    try:
        process = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq EXCEL.EXE", "/FO", "CSV", "/NH"],  # noqa: S607
            check=False,
            capture_output=True,
        )
        if process.returncode != 0 or process.stdout is None:
            return set()
    except FileNotFoundError:
        return set()
    decoded_stdout = ""
    for encoding in (locale.getencoding(), "cp932", "utf-8"):
        with suppress(UnicodeDecodeError, LookupError):
            decoded_stdout = process.stdout.decode(encoding)
            break
    if not decoded_stdout:
        decoded_stdout = process.stdout.decode(errors="replace")

    process_ids: set[int] = set()
    for line in decoded_stdout.splitlines():
        if not line.strip() or line.startswith("INFO:"):
            continue
        row = next(csv.reader([line]), [])
        with suppress(IndexError, ValueError):
            process_ids.add(int(row[1]))
    return process_ids


def _terminate_excel_processes(process_ids: set[int]) -> None:
    """Terminate specific EXCEL.EXE process IDs."""
    for process_id in process_ids:
        try:
            subprocess.run(  # noqa: S603
                ["taskkill", "/PID", str(process_id), "/T", "/F"],  # noqa: S607
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            # taskkill unavailable (e.g., not on PATH)
            return


class TestExcelCleanupLogging:
    """Tests for debug logging during Excel cleanup failures."""

    def test_get_workbook_version_logs_cleanup_failures(self, caplog) -> None:  # noqa: ANN001
        """Cleanup failures should be logged without masking version retrieval."""
        caplog.set_level(logging.DEBUG)
        workbook = mock.Mock()
        workbook.BuiltinDocumentProperties.return_value = "0.3.11"
        workbook.Close.side_effect = OSError("close failed")

        excel_app = mock.Mock()
        excel_app.Workbooks.Open.return_value = workbook
        excel_app.Quit.side_effect = OSError("quit failed")

        with mock.patch.object(
            pre_commit_vba,
            "get_noninteractive_excel_app",
            return_value=excel_app,
        ):
            result = pre_commit_vba.get_workbook_version(Path("dummy.xlsm"))

        assert result == "0.3.11"  # noqa: S101
        assert "Failed to clean up Excel resource: workbook" in caplog.text  # noqa: S101
        assert "Failed to clean up Excel resource: application" in caplog.text  # noqa: S101

    def test_exporter_logs_cleanup_failures(self, tmp_path: Path, caplog) -> None:  # noqa: ANN001
        """Exporter cleanup failures should be traceable at debug level."""
        caplog.set_level(logging.DEBUG)
        workbook = mock.Mock()
        workbook.VBProject.VBComponents = []
        workbook.Close.side_effect = OSError("close failed")

        excel_app = mock.Mock()
        excel_app.Workbooks.Open.return_value = workbook
        excel_app.Quit.side_effect = OSError("quit failed")

        settings = pre_commit_vba.SettingsFoldersHandleExcel(
            pre_commit_vba.SettingsCommonFolder(tmp_path / "dummy.xlsm", ".VBA"),
            "export",
            "customUI",
            "code",
        )

        with mock.patch.object(
            pre_commit_vba,
            "get_noninteractive_excel_app",
            return_value=excel_app,
        ):
            pre_commit_vba.ExcelVbaExporter(settings)

        assert "Failed to clean up Excel resource: workbook" in caplog.text  # noqa: S101
        assert "Failed to clean up Excel resource: application" in caplog.text  # noqa: S101

    def test_get_workbook_version_swallows_non_com_cleanup_errors(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Non-COM cleanup errors should not alter command outcome."""
        caplog.set_level(logging.DEBUG)
        workbook = mock.Mock()
        workbook.BuiltinDocumentProperties.return_value = "0.3.11"
        workbook.Close.side_effect = AttributeError("close failed")

        excel_app = mock.Mock()
        excel_app.Workbooks.Open.return_value = workbook
        excel_app.Quit.side_effect = TypeError("quit failed")

        with mock.patch.object(
            pre_commit_vba,
            "get_noninteractive_excel_app",
            return_value=excel_app,
        ):
            result = pre_commit_vba.get_workbook_version(Path("dummy.xlsm"))

        assert result == "0.3.11"  # noqa: S101
        assert "Failed to clean up Excel resource: workbook" in caplog.text  # noqa: S101
        assert "Failed to clean up Excel resource: application" in caplog.text  # noqa: S101


class TestConfigureLogStreamEncoding:
    """Tests for stderr encoding configuration behavior."""

    def test_non_windows_platform_returns_without_reconfigure(self) -> None:
        """Non-Windows environments should not reconfigure stderr."""
        stderr = mock.Mock()
        stderr.reconfigure = mock.Mock()

        with (
            mock.patch.object(pre_commit_vba.sys, "platform", "linux"),
            mock.patch.object(pre_commit_vba.sys, "stderr", stderr),
        ):
            pre_commit_vba.configure_log_stream_encoding()

        stderr.reconfigure.assert_not_called()

    def test_none_stderr_returns_without_reconfigure(self) -> None:
        """Missing stderr stream should exit without attempting reconfigure."""
        with (
            mock.patch.object(pre_commit_vba.sys, "platform", "win32"),
            mock.patch.object(pre_commit_vba.sys, "stderr", None),
        ):
            pre_commit_vba.configure_log_stream_encoding()

    def test_reconfigure_skipped_for_tty_stderr(self) -> None:
        """Interactive terminals should keep their active code page."""
        stderr = mock.Mock()
        stderr.isatty.return_value = True
        stderr.reconfigure = mock.Mock()

        with (
            mock.patch.object(pre_commit_vba.sys, "platform", "win32"),
            mock.patch.object(pre_commit_vba.sys, "stderr", stderr),
        ):
            pre_commit_vba.configure_log_stream_encoding()

        stderr.reconfigure.assert_not_called()

    def test_non_callable_reconfigure_returns_without_error(self) -> None:
        """Non-callable reconfigure should short-circuit safely."""
        stderr = object()

        with (
            mock.patch.object(pre_commit_vba.sys, "platform", "win32"),
            mock.patch.object(pre_commit_vba.sys, "stderr", stderr),
        ):
            pre_commit_vba.configure_log_stream_encoding()

    def test_reconfigure_value_error_is_swallowed(self) -> None:
        """ValueError from reconfigure should be swallowed."""
        stderr = mock.Mock()
        stderr.isatty.return_value = False
        stderr.reconfigure = mock.Mock(side_effect=ValueError("bad encoding"))

        with (
            mock.patch.object(pre_commit_vba.sys, "platform", "win32"),
            mock.patch.object(pre_commit_vba.sys, "stderr", stderr),
        ):
            pre_commit_vba.configure_log_stream_encoding()

        stderr.reconfigure.assert_called_once_with(encoding="utf-8", errors="replace")

    def test_reconfigure_applied_for_non_tty_stderr(self) -> None:
        """Captured logs should be forced to UTF-8 on Windows."""
        stderr = mock.Mock()
        stderr.isatty.return_value = False
        stderr.reconfigure = mock.Mock()

        with (
            mock.patch.object(pre_commit_vba.sys, "platform", "win32"),
            mock.patch.object(pre_commit_vba.sys, "stderr", stderr),
        ):
            pre_commit_vba.configure_log_stream_encoding()

        stderr.reconfigure.assert_called_once_with(encoding="utf-8", errors="replace")


class TestAddToStaging:
    """Tests for add_to_staging helper."""

    def test_kills_process_when_git_add_times_out(self, tmp_path: Path) -> None:
        """Timeout during git add should trigger process.kill and retry communicate."""
        settings = pre_commit_vba.SettingsFoldersHandleExcel(
            pre_commit_vba.SettingsCommonFolder(tmp_path / "book.xlsm", ".VBA"),
            "export",
            "customUI",
            "code",
        )

        process = mock.Mock()
        process.communicate.side_effect = [
            subprocess.TimeoutExpired(cmd="git add", timeout=15),
            (b"", b""),
        ]
        process.returncode = 0

        with mock.patch.object(
            pre_commit_vba.subprocess,
            "Popen",
            return_value=process,
        ):
            pre_commit_vba.add_to_staging(settings)

        process.kill.assert_called_once_with()
        assert process.communicate.call_args_list == [  # noqa: S101
            mock.call(timeout=15),
            mock.call(),
        ]


class TestGetStagingStatus:
    """Tests for get_staging_status helper."""

    def test_kills_process_when_write_tree_times_out(self) -> None:
        """Timeout during git write-tree should trigger kill and retry communicate."""
        process = mock.Mock()
        process.communicate.side_effect = [
            subprocess.TimeoutExpired(cmd="git write-tree", timeout=15),
            (b"tree-id\n", b""),
        ]
        process.returncode = 0

        with mock.patch.object(
            pre_commit_vba.subprocess,
            "Popen",
            return_value=process,
        ):
            result = pre_commit_vba.get_staging_status()

        process.kill.assert_called_once_with()
        assert process.communicate.call_args_list == [  # noqa: S101
            mock.call(timeout=15),
            mock.call(),
        ]
        assert result == "tree-id\n"  # noqa: S101


class TestExtractCommandStagingStatus:
    """Tests for extract command staging-status failure handling."""

    def test_extract_exits_when_post_extract_staging_status_fails(self) -> None:
        """StagingStatusError after extraction should exit with code 1."""
        with (
            mock.patch.object(
                pre_commit_vba,
                "get_staging_status",
                side_effect=["before-tree", pre_commit_vba.StagingStatusError()],
            ) as get_status,
            mock.patch.object(Path, "glob", return_value=[]),
        ):
            result = runner.invoke(app, ["extract", "--target-path", "."])

        assert result.exit_code == 1  # noqa: S101
        assert get_status.call_args_list == [mock.call(), mock.call()]  # noqa: S101


class TestGetCurrentBranchName:
    """Tests for get_current_branch_name helper."""

    def test_kills_process_when_rev_parse_times_out(self) -> None:
        """Timeout during git rev-parse should trigger kill and retry."""
        process = mock.Mock()
        process.communicate.side_effect = [
            subprocess.TimeoutExpired(cmd="git rev-parse", timeout=15),
            (b"feature/test-branch\n", b""),
        ]

        with mock.patch.object(
            pre_commit_vba.subprocess,
            "Popen",
            return_value=process,
        ):
            result = pre_commit_vba.get_current_branch_name()

        process.kill.assert_called_once_with()
        assert process.communicate.call_args_list == [  # noqa: S101
            mock.call(timeout=15),
            mock.call(),
        ]
        assert result == "feature/test-branch"  # noqa: S101


class TestHasRubberduckAddinReferences:
    """Tests for has_rubberduck_addin_references helper."""

    def test_returns_false_when_workbook_cannot_be_opened(self, tmp_path: Path) -> None:
        """OSError while opening workbook should return False."""
        missing_workbook = tmp_path / "missing.xlsm"

        result = pre_commit_vba.has_rubberduck_addin_references(missing_workbook)

        assert result is False  # noqa: S101


class TestCodeMetadataPortionIsOkInTrailingWhitespaceCheck:
    """Test class for code metadata portion in trailing whitespace check."""

    @pytest.fixture(scope="class")
    @classmethod
    def set_up(cls) -> typing.tuple[subprocess.Popen, bytes]:
        """Set up for test."""
        with mock.patch.object(pre_commit_vba, "add_to_staging", return_value=None):
            runner.invoke(
                app,
                [
                    "extract",
                    "--target-path",
                    "tests",
                    "--folder-suffix",
                    ".test",
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
                "tests/test.xlsm.test/code/registerForm/RegisterProductForm.frm",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            stdout_data, _ = process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout_data, _ = process.communicate()
        finally:
            shutil.rmtree(
                Path(Path.cwd(), "tests", "test.xlsm.test"), ignore_errors=True
            )
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
                ".test",
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

    def test_folder_suffix_is_test(self, caplog) -> None:  # noqa: ANN001
        """Test that folder suffix is '.test'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "folder-suffix: .test" in caplog.text  # noqa: S101

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


@pytest.mark.skipif(DispatchEx is None, reason="pywin32 is only available on Windows")
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
        shutil.rmtree(Path(Path.cwd(), "tests", "test.xlsm.test"), ignore_errors=True)

    @classmethod
    def sut(cls) -> CliRunner:
        """Fixture for TestExtractCommandExistenceFiles."""
        with mock.patch.object(pre_commit_vba, "add_to_staging", return_value=None):
            return runner.invoke(
                app,
                [
                    "extract",
                    "--target-path",
                    "tests",
                    "--folder-suffix",
                    ".test",
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
        assert Path(Path.cwd(), "tests", "test.xlsm.test", file).exists()  # noqa: S101

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
    """Test that the test1.test folder does not exist."""
    if Path(Path.cwd(), "tests", "test1.test").exists():
        shutil.rmtree(Path(Path.cwd(), "tests", "test1.test"))
    try:
        with mock.patch.object(pre_commit_vba, "add_to_staging", return_value=None):
            runner.invoke(
                app,
                [
                    "extract",
                    "--target-path",
                    "tests",
                    "--folder-suffix",
                    ".test",
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
        test_result = not Path(Path.cwd(), "tests", "test1.test").exists()
        if Path(Path.cwd(), "tests", "test1.test").exists():
            shutil.rmtree(Path(Path.cwd(), "tests", "test1.test"))
        assert test_result  # noqa: S101
    finally:
        shutil.rmtree(Path(Path.cwd(), "tests", "test.xlsm.test"), ignore_errors=True)


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

        try:
            exit_code, output = result_queue.get(timeout=10)
        except queue.Empty:
            pytest.fail("extract command did not publish a result to the queue")
        assert process.exitcode == 0, output  # noqa: S101
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
        result_queue.close()
        result_queue.join_thread()
        shutil.rmtree(temp_root, ignore_errors=True)


def test_check_command_does_not_timeout_on_issue107_repro_workbook() -> None:
    """Issue107: check command should not block on Workbook_Open macro."""
    repro_workbook = Path(
        Path.cwd(),
        "tests",
        "fixtures",
        "issue107",
        "Issue107_Repro_WorkbookOpen_MsgBox.xlsm",
    )
    assert repro_workbook.exists()  # noqa: S101

    temp_root = Path(
        tempfile.mkdtemp(prefix="issue107-check-", dir=Path.cwd() / "tests")
    )
    target_workbook = Path(temp_root, repro_workbook.name)
    git_path = shutil.which("git")
    assert git_path is not None  # noqa: S101
    excel_process_ids_before = _get_excel_process_ids()

    process = None
    result_queue = multiprocessing.Queue()
    try:
        shutil.copy2(repro_workbook, target_workbook)
        process = multiprocessing.Process(
            target=_run_check_issue107_with_cli_runner,
            args=(str(temp_root), result_queue),
        )
        process.start()
        process.join(timeout=15)

        if process.is_alive():
            process.terminate()
            process.join(timeout=5)
            pytest.fail("check command timed out for Issue107 repro workbook")

        try:
            exit_code, output = result_queue.get(timeout=10)
        except queue.Empty:
            pytest.fail("check command did not publish a result to the queue")
        assert process.exitcode == 0, output  # noqa: S101
        assert exit_code == 1, output  # noqa: S101
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
        result_queue.close()
        result_queue.join_thread()
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
                ".test",
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


@pytest.mark.skipif(DispatchEx is None, reason="pywin32 is only available on Windows")
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
        shutil.rmtree(Path(Path.cwd(), "tests", "test.xlsm.test"), ignore_errors=True)

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

    def test_branch_release_version_mismatch_exits_with_error(
        self, caplog: Generator[pytest.LogCaptureFixture]
    ) -> None:
        """Version mismatch between workbook and branch should exit with error."""
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
            mock.patch.object(
                pre_commit_vba,
                "get_workbook_version",
                return_value="v9.9.9",
            ),
        ):
            sut = runner.invoke(app, ["check", "--target-path", "tests"])
            assert sut.exit_code == 1  # noqa: S101
            assert "Version mismatch" in caplog.text  # noqa: S101

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
