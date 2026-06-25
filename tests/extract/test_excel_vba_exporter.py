"""Tests for ExcelVbComponent class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path
from unittest.mock import Mock, call

import pytest

from src.pre_commit_vba.pre_commit_vba import (
    ExcelVbaExporter,
    SettingsCommonFolder,
    SettingsFoldersHandleExcel,
)


class TestExcelVbaExporter:
    """Tests for ExcelVbaExporter class."""

    @pytest.fixture(scope="class")
    @classmethod
    def sut(cls) -> Generator[ExcelVbaExporter]:
        """Act first this tests."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "test.xlsm"), ".VBA", include_extension=True
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="",
            code_folder="",
        )
        if Path.is_dir(settings.common_folder):
            shutil.rmtree(settings.common_folder)
        yield ExcelVbaExporter(settings)
        shutil.rmtree(settings.common_folder)

    def test_exists_this_workbook_file(self, sut: ExcelVbaExporter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = Path(
            Path.cwd(), "tests", "test.xlsm.VBA", "export", "ThisWorkbook.cls"
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_exists_sheet1_file(self, sut: ExcelVbaExporter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = Path(
            Path.cwd(), "tests", "test.xlsm.VBA", "export", "sheet1.cls"
        )
        assert Path.is_file(expected_file)  # noqa: S101


def test_destructor_does_not_raise_for_partially_initialized_instance() -> None:
    """Test destructor handles partially-initialized instances safely."""
    exporter = ExcelVbaExporter.__new__(ExcelVbaExporter)

    exporter.__del__()


def test_destructor_swallows_close_and_quit_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test destructor logs errors without re-raising exceptions."""
    exporter = ExcelVbaExporter.__new__(ExcelVbaExporter)
    workbook = Mock()
    app = Mock()
    workbook.Close.side_effect = RuntimeError("close failed")
    app.Quit.side_effect = RuntimeError("quit failed")
    object.__setattr__(exporter, "_ExcelVbaExporter__workbook", workbook)
    object.__setattr__(exporter, "_ExcelVbaExporter__app", app)

    mock_logger = Mock()
    monkeypatch.setattr("src.pre_commit_vba.pre_commit_vba.logger", mock_logger)

    exporter.__del__()

    workbook.Close.assert_called_once_with(SaveChanges=False)
    app.Quit.assert_called_once_with()

    expected_calls = [
        call("Error while closing workbook in destructor"),
        call("Error while quitting Excel app in destructor"),
    ]
    mock_logger.exception.assert_has_calls(expected_calls)
    assert mock_logger.exception.call_count == len(expected_calls)  # noqa: S101

    # Prevent duplicate destructor logs when pytest later garbage-collects this object.
    delattr(exporter, "_ExcelVbaExporter__workbook")
    delattr(exporter, "_ExcelVbaExporter__app")
