"""pre-commit-vba script.

extract code files from excel workbook with codes.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import DEBUG, basicConfig, getLogger
from pathlib import Path
from zipfile import ZipFile

import typer
from win32com.client import Dispatch


class UndefineTypeError(Exception):
    """Custom UndefineTypeError exception."""


@dataclass(frozen=True)
class Constants:
    """Constants Class for win32com.

    This class can replace win32com.client.constants as follows:
    `constants=Constants()`
    """

    vbext_ct_ClassModule: int = 2  # from enum vbext_ComponentType  # noqa: N815
    vbext_ct_Document: int = 100  # from enum vbext_ComponentType  # noqa: N815
    vbext_ct_MSForm: int = 3  # from enum vbext_ComponentType  # noqa: N815
    vbext_ct_StdModule: int = 1  # from enum vbext_ComponentType  # noqa: N815


class SettingsCommonFolder:
    """Settings for handling common folder."""

    def __init__(
        self,
        workbook_path: Path,
        folder_suffix: str,
    ) -> None:
        """Initialize settings."""
        self.__workbook_path = workbook_path
        self.__folder_suffix = folder_suffix

    @property
    def common_folder(self) -> Path:
        """Return common folder path."""
        return Path(
            self.__workbook_path.parent,
            f"{self.__workbook_path.name.split('.')[0]}{self.__folder_suffix}",
        )

    @property
    def workbook_path(self) -> Path:
        """Return workbook path."""
        return self.__workbook_path


class SettingsFoldersHandleExcel:
    """Settings for handling Excel."""

    def __init__(
        self,
        settings_common_folder: SettingsCommonFolder,
        export_folder: str,
        custom_ui_folder: str,
        code_folder: str,
    ) -> None:
        """Initialize settings."""
        self.__settings_common_folder = settings_common_folder
        self.__export_folder = export_folder
        self.__custom_ui_folder = custom_ui_folder
        self.__code_folder = code_folder

    @property
    def export_folder(self) -> Path:
        """Return common folder path."""
        return Path(self.__settings_common_folder.common_folder, self.__export_folder)

    @property
    def custom_ui_folder(self) -> Path:
        """Return custom UI folder path."""
        return Path(
            self.__settings_common_folder.common_folder, self.__custom_ui_folder
        )

    @property
    def code_folder(self) -> Path:
        """Return code folder path."""
        return Path(self.__settings_common_folder.common_folder, self.__code_folder)

    @property
    def workbook_path(self) -> Path:
        """Return workbook path."""
        return self.__settings_common_folder.workbook_path

    @property
    def common_folder(self) -> Path:
        """Return common folder path."""
        return self.__settings_common_folder.common_folder


class SettingsOptionsHandleExcel:
    """Settings for handling Excel options."""

    def __init__(
        self, *, enable_folder_annotation: bool, create_gitignore: bool
    ) -> None:
        """Initialize settings."""
        self.__enable_folder_annotation = enable_folder_annotation
        self.__create_gitignore = create_gitignore

    def enable_folder_annotation(self) -> bool:
        """Return enable folder annotation setting."""
        return self.__enable_folder_annotation

    def create_gitignore(self) -> bool:
        """Return create gitignore setting."""
        return self.__create_gitignore


class ExcelVbaExporter:
    """A placeholder class for ExcelVbaExporter."""

    def __init__(self, settings: SettingsFoldersHandleExcel) -> None:
        """Initialize with file path."""
        self.__app = self.__get_xl_app()
        self.__workbook = self.__app.Workbooks.Open(
            settings.workbook_path, ReadOnly=True
        )
        settings.export_folder.mkdir(parents=True, exist_ok=True)
        for vb_comp in self.__workbook.VBProject.VBComponents:
            vb_comp_file_name = vb_component_type_factory(
                vb_comp.Name, vb_comp.Type
            ).file_name
            vb_comp.Export(Path(settings.export_folder, f"{vb_comp_file_name}"))

    def __get_xl_app(self) -> Dispatch:
        """Get Excel application."""
        excel_app = Dispatch("Excel.Application")
        excel_app.Visible = True
        excel_app.DisplayAlerts = False
        return excel_app

    def __del__(self) -> None:
        """Destructor to close workbook and quit app."""
        try:
            self.__workbook.Close(SaveChanges=False)
            self.__app.Quit()
        except Exception:
            logger.exception("Error in destructor")
            raise


def vb_component_type_factory(module_name: str, type_id: int) -> IVbComponentType:
    """Return VbComponentType instances."""
    if type_id == constants.vbext_ct_StdModule:
        return StdModule(module_name)
    if type_id == constants.vbext_ct_ClassModule:
        return ClassModule(module_name)
    if type_id == constants.vbext_ct_MSForm:
        return UserFormModule(module_name)
    if type_id == constants.vbext_ct_Document:
        return SheetClassModule(module_name)
    raise UndefineTypeError(type_id)


class IVbComponentType(ABC):
    """A placeholder class for VbComponentType constants."""

    def __init__(self, module_name: str) -> None:
        """Initialize Class Module type."""
        self.module_name = module_name

    @property
    @abstractmethod
    def file_name(self) -> str:
        """Return module name."""
        raise NotImplementedError


class StdModule(IVbComponentType):
    """Standard Module type."""

    @property
    def file_name(self) -> str:
        """Return module name."""
        return self.module_name + ".bas"


class ClassModule(IVbComponentType):
    """Class Module type."""

    @property
    def file_name(self) -> str:
        """Return module name."""
        return self.module_name + ".cls"


class UserFormModule(IVbComponentType):
    """User Form type."""

    @property
    def file_name(self) -> str:
        """Return module name."""
        return self.module_name + ".frm"


class SheetClassModule(IVbComponentType):
    """Sheet class type."""

    @property
    def file_name(self) -> str:
        """Return module name."""
        return self.module_name + ".cls"


class ExcelCustomUiExtractor:
    """A placeholder class for ExcelCustomUiExtractor."""

    def __init__(self, settings: SettingsFoldersHandleExcel) -> None:
        """Initialize with file path."""
        self.__settings = settings
        self.__extract_custom_ui_files()

    def __extract_custom_ui_files(self) -> None:
        self.__settings.custom_ui_folder.mkdir(parents=True, exist_ok=True)
        self.__extract_custom_ui_file("customUI/customUI14.xml")
        self.__extract_custom_ui_file("customUI/customUI.xml")

    def __extract_custom_ui_file(self, full_item_name: str) -> None:
        try:
            with ZipFile(self.__settings.workbook_path, "r") as zip_ref:
                file_data = zip_ref.read(full_item_name)
            with Path(self.__settings.custom_ui_folder, Path(full_item_name).name).open(
                mode="wb"
            ) as xml_file:
                xml_file.write(file_data)
        except KeyError:
            logger.info(
                "%s does not exists in %s",
                Path(full_item_name).name,
                self.__settings.workbook_path.name,
            )


class Utf8Converter:
    """A placeholder class for Utf8Converter."""

    def __init__(
        self, settings: SettingsFoldersHandleExcel, options: SettingsOptionsHandleExcel
    ) -> None:
        """Initialize with file path."""
        self.__settings = settings
        self.__options = options
        self.__add_gitignore_file()
        self.__convert_to_utf8()

    def __add_gitignore_file(self) -> None:
        if not self.__options.create_gitignore():
            return
        gitignore_content = f"{self.__settings.export_folder.name}/\n"
        with Path(self.__settings.common_folder, ".gitignore").open(
            mode="w", encoding="utf-8", newline="\n"
        ) as gitignore_file:
            gitignore_file.write(gitignore_content)

    def __convert_to_utf8(self) -> None:
        for file_path in self.__settings.export_folder.glob("*.*"):
            content = self.__format_line_breaks(
                file_path.read_text(encoding="shift-jis")
            )
            code_folder = self.__get_code_folder(content)
            code_folder.mkdir(parents=True, exist_ok=True)
            code_path = Path(code_folder, file_path.name)
            code_path.write_text(content, encoding="utf-8", newline="\n")

    def __format_line_breaks(self, text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"

    def __get_code_folder(self, text: str) -> Path:
        code_root_folder = self.__settings.code_folder
        if not self.__options.enable_folder_annotation():
            return code_root_folder
        pattern = r"\'@Folder \"(.*)\""
        if match := re.search(pattern, text):
            return Path(code_root_folder, *match.group(1).split("."))
        return code_root_folder


app = typer.Typer()
basicConfig(level=DEBUG)
logger = getLogger(__name__)
constants = Constants()


@app.command()
def main() -> None:
    """Log info Hello pre-commit-vba script."""
    logger.info("Hello from pre-commit-vba!")


if __name__ == "__main__":
    app()
