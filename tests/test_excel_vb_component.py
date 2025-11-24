"""Tests for ExcelVbComponent class."""

from pre_commit_vba import ExcelVbComponent


class TestExcelVbComponent:
    """Tests for ExcelVbComponent class."""

    def test_this_work_book_exists(self) -> None:
        """Test that ThisWorkbook component exists in the test Excel file."""
        sut = ExcelVbComponent("tests/test.xlsm")
        assert sut.components["ThisWorkbook"] is not None  # noqa: S101

    def test_sheet1_exists(self) -> None:
        """Test that sheet1 component exists in the test Excel file."""
        sut = ExcelVbComponent("tests/test.xlsm")
        assert sut.components["sheet1"] is not None  # noqa: S101
