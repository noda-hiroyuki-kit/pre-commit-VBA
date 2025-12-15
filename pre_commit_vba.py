"""pre-commit-vba script.

extract code files from excel workbook with codes.
"""

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


class ExcelVbaExporter:
    """A placeholder class for ExcelVbaExporter."""

    def __init__(
        self, target_folder: str, workbook_name: str, folder_suffix: str
    ) -> None:
        """Initialize with file path."""
        self._app = self._get_xl_app()
        self._workbook = self._app.Workbooks.Open(
            f"{target_folder}\\{workbook_name}", ReadOnly=True
        )
        vb_comp_export_folder = (
            f"{target_folder}\\{workbook_name.split('.')[0]}{folder_suffix}"
        )
        Path(vb_comp_export_folder).mkdir(exist_ok=True)
        for vb_comp in self._workbook.VBProject.VBComponents:
            vb_comp_file_name = vb_component_type_factory(
                vb_comp.Name, vb_comp.Type
            ).file_name
            vb_comp.Export(f"{vb_comp_export_folder}\\{vb_comp_file_name}")

    def _get_xl_app(self) -> Dispatch:
        """Get Excel application."""
        excel_app = Dispatch("Excel.Application")
        excel_app.Visible = True
        excel_app.DisplayAlerts = False
        return excel_app

    def __del__(self) -> None:
        """Destructor to close workbook and quit app."""
        try:
            self._workbook.Close(SaveChanges=False)
            self._app.Quit()
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

    def __init__(
        self,
        target_folder: str,
        workbook_name: str,
        folder_suffix: str,
        custom_ui_folder_name: str,
    ) -> None:
        """Initialize with file path."""
        self._target_folder = target_folder
        self._workbook_name = workbook_name
        self._folder_suffix = folder_suffix
        self._custom_ui_folder_name = custom_ui_folder_name
        self._extract_custom_ui_files()

    def _extract_custom_ui_files(self) -> None:
        self._make_export_folder()
        self._extract_custom_ui_file("customUI/customUI14.xml")
        self._extract_custom_ui_file("customUI/customUI.xml")

    def _make_export_folder(self) -> None:
        self._xml_export_folder = (
            f"{self._target_folder}"
            f"\\{self._workbook_name.split('.')[0]}{self._folder_suffix}"
            f"\\{self._custom_ui_folder_name}"
        )
        Path(self._xml_export_folder).mkdir(parents=True, exist_ok=True)

    def _extract_custom_ui_file(self, full_item_name: str) -> None:
        try:
            with ZipFile(
                f"{self._target_folder}\\{self._workbook_name}", "r"
            ) as zip_ref:
                file_data = zip_ref.read(full_item_name)
            with Path(f"{self._xml_export_folder}\\{Path(full_item_name).name}").open(
                mode="wb"
            ) as xml_file:
                xml_file.write(file_data)
        except KeyError:
            logger.info(
                "%s does not exists in %s",
                Path(full_item_name).name,
                self._workbook_name,
            )


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
