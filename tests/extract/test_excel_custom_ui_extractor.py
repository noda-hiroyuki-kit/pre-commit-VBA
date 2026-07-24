"""Tests for ExcelCustomUiExtractor class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import logging
import os
import shutil
import subprocess
import sys
import textwrap
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
    @classmethod
    def sut(cls) -> Generator[ExcelCustomUiExtractor]:
        """Act first this tests."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "test.xlsm"), ".VBA", include_extension=True
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
            Path.cwd(), "tests", "test.xlsm.VBA", "customUI", "customUI14.xml"
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_custom_ui_folder_not_created_when_no_custom_ui_files(self) -> None:
        """Test that custom_ui_folder is not created
        when no custom UI files are present.
        """  # noqa: D205
        workbook_path = Path("tests/extract/no_custom_ui.xlsm")
        common_folder = SettingsCommonFolder(workbook_path, ".VBA")
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="",
            custom_ui_folder="customUI",
            code_folder="",
        )
        if settings.common_folder.exists():
            shutil.rmtree(settings.common_folder)

        ExcelCustomUiExtractor(settings)

        assert not settings.custom_ui_folder.exists()  # noqa: S101

    def test_logs_japanese_workbook_filename_without_mojibake(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Issue121: log output should keep Japanese workbook filename."""
        workbook_path = Path("tests/fixtures/issue121/Issue121_日本語.xlsm")
        common_folder = SettingsCommonFolder(workbook_path, ".VBA")
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="",
            custom_ui_folder="customUI",
            code_folder="",
        )
        if settings.common_folder.exists():
            shutil.rmtree(settings.common_folder)

        try:
            caplog.set_level(logging.INFO)
            ExcelCustomUiExtractor(settings)

            expected_log_14 = "customUI14.xml does not exists in Issue121_日本語.xlsm"
            expected_log = "customUI.xml does not exists in Issue121_日本語.xlsm"
            assert expected_log_14 in caplog.text  # noqa: S101
            assert expected_log in caplog.text  # noqa: S101
        finally:
            if settings.common_folder.exists():
                shutil.rmtree(settings.common_folder)

    @pytest.mark.skipif(
        sys.platform != "win32", reason="Windows specific encoding behavior"
    )
    def test_japanese_filename_is_readable_by_utf8_consumers(self) -> None:
        """Issue121: UTF-8 consumers should read Japanese filename without mojibake."""
        workbook_path = Path("tests/fixtures/issue121/Issue121_日本語.xlsm")
        common_folder = SettingsCommonFolder(workbook_path, ".VBA")
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="",
            custom_ui_folder="customUI",
            code_folder="",
        )
        script = textwrap.dedent(
            """
            from pathlib import Path
            from src.pre_commit_vba.pre_commit_vba import (
                ExcelCustomUiExtractor,
                SettingsCommonFolder,
                SettingsFoldersHandleExcel,
            )

            workbook_path = Path("tests/fixtures/issue121/Issue121_日本語.xlsm")
            common_folder = SettingsCommonFolder(workbook_path, ".VBA")
            settings = SettingsFoldersHandleExcel(
                settings_common_folder=common_folder,
                export_folder="",
                custom_ui_folder="customUI",
                code_folder="",
            )
            if settings.common_folder.exists():
                import shutil

                shutil.rmtree(settings.common_folder)
            ExcelCustomUiExtractor(settings)
            """
        )
        env = os.environ.copy()
        env["PYTHONUTF8"] = "0"
        env["PYTHONIOENCODING"] = "cp932"

        if settings.common_folder.exists():
            shutil.rmtree(settings.common_folder)

        try:
            process = subprocess.run(  # noqa: S603
                [sys.executable, "-c", script],
                check=False,
                capture_output=True,
                cwd=Path.cwd(),
                env=env,
            )

            expected_log = "customUI14.xml does not exists in Issue121_日本語.xlsm"
            utf8_decoded = process.stderr.decode("utf-8", errors="replace")
            assert expected_log in utf8_decoded  # noqa: S101
        finally:
            if settings.common_folder.exists():
                shutil.rmtree(settings.common_folder)
