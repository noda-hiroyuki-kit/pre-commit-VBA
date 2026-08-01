"""Test for Utf8Converter."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from src.pre_commit_vba.pre_commit_vba import (
    ExcelVbaExporter,
    SettingsCommonFolder,
    SettingsFoldersHandleExcel,
    SettingsOptionsHandleExcel,
    Utf8Converter,
)


class TestExcelVbaExporter:
    """Tests for ExcelVbaExporter class."""

    @pytest.fixture(scope="class")
    @classmethod
    def sut(cls) -> Generator[Utf8Converter]:
        """Act first this tests."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "test.xlsm"), ".test", include_extension=True
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="customUI",
            code_folder="code",
        )
        options = SettingsOptionsHandleExcel(
            enable_folder_annotation=True,
            create_gitignore=True,
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
            "test.xlsm.test",
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
            "test.xlsm.test",
            "code",
            "excel document modules",
            "シート",
            "sheet1.cls",
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_exists_gitignore_file(self, sut: Utf8Converter) -> None:  # noqa: ARG002
        """Test that ThisWorkbook component file exists."""
        expected_file = Path(
            Path.cwd(),
            "tests",
            "test.xlsm.test",
            ".gitignore",
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_not_create_gitignore_file_when_option_disabled(self) -> None:
        """Test that .gitignore is not created when disabled."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "test.xlsm"),
            ".no-gitignore",
            include_extension=True,
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="customUI",
            code_folder="code",
        )
        options = SettingsOptionsHandleExcel(
            enable_folder_annotation=True,
            create_gitignore=False,
        )
        if Path.is_dir(settings.common_folder):
            shutil.rmtree(settings.common_folder)

        try:
            ExcelVbaExporter(settings)
            Utf8Converter(settings, options)
            expected_file = Path(
                Path.cwd(),
                "tests",
                "test.xlsm.no-gitignore",
                ".gitignore",
            )
            assert not Path.is_file(expected_file)  # noqa: S101
        finally:
            if Path.is_dir(settings.common_folder):
                shutil.rmtree(settings.common_folder)


class TestUtf8ConverterFolderAnnotation:
    """Tests for folder-annotation behavior in Utf8Converter."""

    def test_disable_folder_annotation_keeps_file_in_code_root(self) -> None:
        """Disabled folder annotation should keep modules in code root."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "test.xlsm"),
            ".no-annotation",
            include_extension=True,
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="customUI",
            code_folder="code",
        )
        options = SettingsOptionsHandleExcel(
            enable_folder_annotation=False,
            create_gitignore=False,
        )
        if Path.is_dir(settings.common_folder):
            shutil.rmtree(settings.common_folder)

        try:
            ExcelVbaExporter(settings)
            Utf8Converter(settings, options)
            expected_file = Path(
                Path.cwd(),
                "tests",
                "test.xlsm.no-annotation",
                "code",
                "upperFolderQuotation.bas",
            )
            assert Path.is_file(expected_file)  # noqa: S101
        finally:
            if Path.is_dir(settings.common_folder):
                shutil.rmtree(settings.common_folder)

    def test_enable_folder_annotation_without_match_keeps_code_root(
        self,
        tmp_path: Path,
    ) -> None:
        """Enabled annotation should fallback to code root when no marker exists."""
        common_folder = SettingsCommonFolder(
            tmp_path / "workbook.xlsm",
            ".tmp",
            include_extension=True,
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="customUI",
            code_folder="code",
        )
        settings.export_folder.mkdir(parents=True, exist_ok=True)
        Path(settings.export_folder, "NoFolderAnnotation.bas").write_text(
            'Attribute VB_Name = "NoFolderAnnotation"\nOption Explicit\n',
            encoding="cp932",
            newline="\n",
        )
        options = SettingsOptionsHandleExcel(
            enable_folder_annotation=True,
            create_gitignore=False,
        )

        Utf8Converter(settings, options)

        expected_file = Path(settings.code_folder, "NoFolderAnnotation.bas")
        assert expected_file.is_file()  # noqa: S101

    def test_convert_to_utf8_continues_when_binary_probe_raises_oserror(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Binary probe OSError should be treated as non-binary file."""
        common_folder = SettingsCommonFolder(
            tmp_path / "workbook.xlsm",
            ".open-error",
            include_extension=True,
        )
        settings = SettingsFoldersHandleExcel(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="customUI",
            code_folder="code",
        )
        settings.export_folder.mkdir(parents=True, exist_ok=True)
        export_file = Path(settings.export_folder, "Module1.bas")
        export_file.write_text(
            'Attribute VB_Name = "Module1"\nOption Explicit\n',
            encoding="cp932",
            newline="\n",
        )
        options = SettingsOptionsHandleExcel(
            enable_folder_annotation=False,
            create_gitignore=False,
        )

        original_open = Path.open

        def _patched_open(
            path_obj: Path,
            *args: object,
            **kwargs: object,
        ) -> object:
            mode = args[0] if args else kwargs.get("mode", "r")
            if path_obj == export_file and mode == "rb":
                raise OSError
            return original_open(path_obj, *args, **kwargs)

        monkeypatch.setattr(Path, "open", _patched_open)

        Utf8Converter(settings, options)

        expected_file = Path(settings.code_folder, "Module1.bas")
        assert expected_file.is_file()  # noqa: S101
