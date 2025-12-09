"""Tests for ExcelVbComponent class."""

from pathlib import Path

import pytest

from pre_commit_vba import ExcelVbComponent


class TestExcelVbComponent:
    """Tests for ExcelVbComponent class."""

    class TestConstructExcelVbComponent:
        """Tests for construct ExcelVbComponent."""

        @pytest.fixture(scope="class")
        def sut(self) -> ExcelVbComponent:
            """Act first this tests."""
            return ExcelVbComponent(f"{Path.cwd()}\\tests", "test.xlsm")

        def test_exists_this_workbook(self, sut: ExcelVbComponent) -> None:
            """Test that ThisWorkbook component exists."""
            assert sut.components["ThisWorkbook"] is not None  # noqa: S101

        def test_exists_sheet1(self, sut: ExcelVbComponent) -> None:
            """Test that Sheet1 component exists."""
            assert sut.components["Sheet1"] is not None  # noqa: S101

        def test_equals_this_workbook_type_100(self, sut: ExcelVbComponent) -> None:
            """Test that ThisWorkbook component exists."""
            expected_type_id = 100  # vbext_ct_Document
            assert sut.components["ThisWorkbook"] == expected_type_id  # noqa: S101
