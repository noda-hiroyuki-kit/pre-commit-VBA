"""pre-commit-vba script.

extract code files from excel workbook with codes.
"""

from logging import DEBUG, basicConfig, getLogger

import typer

app = typer.Typer()
basicConfig(level=DEBUG)
logger = getLogger(__name__)


class ExcelVbComponent:
    """A placeholder class for ExcelVbComponent."""

    def __init__(self, file_path: str) -> None:
        """Initialize with file path."""
        self.file_path = file_path

    @property
    def components(self) -> dict[str, int | None]:
        """Return components dict."""
        return {"ThisWorkbook": 100}


@app.command()
def main() -> None:
    """Log info Hello pre-commit-vba script."""
    logger.info("Hello from pre-commit-vba!")


if __name__ == "__main__":
    app()
