"""Tests for ExcelCustomUiExtractor class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from src.pre_commit_vba.pre_commit_vba import (
    ExcelCustomUiExtractor,
    SettingsCommonFolder,
    SettingsFoldersHandleExcel,
)


class TestExcelCustomUiExtractor:
    """Tests for ExcelCustomUiExtractor class."""

    @pytest.fixture(scope="class")
    def sut(self) -> Generator[ExcelCustomUiExtractor]:
        """Act first this tests."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "test.xlsm"), ".VBA"
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="",
            custom_ui_folder="customUI",
            code_folder="",
        )
        if Path.is_dir(settings.common_folder):
            shutil.rmtree(settings.common_folder)
        yield ExcelCustomUiExtractor(settings)
        shutil.rmtree(settings.common_folder)

    def test_exists_custom_ui_14_xml_file(self, sut: ExcelCustomUiExtractor) -> None:  # noqa: ARG002
        """Test that customUI14.xml file exists."""
        expected_file = Path(
            Path.cwd(), "tests", "test.VBA", "customUI", "customUI14.xml"
        )
        assert Path.is_file(expected_file)  # noqa: S101
