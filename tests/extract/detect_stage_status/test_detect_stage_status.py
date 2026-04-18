"""Tests for staging state detection during extract command."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZipFile

import pytest
from typer.testing import CliRunner

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch

from src.pre_commit_vba import pre_commit_vba
from src.pre_commit_vba.pre_commit_vba import app

runner = CliRunner()


MODULE_TEXT = 'Attribute VB_Name = "Module1"\n'


class _DummyProcess:
    def __init__(
        self, *, returncode: int, stdout_data: bytes, stderr_data: bytes
    ) -> None:
        self.returncode = returncode
        self._stdout_data = stdout_data
        self._stderr_data = stderr_data

    def communicate(self, timeout: int | None = None) -> tuple[bytes, bytes]:
        _ = timeout
        return self._stdout_data, self._stderr_data

    def kill(self) -> None:
        pass


def _create_workbook_with_vba(workbook_path: Path) -> None:
    workbook_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(workbook_path, "w") as zip_ref:
        zip_ref.writestr("xl/vbaProject.bin", b"dummy")


class _DummyExcelVbaExporter:
    def __init__(self, settings: pre_commit_vba.SettingsFoldersHandleExcel) -> None:
        settings.export_folder.mkdir(parents=True, exist_ok=True)
        Path(settings.export_folder, "Module1.bas").write_text(
            MODULE_TEXT, encoding="utf-8"
        )


class _DummyExcelCustomUiExtractor:
    def __init__(self, settings: pre_commit_vba.SettingsFoldersHandleExcel) -> None:
        pass


class _DummyUtf8Converter:
    def __init__(
        self,
        settings: pre_commit_vba.SettingsFoldersHandleExcel,
        options: pre_commit_vba.SettingsOptionsHandleExcel,
    ) -> None:
        settings.code_folder.mkdir(parents=True, exist_ok=True)
        Path(settings.code_folder, "Module1.bas").write_text(
            MODULE_TEXT, encoding="utf-8"
        )
        if options.create_gitignore():
            Path(settings.common_folder, ".gitignore").write_text(
                f"{settings.export_folder.name}/\n", encoding="utf-8"
            )


def _init_git_repo(repo_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo_path, check=True)  # noqa: S607
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],  # noqa: S607
        cwd=repo_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],  # noqa: S607
        cwd=repo_path,
        check=True,
    )


def _patch_extract_dependencies(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(pre_commit_vba, "ExcelVbaExporter", _DummyExcelVbaExporter)
    monkeypatch.setattr(
        pre_commit_vba,
        "ExcelCustomUiExtractor",
        _DummyExcelCustomUiExtractor,
    )
    monkeypatch.setattr(pre_commit_vba, "Utf8Converter", _DummyUtf8Converter)


def test_get_staging_status_raises_error_when_git_diff_fails(
    monkeypatch: MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """`get_staging_status` should raise and log stderr when git diff fails."""

    def _mock_popen(*_args: object, **_kwargs: object) -> _DummyProcess:
        return _DummyProcess(returncode=1, stdout_data=b"", stderr_data=b"mock stderr")

    monkeypatch.setattr(pre_commit_vba.subprocess, "Popen", _mock_popen)

    with caplog.at_level("ERROR"), pytest.raises(pre_commit_vba.StagingStatusError):
        pre_commit_vba.get_staging_status()

    assert (  # noqa: S101
        "Failed to get staging status via 'git diff --cached'. stderr: mock stderr"
        in caplog.text
    )


def test_extract_returns_non_zero_when_staging_status_retrieval_fails(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Extract should fail fast when staging status cannot be retrieved."""
    _init_git_repo(tmp_path)
    _patch_extract_dependencies(monkeypatch)

    workbook_path = Path(tmp_path, "test.xlsm")
    _create_workbook_with_vba(workbook_path)

    def _raise_staging_status_error() -> str:
        raise pre_commit_vba.StagingStatusError

    monkeypatch.setattr(
        pre_commit_vba, "get_staging_status", _raise_staging_status_error
    )

    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["extract", "--target-path", str(tmp_path)])

    assert result.exit_code != 0  # noqa: S101


def test_extract_returns_non_zero_when_staging_state_changes(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Issue #47: extract should fail if staging state changes during the run."""
    _init_git_repo(tmp_path)
    _patch_extract_dependencies(monkeypatch)

    workbook_path = Path(tmp_path, "test.xlsm")
    _create_workbook_with_vba(workbook_path)

    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["extract", "--target-path", str(tmp_path)])

    assert result.exit_code != 0  # noqa: S101


def test_extract_returns_zero_when_staging_state_does_not_change(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Issue #47: extract should pass when staging state is unchanged."""
    _init_git_repo(tmp_path)
    _patch_extract_dependencies(monkeypatch)

    workbook_path = Path(tmp_path, "test.xlsm")
    _create_workbook_with_vba(workbook_path)

    baseline_common = Path(tmp_path, "test.xlsm.VBA")
    Path(baseline_common, "export").mkdir(parents=True, exist_ok=True)
    Path(baseline_common, "code").mkdir(parents=True, exist_ok=True)
    Path(baseline_common, "export", "Module1.bas").write_text(
        MODULE_TEXT, encoding="utf-8"
    )
    Path(baseline_common, "code", "Module1.bas").write_text(
        MODULE_TEXT, encoding="utf-8"
    )
    Path(baseline_common, ".gitignore").write_text("export/\n", encoding="utf-8")

    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)  # noqa: S607
    subprocess.run(
        ["git", "commit", "-m", "chore: prepare baseline"],  # noqa: S607
        cwd=tmp_path,
        check=True,
    )

    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["extract", "--target-path", str(tmp_path)])

    assert result.exit_code == 0  # noqa: S101
