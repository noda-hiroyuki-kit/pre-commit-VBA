"""Tests for ExcelVbComponent class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from pre_commit_vba import ExcelVbComponent


class TestExcelVbComponent:
    """Tests for ExcelVbComponent class."""

    class TestConstructExcelVbComponent:
        """Tests for construct ExcelVbComponent."""

        @pytest.fixture(scope="class")
        def sut(self) -> Generator[ExcelVbComponent]:
            """Act first this tests."""
            vb_component_export_folder = f"{Path.cwd()}\\tests\\test.VBA"
            if Path.is_dir(vb_component_export_folder):
                shutil.rmtree(vb_component_export_folder)
            yield ExcelVbComponent(f"{Path.cwd()}\\tests", "test.xlsm")
            shutil.rmtree(vb_component_export_folder)

        def test_exists_this_workbook(self, sut: ExcelVbComponent) -> None:
            """Test that ThisWorkbook component exists."""
            assert sut.components["ThisWorkbook"] is not None  # noqa: S101

        def test_exists_this_workbook_file(self, sut: ExcelVbComponent) -> None:  # noqa: ARG002
            """Test that ThisWorkbook component file exists."""
            expected_file = f"{Path.cwd()}\\tests\\test.VBA\\ThisWorkbook.cls"
            assert Path.is_file(expected_file)  # noqa: S101

        def test_exists_sheet1(self, sut: ExcelVbComponent) -> None:
            """Test that Sheet1 component exists."""
            assert sut.components["Sheet1"] is not None  # noqa: S101

        def test_equals_this_workbook_type_100(self, sut: ExcelVbComponent) -> None:
            """Test that ThisWorkbook component exists."""
            expected_type_id = 100  # vbext_ct_Document
            assert sut.components["ThisWorkbook"] == expected_type_id  # noqa: S101
