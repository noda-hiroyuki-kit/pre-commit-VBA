"""Test module for pre-commit-vba script."""

from logging import INFO
from pathlib import Path

from typer.testing import CliRunner

from pre_commit_vba import app, extract

runner = CliRunner()


def test_extract_function_exists() -> None:
    """Test that the extract function exists in pre_commit_vba module."""
    assert callable(extract)  # noqa: S101


def test_extract_command_execution(caplog) -> None:  # noqa: ANN001
    """Test that the extract command executes without errors."""
    caplog.set_level(INFO)
    result = runner.invoke(app, ["extract"])
    assert result.exit_code == 0  # noqa: S101
    assert "Hello from pre-commit-vba!" in caplog.text  # noqa: S101


class TestExtractCommandPositiveOptions:
    """Test class for extract command."""

    def extract_command_fixture(self, caplog) -> CliRunner:  # noqa: ANN001
        """Test that the extract command executes without errors."""
        caplog.set_level(INFO)
        return runner.invoke(
            app,
            [
                "extract",
                "--target-path",
                ".",
                "--folder-suffix",
                ".VBA",
                "--export-folder",
                "export",
                "--custom-ui-folder",
                "customUI",
                "--code-folder",
                "code",
                "--enable-folder-annotation",
                "--create-gitignore",
            ],
        )

    def test_target_path_is_current_directory(self, caplog) -> None:  # noqa: ANN001
        """Test that target_path is current directory."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert f"{Path.cwd()}".lower() in caplog.text  # noqa: S101

    def test_folder_suffix_is_vba(self, caplog) -> None:  # noqa: ANN001
        """Test that folder suffix is '.VBA'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "folder-suffix: .VBA" in caplog.text  # noqa: S101

    def test_export_folder_is_export(self, caplog) -> None:  # noqa: ANN001
        """Test that export folder is 'export'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "export-folder: export" in caplog.text  # noqa: S101

    def test_custom_ui_folder_is_custom_ui(self, caplog) -> None:  # noqa: ANN001
        """Test that custom ui folder is 'customUI'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "custom-ui-folder: customUI" in caplog.text  # noqa: S101

    def test_code_folder_is_code(self, caplog) -> None:  # noqa: ANN001
        """Test that code folder is 'code'."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "code-folder: code" in caplog.text  # noqa: S101

    def test_enable_folder_annotation_is_true(self, caplog) -> None:  # noqa: ANN001
        """Test that enable-folder-annotation is True."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "enable-folder-annotation: True" in caplog.text  # noqa: S101

    def test_create_gitignore_is_true(self, caplog) -> None:  # noqa: ANN001
        """Test that create-gitignore is True."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "create-gitignore: True" in caplog.text  # noqa: S101


class TestExtractCommandNegativeOptions:
    """Test class for extract command."""

    def extract_command_fixture(self, caplog) -> CliRunner:  # noqa: ANN001
        """Test that the extract command executes without errors."""
        caplog.set_level(INFO)
        return runner.invoke(
            app,
            [
                "extract",
                "--target-path",
                ".",
                "--folder-suffix",
                ".VBA",
                "--export-folder",
                "export",
                "--custom-ui-folder",
                "customUI",
                "--code-folder",
                "code",
                "--disable-folder-annotation",
                "--not-create-gitignore",
            ],
        )

    def test_enable_folder_annotation_is_false(self, caplog) -> None:  # noqa: ANN001
        """Test that enable-folder-annotation is False."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "enable-folder-annotation: False" in caplog.text  # noqa: S101

    def test_create_gitignore_is_false(self, caplog) -> None:  # noqa: ANN001
        """Test that create-gitignore is False."""
        result = self.extract_command_fixture(caplog)
        assert result.exit_code == 0  # noqa: S101
        assert "create-gitignore: False" in caplog.text  # noqa: S101
