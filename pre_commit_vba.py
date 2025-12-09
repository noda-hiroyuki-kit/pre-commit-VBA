"""pre-commit-vba script.

extract code files from excel workbook with codes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import DEBUG, basicConfig, getLogger
from pathlib import Path  # noqa: F401

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


class ExcelVbComponent:
    """A placeholder class for ExcelVbComponent."""

    def __init__(self, target_folder: str, workbook_name: str) -> None:
        """Initialize with file path."""
        self._app = self._get_xl_app()
        self._workbook = self._app.Workbooks.Open(
            f"{target_folder}\\{workbook_name}", ReadOnly=True
        )
        self._components: dict[str, int | None] = {}
        for vb_comp in self._workbook.VBProject.VBComponents:
            self._components[vb_comp.Name] = vb_comp.Type

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

    @property
    def components(self) -> dict[str, int | None]:
        """Return components dict."""
        return self._components


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
