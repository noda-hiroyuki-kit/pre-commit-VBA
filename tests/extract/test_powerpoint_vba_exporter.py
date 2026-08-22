# Copyright (c) 2026 Noda Hiroyuki
"""Tests for PowerPointVbaExporter class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import shutil
from pathlib import Path

import pytest

from src.pre_commit_vba import pre_commit_vba
from src.pre_commit_vba.pre_commit_vba import (
    PowerPointVbaExporter,
    SettingsCommonFolder,
    SettingsFoldersHandleOffice,
)


@pytest.mark.skipif(
    pre_commit_vba.DispatchEx is None,
    reason="pywin32 is only available on Windows",
)
class TestPowerPointVbaExporter:
    """Tests for PowerPointVbaExporter class."""

    @pytest.fixture(scope="class")
    @classmethod
    def sut(cls) -> Generator[PowerPointVbaExporter]:
        """Act first this tests."""
        common_folder = SettingsCommonFolder(
            Path(Path.cwd(), "tests", "powerpoint", "extract", "test.pptm"),
            ".test",
            include_extension=True,
        )
        settings = SettingsFoldersHandleOffice(
            settings_common_folder=common_folder,
            export_folder="export",
            custom_ui_folder="",
            code_folder="",
        )
        if Path.is_dir(settings.common_folder):
            shutil.rmtree(settings.common_folder)
        yield PowerPointVbaExporter(settings)
        shutil.rmtree(settings.common_folder)

    def test_exists_std_module_file(
        self,
        sut: PowerPointVbaExporter,  # noqa: ARG002
    ) -> None:
        """Test that a standard module component file exists."""
        expected_file = Path(
            Path.cwd(),
            "tests",
            "powerpoint",
            "extract",
            "test.pptm.test",
            "export",
            "SampleTabModule.bas",
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_exists_class_module_file(
        self,
        sut: PowerPointVbaExporter,  # noqa: ARG002
    ) -> None:
        """Test that a class module component file exists."""
        expected_file = Path(
            Path.cwd(),
            "tests",
            "powerpoint",
            "extract",
            "test.pptm.test",
            "export",
            "Company.cls",
        )
        assert Path.is_file(expected_file)  # noqa: S101

    def test_exists_user_form_file(
        self,
        sut: PowerPointVbaExporter,  # noqa: ARG002
    ) -> None:
        """Test that a user form component file exists."""
        expected_file = Path(
            Path.cwd(),
            "tests",
            "powerpoint",
            "extract",
            "test.pptm.test",
            "export",
            "SetCompanyForm.frm",
        )
        assert Path.is_file(expected_file)  # noqa: S101


@pytest.mark.skipif(
    pre_commit_vba.DispatchEx is None,
    reason="pywin32 is only available on Windows",
)
class TestPowerPointAddinVbaExporter:
    """Tests for extracting VBA from a PowerPoint add-in."""

    def test_exports_ppam_vba_component(self, tmp_path: Path) -> None:
        """The PowerPoint add-in fixture should be extracted through the VBE."""
        source = Path(Path.cwd(), "tests", "powerpoint", "extract", "test.ppam")
        target = tmp_path / source.name
        shutil.copy2(source, target)
        settings = SettingsFoldersHandleOffice(
            SettingsCommonFolder(target, ".VBA"),
            "export",
            "customUI",
            "code",
        )

        PowerPointVbaExporter(settings)

        assert not settings.export_folder.exists()  # noqa: S101
