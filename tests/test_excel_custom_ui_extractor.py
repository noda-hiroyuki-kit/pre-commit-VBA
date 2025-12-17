"""Tests for ExcelCustomUiExtractor class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from pre_commit_vba import ExcelCustomUiExtractor, SettingsHandleExcel


class TestExcelCustomUiExtractor:
    """Tests for ExcelCustomUiExtractor class."""

    @pytest.fixture(scope="class")
    def sut(self) -> Generator[ExcelCustomUiExtractor]:
        """Act first this tests."""
        settings = SettingsHandleExcel(
            target_folder=f"{Path.cwd()}\\tests",
            folder_suffix=".VBA",
            export_folder="",
            custom_ui_folder="customUI",
        )
        book_name = "test.xlsm"
        vb_component_export_folder = settings.common_folder(book_name)
        if Path.is_dir(vb_component_export_folder):
            shutil.rmtree(vb_component_export_folder)
        yield ExcelCustomUiExtractor(book_name, settings)
        shutil.rmtree(vb_component_export_folder)

    def test_exists_custom_ui_14_xml_file(self, sut: ExcelCustomUiExtractor) -> None:  # noqa: ARG002
        """Test that customUI14.xml file exists."""
        expected_file = f"{Path.cwd()}\\tests\\test.VBA\\customUI\\customUI14.xml"
        assert Path.is_file(expected_file)  # noqa: S101
