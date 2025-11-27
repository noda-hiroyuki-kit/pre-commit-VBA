"""pre-commit-vba script.

extract code files from excel workbook with codes.
"""

from logging import DEBUG, basicConfig, getLogger
from pathlib import Path

import typer
from win32com.client import gencache

app = typer.Typer()
basicConfig(level=DEBUG)
logger = getLogger(__name__)


class ExcelVbComponent:
    """A placeholder class for ExcelVbComponent."""

    def __init__(self, file_path: str) -> None:
        """Initialize with file path."""
        self._app = self._get_xl_app()
        self._workbook = self._app.Workbooks.Open(
            f"{Path.cwd()}\\{file_path}", ReadOnly=True
        )
        self._components: dict[str, int | None] = {}
        for vb_comp in self._workbook.VBProject.VBComponents:
            self._components[vb_comp.Name] = vb_comp.Type

    def _get_xl_app(self) -> gencache.Dispatch:
        """Get Excel application."""
        excel_app = gencache.EnsureDispatch("Excel.Application")
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


@app.command()
def main() -> None:
    """Log info Hello pre-commit-vba script."""
    logger.info("Hello from pre-commit-vba!")


if __name__ == "__main__":
    app()
