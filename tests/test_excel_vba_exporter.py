"""Tests for ExcelVbComponent class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from pre_commit_vba import ExcelVbaExporter, SettingsHandleExcel


class TestExcelVbaExporter:
    """Tests for ExcelVbaExporter class."""

    @pytest.fixture(scope="class")
    def sut(self) -> Generator[ExcelVbaExporter]:
        """Act first this tests."""
        settings = SettingsHandleExcel(
            target_folder=f"{Path.cwd()}\\tests",
            folder_suffix=".VBA",
            export_folder="export",
            custom_ui_folder="",
            code_folder="",
            enable_folder_annotation=False,
        )
        book_name = "test.xlsm"
        vb_component_export_folder = settings.common_folder(book_name)
        if Path.is_dir(vb_component_export_folder):
            shutil.rmtree(vb_component_export_folder)
        yield ExcelVbaExporter("test.xlsm", settings)
        shutil.rmtree(vb_component_export_folder)

    def test_exists_this_workbook_file(self, sut: ExcelVbaExporter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = Path(
            Path.cwd(), "tests", "test.VBA", "export", "ThisWorkbook.cls"
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_exists_sheet1_file(self, sut: ExcelVbaExporter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = Path(Path.cwd(), "tests", "test.VBA", "export", "sheet1.cls")
        assert Path.is_file(expected_file)  # noqa: S101
