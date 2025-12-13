"""Tests for ExcelVbComponent class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from pre_commit_vba import ExcelVbaExporter


class TestExcelVbaExporter:
    """Tests for ExcelVbaExporter class."""

    @pytest.fixture(scope="class")
    def sut(self) -> Generator[ExcelVbaExporter]:
        """Act first this tests."""
        vb_component_export_folder = f"{Path.cwd()}\\tests\\test.VBA"
        if Path.is_dir(vb_component_export_folder):
            shutil.rmtree(vb_component_export_folder)
        yield ExcelVbaExporter(f"{Path.cwd()}\\tests", "test.xlsm", ".VBA")
        shutil.rmtree(vb_component_export_folder)

    def test_exists_this_workbook_file(self, sut: ExcelVbaExporter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = f"{Path.cwd()}\\tests\\test.VBA\\ThisWorkbook.cls"
        assert Path.is_file(expected_file)  # noqa: S101

    def test_exists_sheet1_file(self, sut: ExcelVbaExporter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = f"{Path.cwd()}\\tests\\test.VBA\\sheet1.cls"
        assert Path.is_file(expected_file)  # noqa: S101
