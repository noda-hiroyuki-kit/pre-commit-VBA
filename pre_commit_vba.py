"""pre-commit-vba script.

extract code files from excel workbook with codes.
"""

from logging import DEBUG, basicConfig, getLogger

import typer

app = typer.Typer()
basicConfig(level=DEBUG)
logger = getLogger(__name__)


@app.command()
def main() -> None:
    """Log info Hello pre-commit-vba script."""
    logger.info("Hello from pre-commit-vba!")


if __name__ == "__main__":
    main()
