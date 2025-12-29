"""Test for Utf8Converter."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from pre_commit_vba import (
    ExcelVbaExporter,
    SettingsCommonFolder,
    SettingsFoldersHandleExcel,
    SettingsOptionsHandleExcel,
    Utf8Converter,
)


class TestExcelVbaExporter:
    """Tests for ExcelVbaExporter class."""

    @pytest.fixture(scope="class")
    def sut(self) -> Generator[Utf8Converter]:
        """Act first this tests."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "test.xlsm"), ".VBA"
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="customUI",
            code_folder="code",
        )
        options = SettingsOptionsHandleExcel(
            enable_folder_annotation=True,
        )
        if Path.is_dir(settings.common_folder):
            shutil.rmtree(settings.common_folder)
        ExcelVbaExporter(settings)
        yield Utf8Converter(settings, options)
        shutil.rmtree(settings.common_folder)

    def test_exists_this_workbook_file(self, sut: Utf8Converter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = Path(
            Path.cwd(),
            "tests",
            "test.VBA",
            "code",
            "excel document modules",
            "ブック",
            "ThisWorkbook.cls",
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_exists_sheet1_file(self, sut: Utf8Converter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = Path(
            Path.cwd(),
            "tests",
            "test.VBA",
            "code",
            "excel document modules",
            "シート",
            "sheet1.cls",
        )
        assert Path.is_file(expected_file)  # noqa: S101
