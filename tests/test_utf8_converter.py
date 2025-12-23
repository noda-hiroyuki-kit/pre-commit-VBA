"""Test for Utf8Converter."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from pre_commit_vba import ExcelVbaExporter, SettingsHandleExcel, Utf8Converter


class TestExcelVbaExporter:
    """Tests for ExcelVbaExporter class."""

    @pytest.fixture(scope="class")
    def sut(self) -> Generator[Utf8Converter]:
        """Act first this tests."""
        settings = SettingsHandleExcel(
            target_folder=f"{Path.cwd()}\\tests",
            folder_suffix=".VBA",
            export_folder="export",
            custom_ui_folder="",
        )
        book_name = "test.xlsm"
        vb_component_export_folder = settings.common_folder(book_name)
        if Path.is_dir(vb_component_export_folder):
            shutil.rmtree(vb_component_export_folder)
        ExcelVbaExporter(book_name, settings)
        yield Utf8Converter(book_name, settings)
        shutil.rmtree(vb_component_export_folder)

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
