# Copyright (c) 2026 Noda Hiroyuki
"""pre-commit-vba script.

Extract VBA code from Excel workbooks, Word documents, and PowerPoint presentations.
"""

# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "pywin32>=312",
#   "olefile>=0.47",
#   "typer>=0.27.1",
# ]
# ///
import re
import shutil
import struct
import subprocess
import sys
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from typing import Annotated, Protocol, cast
from zipfile import BadZipFile, ZipFile

import olefile
import typer

OLE_FILE_ERROR: type[BaseException] = getattr(olefile, "OleFileError", OSError)

try:
    from pywintypes import com_error
    from win32com.client import DispatchEx
except ModuleNotFoundError:
    DispatchEx = None

    class _ComError(Exception):
        """Fallback COM error for non-Windows environments."""

    com_error = _ComError


class WindowsOnlyImportError(RuntimeError):
    """Raised when a Windows-only dependency is unavailable."""

    def __init__(self) -> None:
        """Initialize with a clear Windows-only import hint."""
        message = (
            "pre-commit-vba requires pywin32 (Windows only). "
            "Install it on Windows or run this hook on a Windows runner."
        )
        super().__init__(message)


class VbComponentProtocol(Protocol):
    """Protocol for a VBA component inside a workbook project."""

    Name: str
    Type: int
    Export: Callable[[Path], None]


class VbProjectProtocol(Protocol):
    """Protocol for the VBProject collection."""

    VBComponents: Iterable[VbComponentProtocol]


class WorkbookPropertiesProtocol(Protocol):
    """Protocol for an opened Excel workbook."""

    Close: Callable[..., None]
    BuiltinDocumentProperties: Callable[[str], object]
    VBProject: VbProjectProtocol


class WorkbooksProtocol(Protocol):
    """Protocol for the Excel workbooks collection."""

    Open: Callable[..., WorkbookPropertiesProtocol]


class ExcelApplicationProtocol(Protocol):
    """Protocol for the Excel application object."""

    Visible: bool
    DisplayAlerts: bool
    EnableEvents: bool
    AutomationSecurity: int
    Workbooks: WorkbooksProtocol
    Quit: Callable[[], None]


class DocumentsProtocol(Protocol):
    """Protocol for the Word documents collection."""

    Open: Callable[..., WorkbookPropertiesProtocol]


class WordApplicationProtocol(Protocol):
    """Protocol for the Word application object."""

    Visible: bool
    DisplayAlerts: bool
    AutomationSecurity: int
    Documents: DocumentsProtocol
    Quit: Callable[[], None]


class PresentationsProtocol(Protocol):
    """Protocol for the PowerPoint presentations collection."""

    Open: Callable[..., WorkbookPropertiesProtocol]


class PowerPointApplicationProtocol(Protocol):
    """Protocol for the PowerPoint application object."""

    DisplayAlerts: int
    AutomationSecurity: int
    Presentations: PresentationsProtocol
    Quit: Callable[[], None]


DispatchExFactory = Callable[
    [str],
    ExcelApplicationProtocol | WordApplicationProtocol | PowerPointApplicationProtocol,
]


def get_dispatch_ex() -> DispatchExFactory:
    """Return DispatchEx or raise a Windows-only import error."""
    if DispatchEx is None:
        raise WindowsOnlyImportError
    return cast("DispatchExFactory", DispatchEx)


def get_noninteractive_excel_app() -> ExcelApplicationProtocol:
    """Return a non-interactive Excel application instance."""
    dispatch_ex = get_dispatch_ex()
    excel_app = cast("ExcelApplicationProtocol", dispatch_ex("Excel.Application"))
    excel_app.Visible = False
    excel_app.DisplayAlerts = False
    # Prevent Workbook_Open / Auto_Open execution while opening workbooks.
    excel_app.EnableEvents = False
    excel_app.AutomationSecurity = constants.mso_automation_security_force_disable
    return excel_app


def get_noninteractive_word_app() -> WordApplicationProtocol:
    """Return a non-interactive Word application instance."""
    dispatch_ex = get_dispatch_ex()
    word_app = cast("WordApplicationProtocol", dispatch_ex("Word.Application"))
    word_app.Visible = False
    word_app.DisplayAlerts = False
    word_app.AutomationSecurity = constants.mso_automation_security_force_disable
    return word_app


def get_noninteractive_powerpoint_app() -> PowerPointApplicationProtocol:
    """Return a non-interactive PowerPoint application instance.

    Unlike Excel/Word, PowerPoint refuses to set Application.Visible to False;
    presentations are instead opened with WithWindow=False to stay hidden.
    """
    dispatch_ex = get_dispatch_ex()
    powerpoint_app = cast(
        "PowerPointApplicationProtocol",
        dispatch_ex("PowerPoint.Application"),
    )
    powerpoint_app.DisplayAlerts = constants.ppAlertsNone
    powerpoint_app.AutomationSecurity = constants.mso_automation_security_force_disable
    return powerpoint_app


def cleanup_office_resource(
    action: Callable[[], None],
    resource_name: str,
    application_name: str,
) -> None:
    """Run Office cleanup without masking the original failure cause.

    Cleanup errors are logged at debug level so the command behavior stays the same
    while still leaving a diagnostic trail for stray COM teardown failures.
    """
    try:
        action()
    except OSError, AttributeError, TypeError, com_error:
        logger.debug(
            "Failed to clean up %s resource: %s",
            application_name,
            resource_name,
            exc_info=True,
        )


__version__ = "0.4.0"


class UndefineTypeError(Exception):
    """Custom UndefineTypeError exception."""


class NotReleaseBranchError(Exception):
    """Custom NotReleaseBranch exception."""


class InvalidSemVerError(Exception):
    """Custom InvalidSemVer exception."""


class StagingStatusError(Exception):
    """Raised when staging status cannot be retrieved."""


class AddToStagingError(Exception):
    """Raised when extracted files cannot be staged with git add."""


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
    mso_automation_security_force_disable: int = 3  # from enum MsoAutomationSecurity
    ppAlertsNone: int = 1  # from enum PpAlertLevel  # noqa: N815


class SettingsCommonFolder:
    """Settings for handling common folder."""

    def __init__(
        self,
        office_file_path: Path | None = None,
        folder_suffix: str = "",
        *,
        include_extension: bool = True,
        workbook_path: Path | None = None,
    ) -> None:
        """Initialize settings.

        Args:
            office_file_path: Path to the Office file (e.g., Excel workbook).
            folder_suffix: Suffix for the folder (e.g., ".VBA").
            include_extension:
                If True, use full filename with extension(e.g., "test.xlsm.VBA").
                If False, use basename only (e.g., "test.VBA").
                Default is True (include extension).
            workbook_path: Legacy alias for office_file_path.

        """
        if office_file_path is None:
            office_file_path = workbook_path
        if office_file_path is None:
            raise TypeError

        self.__office_file_path = office_file_path
        self.__folder_suffix = folder_suffix
        self.__include_extension = include_extension

    @property
    def common_folder(self) -> Path:
        """Return common folder path."""
        if self.__include_extension:
            folder_name = f"{self.__office_file_path.name}{self.__folder_suffix}"
        else:
            folder_name = (
                f"{self.__office_file_path.name.split('.')[0]}{self.__folder_suffix}"
            )
        return Path(self.__office_file_path.parent, folder_name)

    @property
    def office_file_path(self) -> Path:
        """Return Office file path."""
        return self.__office_file_path

    @property
    def workbook_path(self) -> Path:
        """Return Office file path using the legacy property name."""
        return self.office_file_path


class SettingsFoldersHandleOffice:
    """Settings for handling Office."""

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
        """Return export folder path."""
        return Path(self.__settings_common_folder.common_folder, self.__export_folder)

    @property
    def custom_ui_folder(self) -> Path:
        """Return custom UI folder path."""
        return Path(
            self.__settings_common_folder.common_folder,
            self.__custom_ui_folder,
        )

    @property
    def code_folder(self) -> Path:
        """Return code folder path."""
        return Path(self.__settings_common_folder.common_folder, self.__code_folder)

    @property
    def office_file_path(self) -> Path:
        """Return Office file path."""
        return self.__settings_common_folder.office_file_path

    @property
    def workbook_path(self) -> Path:
        """Return Office file path using the legacy property name."""
        return self.office_file_path

    @property
    def common_folder(self) -> Path:
        """Return common folder path."""
        return self.__settings_common_folder.common_folder


class SettingsOptionsHandleOffice:
    """Settings for handling Office options."""

    def __init__(
        self,
        *,
        enable_folder_annotation: bool,
        create_gitignore: bool,
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


def get_vba_project_path(office_file_path: Path) -> str:
    """Return the path to the vbaProject.bin file inside the Office document."""
    if is_word_file(office_file_path):
        return "word/vbaProject.bin"
    if is_powerpoint_file(office_file_path):
        return "ppt/vbaProject.bin"
    return "xl/vbaProject.bin"


def has_vba_code(office_file_path: Path) -> bool:
    """Check if an Office document contains VBA code."""
    try:
        with ZipFile(office_file_path, "r") as zip_ref:
            zip_ref.getinfo(get_vba_project_path(office_file_path))
    except KeyError, OSError, BadZipFile:
        return False
    else:
        return True


def is_excel_file(office_file_path: Path) -> bool:
    """Check if a path has a supported Excel VBA file extension.

    Legacy binary `.xls` files are not supported because they are OLE compound
    documents and do not expose a VBA project ZIP stream.
    """
    return office_file_path.suffix.lower() in {
        ".xlsm",
        ".xltm",
        ".xlam",
    }


def is_word_file(office_file_path: Path) -> bool:
    """Check if a path has a supported Word VBA file extension."""
    return office_file_path.suffix.lower() in {
        ".docm",
        ".dotm",
    }


def is_powerpoint_file(office_file_path: Path) -> bool:
    """Check if a path has a supported PowerPoint VBA file extension."""
    return office_file_path.suffix.lower() in {
        ".pptm",
        ".potm",
    }


def is_office_file(office_file_path: Path) -> bool:
    """Check if a path matches any supported Office file extension."""
    return (
        is_excel_file(office_file_path)
        or is_word_file(office_file_path)
        or is_powerpoint_file(office_file_path)
    )


class OfficeVbaExporter(ABC):
    """Abstract base class for Office VBA exporters."""

    @abstractmethod
    def __init__(self, settings: SettingsFoldersHandleOffice) -> None:
        """Initialize with file path."""
        raise NotImplementedError


class ExcelVbaExporter(OfficeVbaExporter):
    """A placeholder class for ExcelVbaExporter."""

    def __init__(self, settings: SettingsFoldersHandleOffice) -> None:
        """Initialize with file path."""
        app = self.__get_xl_app()
        workbook = None
        try:
            workbook = app.Workbooks.Open(settings.office_file_path, ReadOnly=True)
            settings.export_folder.mkdir(parents=True, exist_ok=True)
            for vb_comp in workbook.VBProject.VBComponents:
                vb_comp_file_name = vb_component_type_factory(
                    vb_comp.Name,
                    vb_comp.Type,
                ).file_name
                vb_comp.Export(Path(settings.export_folder, f"{vb_comp_file_name}"))
        finally:
            if workbook is not None:
                cleanup_office_resource(
                    lambda: workbook.Close(SaveChanges=False),
                    "workbook",
                    "Excel",
                )
            cleanup_office_resource(app.Quit, "application", "Excel")

    def __get_xl_app(self) -> ExcelApplicationProtocol:
        """Get Excel application."""
        return get_noninteractive_excel_app()


class WordVbaExporter(OfficeVbaExporter):
    """Export VBA components from a Word document."""

    def __init__(self, settings: SettingsFoldersHandleOffice) -> None:
        """Initialize with file path."""
        app = get_noninteractive_word_app()
        document = None
        try:
            document = app.Documents.Open(
                str(settings.office_file_path),
                ReadOnly=True,
                AddToRecentFiles=False,
            )
            settings.export_folder.mkdir(parents=True, exist_ok=True)
            for vb_comp in document.VBProject.VBComponents:
                vb_comp_file_name = vb_component_type_factory(
                    vb_comp.Name,
                    vb_comp.Type,
                ).file_name
                vb_comp.Export(Path(settings.export_folder, vb_comp_file_name))
        finally:
            if document is not None:
                cleanup_office_resource(
                    lambda: document.Close(SaveChanges=False),
                    "document",
                    "Word",
                )
            cleanup_office_resource(app.Quit, "application", "Word")


class PowerPointVbaExporter(OfficeVbaExporter):
    """Export VBA components from a PowerPoint presentation."""

    def __init__(self, settings: SettingsFoldersHandleOffice) -> None:
        """Initialize with file path."""
        app = get_noninteractive_powerpoint_app()
        presentation = None
        try:
            presentation = app.Presentations.Open(
                str(settings.office_file_path),
                ReadOnly=True,
                WithWindow=False,
            )
            vb_components = presentation.VBProject.VBComponents
            settings.export_folder.mkdir(parents=True, exist_ok=True)
            for vb_comp in vb_components:
                vb_comp_file_name = vb_component_type_factory(
                    vb_comp.Name,
                    vb_comp.Type,
                ).file_name
                vb_comp.Export(Path(settings.export_folder, vb_comp_file_name))
        finally:
            if presentation is not None:
                cleanup_office_resource(
                    presentation.Close,
                    "presentation",
                    "PowerPoint",
                )

            cleanup_office_resource(app.Quit, "application", "PowerPoint")


def office_vba_exporter_factory(
    settings: SettingsFoldersHandleOffice,
) -> OfficeVbaExporter:
    """Return an exporter suitable for the Office document type."""
    if is_word_file(settings.office_file_path):
        return WordVbaExporter(settings)
    if is_powerpoint_file(settings.office_file_path):
        return PowerPointVbaExporter(settings)
    return ExcelVbaExporter(settings)


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


class CustomUiExtractor:
    """A placeholder class for ExcelCustomUiExtractor."""

    def __init__(self, settings: SettingsFoldersHandleOffice) -> None:
        """Initialize with file path."""
        self.__settings = settings
        self.__extract_custom_ui_files()

    def __extract_custom_ui_files(self) -> None:
        self.__extract_custom_ui_file("customUI/customUI14.xml")
        self.__extract_custom_ui_file("customUI/customUI.xml")

    def __extract_custom_ui_file(self, full_item_name: str) -> None:
        try:
            with ZipFile(self.__settings.office_file_path, "r") as zip_ref:
                file_data = zip_ref.read(full_item_name)
            self.__settings.custom_ui_folder.mkdir(parents=True, exist_ok=True)
            with Path(self.__settings.custom_ui_folder, Path(full_item_name).name).open(
                mode="wb",
            ) as xml_file:
                xml_file.write(file_data)
        except KeyError:
            logger.info(
                "%s does not exists in %s",
                Path(full_item_name).name,
                self.__settings.office_file_path.name,
            )


class Utf8Converter:
    """A placeholder class for Utf8Converter."""

    def __init__(
        self,
        settings: SettingsFoldersHandleOffice,
        options: SettingsOptionsHandleOffice,
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
            mode="w",
            encoding="utf-8",
            newline="\n",
        ) as gitignore_file:
            gitignore_file.write(gitignore_content)

    def __convert_to_utf8(self) -> None:
        for file_path in self.__settings.export_folder.glob("*.*"):
            if self.__is_binary(file_path):
                continue
            text_before_trailing_ws_removal = self.__format_line_breaks(
                file_path.read_text(encoding="cp932"),
            )
            content = self.__remove_trailing_white_space_in_vba_metadata_portion(
                text_before_trailing_ws_removal,
            )
            code_folder = self.__get_code_folder(content)
            code_folder.mkdir(parents=True, exist_ok=True)
            code_path = Path(code_folder, file_path.name)
            code_path.write_text(content, encoding="utf-8", newline="\n")

    def __format_line_breaks(self, text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"

    def __remove_trailing_white_space_in_vba_metadata_portion(self, text: str) -> str:
        remover = self._trailing_white_space_class_factory(text)
        return remover.remove_trailing_white_space(text)

    def _trailing_white_space_class_factory(
        self,
        text: str,
    ) -> ITrailingWhiteSpaceRemover:
        if re.search(r"^VERSION 5", text):
            return FrxModuleTrailingWhiteSpaceRemover()
        return OtherModuleTrailingWhiteSpaceRemover()

    def __get_code_folder(self, text: str) -> Path:
        code_root_folder = self.__settings.code_folder
        if not self.__options.enable_folder_annotation():
            return code_root_folder
        pattern = r"\'@(F|f)older(\s|\()\"(.*)\"((.*)|\))(.*)\n"
        if match := re.search(pattern, text):
            return Path(code_root_folder, *match.group(3).split("."))
        return code_root_folder

    def __is_binary(self, file_path: Path, chunk_size: int = 1024) -> bool:
        try:
            with Path.open(file_path, "rb") as f:
                chunk = f.read(chunk_size)
                return b"\x00" in chunk
        except OSError:
            return False


class ITrailingWhiteSpaceRemover(ABC):
    """A placeholder class for TrailingWhiteSpaceRemover."""

    @abstractmethod
    def remove_trailing_white_space(self, text: str) -> str:
        """Remove trailing white space in VBA metadata portion."""
        raise NotImplementedError


class FrxModuleTrailingWhiteSpaceRemover(ITrailingWhiteSpaceRemover):
    """A placeholder class for FrxModuleTrailingWhiteSpaceRemover."""

    def remove_trailing_white_space(self, text: str) -> str:
        """Remove trailing white space in VBA metadata portion."""
        content_split = text.split("\n")
        pattern = (
            r"^(VERSION 5|Begin|"
            r"\s*(Caption|Client|OleObject|StartUp)|"
            r"End|Attribute VB_)"
        )
        continue_flag = True
        for content_index, content in enumerate(content_split):
            if not continue_flag:
                break
            if re.search(pattern, content):
                content_split[content_index] = content.rstrip()
                continue
            continue_flag = False
        return "\n".join(content_split)


class OtherModuleTrailingWhiteSpaceRemover(ITrailingWhiteSpaceRemover):
    """A placeholder class for OtherModuleTrailingWhiteSpaceRemover."""

    def remove_trailing_white_space(self, text: str) -> str:
        """Remove trailing white space in VBA metadata portion."""
        return text


def add_to_staging(settings: SettingsFoldersHandleOffice) -> None:
    """Add files extracted to staging."""
    process = subprocess.Popen(  # noqa: S603
        ["git", "add", settings.common_folder],  # noqa: S607
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        _, stderr_data = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        _, stderr_data = process.communicate()
    stderr_text = stderr_data.decode("utf-8", errors="replace").strip()
    if process.returncode != 0:
        logger.error(
            "Failed to add extracted files to staging via 'git add'. stderr: %s",
            stderr_text,
        )
        raise AddToStagingError


def get_staging_status() -> str:
    """Return a snapshot of the current staged tree."""
    process = subprocess.Popen(
        ["git", "write-tree"],  # noqa: S607
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        stdout_data, stderr_data = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout_data, stderr_data = process.communicate()
    stderr_text = stderr_data.decode("utf-8", errors="replace").strip()
    if process.returncode != 0:
        logger.error(
            "Failed to get staging status via 'git write-tree'. stderr: %s",
            stderr_text,
        )
        raise StagingStatusError
    return stdout_data.decode("utf-8")


def get_version_from_branch_name() -> str:
    """Get version from branch name."""
    branch_name = get_current_branch_name()
    check_valid_branch_name(branch_name)
    return get_and_check_version_from_branch_name(branch_name)


def check_valid_branch_name(branch_name: str) -> None:
    """Check valid branch name."""
    branch_name_pattern = r"(release|hotfix)/v"
    if not re.compile(branch_name_pattern).match(branch_name):
        raise NotReleaseBranchError(branch_name)


def get_and_check_version_from_branch_name(branch_name: str) -> str:
    """Get and check version from branch name."""
    sem_ver_pattern = (
        r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)"
        r"\.(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
        r"?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )
    match = re.search(sem_ver_pattern, branch_name)
    if match:
        return match.group(0)
    raise InvalidSemVerError(branch_name)


def get_current_branch_name() -> str:
    """Get current branch name."""
    process = subprocess.Popen(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],  # noqa: S607
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        stdout_data, stderr_data = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout_data, stderr_data = process.communicate()  # noqa: RUF059
    return stdout_data.decode("utf-8").replace("\n", "")


class OfficeFileVersion(ABC):
    """Interface for retrieving an Office file version."""

    @property
    @abstractmethod
    def version(self) -> str:
        """Return the Office file version."""
        raise NotImplementedError


class ExcelOfficeFileVersion(OfficeFileVersion):
    """Retrieve a version from an Excel workbook."""

    def __init__(self, office_file_path: Path) -> None:
        """Initialize and retrieve the workbook version."""
        excel_app = get_noninteractive_excel_app()
        workbook = None
        try:
            workbook = excel_app.Workbooks.Open(office_file_path, ReadOnly=True)
            self.__version = str(
                workbook.BuiltinDocumentProperties("Document version"),
            )
        finally:
            if workbook is not None:
                cleanup_office_resource(
                    lambda: workbook.Close(SaveChanges=False),
                    "workbook",
                    "Excel",
                )
            cleanup_office_resource(excel_app.Quit, "application", "Excel")

    @property
    def version(self) -> str:
        """Return the workbook version."""
        return self.__version


class WordOfficeFileVersion(OfficeFileVersion):
    """Retrieve a version from a Word document."""

    def __init__(self, office_file_path: Path) -> None:
        """Initialize and retrieve the document version."""
        word_app = get_noninteractive_word_app()
        document = None
        try:
            document = word_app.Documents.Open(
                str(office_file_path),
                ReadOnly=True,
                AddToRecentFiles=False,
            )
            self.__version = str(
                document.BuiltinDocumentProperties("Document version"),
            )
        finally:
            if document is not None:
                cleanup_office_resource(
                    lambda: document.Close(SaveChanges=False),
                    "document",
                    "Word",
                )
            cleanup_office_resource(word_app.Quit, "application", "Word")

    @property
    def version(self) -> str:
        """Return the document version."""
        return self.__version


class PowerPointOfficeFileVersion(OfficeFileVersion):
    """Retrieve a version from a PowerPoint presentation."""

    def __init__(self, office_file_path: Path) -> None:
        """Initialize and retrieve the presentation version."""
        powerpoint_app = get_noninteractive_powerpoint_app()
        presentation = None
        try:
            presentation = powerpoint_app.Presentations.Open(
                str(office_file_path),
                ReadOnly=True,
                WithWindow=False,
            )
            self.__version = str(
                presentation.BuiltinDocumentProperties("Document version"),
            )
        finally:
            if presentation is not None:
                cleanup_office_resource(
                    presentation.Close,
                    "presentation",
                    "PowerPoint",
                )
            cleanup_office_resource(
                powerpoint_app.Quit,
                "application",
                "PowerPoint",
            )

    @property
    def version(self) -> str:
        """Return the presentation version."""
        return self.__version


def office_file_version_factory(office_file_path: Path) -> OfficeFileVersion:
    """Return a version retriever suitable for the Office file type."""
    if is_word_file(office_file_path):
        return WordOfficeFileVersion(office_file_path)
    if is_powerpoint_file(office_file_path):
        return PowerPointOfficeFileVersion(office_file_path)
    return ExcelOfficeFileVersion(office_file_path)


def get_office_file_version(office_file_path: Path) -> str:
    """Get the version of an Office file."""
    return office_file_version_factory(office_file_path).version


SettingsFoldersHandleExcel = SettingsFoldersHandleOffice
SettingsOptionsHandleExcel = SettingsOptionsHandleOffice
ExcelCustomUiExtractor = CustomUiExtractor
get_workbook_version = get_office_file_version


VBA_CHUNK_SIGNATURE = 0b011
VBA_CHUNK_HEADER_SIZE = 2
RAW_CHUNK_SIZE = 4098


def _read_vba_chunk_header(data: bytes | bytearray, pos: int) -> tuple[int, int, int]:
    """Return the chunk size, signature, and flag for a VBA compressed chunk."""
    header_data = data[pos : pos + VBA_CHUNK_HEADER_SIZE]
    if len(header_data) < VBA_CHUNK_HEADER_SIZE:
        error_message = "Truncated VBA compressed chunk header"
        raise ValueError(error_message)
    header = struct.unpack("<H", header_data)[0]
    chunk_size = (header & 0x0FFF) + 3
    chunk_signature = (header >> 12) & 0x07
    chunk_flag = (header >> 15) & 0x01
    return chunk_size, chunk_signature, chunk_flag


def _validate_vba_chunk(chunk_size: int, chunk_signature: int, chunk_flag: int) -> None:
    """Validate a VBA chunk before processing it."""
    if chunk_signature != VBA_CHUNK_SIGNATURE:
        error_message = "Invalid CompressedChunkSignature in VBA compressed stream"
        raise ValueError(error_message)
    if chunk_flag == 0 and chunk_size != RAW_CHUNK_SIZE:
        error_message = "Invalid raw chunk size"
        raise ValueError(error_message)


def _copy_token_help(
    decompressed_current: int,
    decompressed_chunk_start: int,
) -> tuple[int, int, int, int]:
    """Return masks and bit width for a VBA CopyToken."""
    difference = decompressed_current - decompressed_chunk_start
    bit_count = max((difference - 1).bit_length(), 4)
    length_mask = 0xFFFF >> bit_count
    offset_mask = ~length_mask
    maximum_length = (0xFFFF >> bit_count) + 3
    return length_mask, offset_mask, bit_count, maximum_length


def _decompress_vba_tokens(
    data: bytes | bytearray,
    chunk_start: int,
    chunk_size: int,
    decompressed: bytearray,
) -> int:
    """Decompress a single token sequence in a compressed VBA chunk."""
    pos = chunk_start + 2
    decompressed_chunk_start = len(decompressed)
    while pos < chunk_start + chunk_size:
        flag_byte = data[pos]
        pos += 1
        for bit_index in range(8):
            if pos >= chunk_start + chunk_size:
                break
            flag_bit = (flag_byte >> bit_index) & 1
            if flag_bit == 0:
                decompressed.append(data[pos])
                pos += 1
                continue
            if pos + 1 >= chunk_start + chunk_size:
                error_message = "Truncated VBA copy token"
                raise ValueError(error_message)
            copy_token = struct.unpack("<H", data[pos : pos + 2])[0]
            length_mask, offset_mask, bit_count, _ = _copy_token_help(
                len(decompressed),
                decompressed_chunk_start,
            )
            length = (copy_token & length_mask) + 3
            temp1 = copy_token & offset_mask
            temp2 = 16 - bit_count
            offset = (temp1 >> temp2) + 1
            copy_source = len(decompressed) - offset
            if copy_source < decompressed_chunk_start:
                error_message = "VBA copy token references a previous chunk"
                raise ValueError(error_message)
            for index in range(copy_source, copy_source + length):
                decompressed.append(decompressed[index])
            pos += 2
    return pos


def decompress_stream(compressed_container: bytes | bytearray) -> bytes:
    """Decompress a VBA stream using the minimal algorithm needed here."""
    if not isinstance(compressed_container, bytearray):
        compressed_container = bytearray(compressed_container)

    if not compressed_container or compressed_container[0] != 0x01:
        error_message = "invalid signature byte"
        raise ValueError(error_message)

    decompressed = bytearray()
    pos = 1

    while pos < len(compressed_container):
        chunk_start = pos
        chunk_size, chunk_signature, chunk_flag = _read_vba_chunk_header(
            compressed_container,
            chunk_start,
        )
        _validate_vba_chunk(chunk_size, chunk_signature, chunk_flag)

        if chunk_start + chunk_size > len(compressed_container):
            error_message = "VBA compressed chunk exceeds container"
            raise ValueError(error_message)

        pos = chunk_start + 2
        if chunk_flag == 0:
            decompressed.extend(compressed_container[pos : pos + 4096])
            pos += 4096
            continue

        pos = _decompress_vba_tokens(
            compressed_container,
            chunk_start,
            chunk_size,
            decompressed,
        )

    return bytes(decompressed)


def has_rubberduck_addin_references(office_file_path: Path) -> bool:
    """Check whether the office file includes active Rubberduck reference metadata."""
    try:
        with ZipFile(office_file_path) as zip_ref:
            project_bin = zip_ref.read(get_vba_project_path(office_file_path))
        with olefile.OleFileIO(project_bin) as ole:
            compressed_dir = ole.openstream(["VBA", "dir"]).read()
        directory = decompress_stream(compressed_dir)
    except BadZipFile, KeyError, OSError, ValueError, IndexError, OLE_FILE_ERROR:
        return False
    return bool(re.search(rb"rubberduck\.x(32|64)\.tlb", directory, re.IGNORECASE))


def configure_log_stream_encoding() -> None:
    """Force UTF-8 encoding for non-interactive stderr on Windows."""
    if sys.platform != "win32":
        return
    stderr = getattr(sys, "stderr", None)
    if stderr is None:
        return
    isatty = getattr(stderr, "isatty", None)
    if callable(isatty) and isatty():
        return
    reconfigure = getattr(stderr, "reconfigure", None)
    if not callable(reconfigure):
        return
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except LookupError, OSError, ValueError:
        return


configure_log_stream_encoding()
app = typer.Typer(pretty_exceptions_show_locals=True, pretty_exceptions_short=False)
basicConfig(level=INFO)
logger = getLogger(__name__)
constants = Constants()


def version_callback(value: bool) -> None:  # noqa: FBT001
    """Print version information."""
    if value:
        typer.echo(f"pre-commit-vba version: {__version__}")
        raise typer.Exit


@app.command("extract")
def extract_vba_code_from_office_files(  # noqa: PLR0913, C901
    *,
    target_path: Annotated[str, typer.Option()] = ".",
    folder_suffix: Annotated[str, typer.Option()] = ".VBA",
    export_folder: Annotated[str, typer.Option()] = "export",
    custom_ui_folder: Annotated[str, typer.Option()] = "customUI",
    code_folder: Annotated[str, typer.Option()] = "code",
    version: Annotated[  # noqa: ARG001
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
    enable_folder_annotation: Annotated[
        bool,
        typer.Option("--enable-folder-annotation/--disable-folder-annotation"),
    ] = True,
    create_gitignore: Annotated[
        bool,
        typer.Option("--create-gitignore/--not-create-gitignore"),
    ] = True,
    include_extension: Annotated[
        bool,
        typer.Option("--include-extension/--exclude-extension"),
    ] = True,
) -> None:
    """Extract VBA code from Office files."""
    logger.debug("Target path: %s", str(Path(target_path).resolve()).lower())
    logger.debug("folder-suffix: %s", folder_suffix)
    logger.debug("export-folder: %s", export_folder)
    logger.debug("custom-ui-folder: %s", custom_ui_folder)
    logger.debug("code-folder: %s", code_folder)
    logger.debug("enable-folder-annotation: %s", enable_folder_annotation)
    logger.debug("create-gitignore: %s", create_gitignore)
    logger.debug("include-extension: %s", include_extension)
    options = SettingsOptionsHandleOffice(
        enable_folder_annotation=enable_folder_annotation,
        create_gitignore=create_gitignore,
    )
    resolved_target_path = Path(target_path).resolve()
    check_staging_drift = (
        resolved_target_path == Path.cwd().resolve() and (Path.cwd() / ".git").exists()
    )
    staging_status_before = ""
    if check_staging_drift:
        try:
            staging_status_before = get_staging_status()
        except StagingStatusError:
            sys.exit(1)
    for office_file_path in resolved_target_path.glob("*"):
        if office_file_path.name.startswith("~$"):
            continue
        if not is_office_file(office_file_path):
            continue
        if not has_vba_code(office_file_path):
            continue
        common_folder_settings = SettingsCommonFolder(
            office_file_path=office_file_path,
            folder_suffix=folder_suffix,
            include_extension=include_extension,
        )
        folder_settings = SettingsFoldersHandleOffice(
            settings_common_folder=common_folder_settings,
            export_folder=export_folder,
            custom_ui_folder=custom_ui_folder,
            code_folder=code_folder,
        )
        if folder_settings.common_folder.exists():
            shutil.rmtree(folder_settings.common_folder)
        office_vba_exporter_factory(folder_settings)
        CustomUiExtractor(folder_settings)
        Utf8Converter(folder_settings, options)
        try:
            add_to_staging(folder_settings)
        except AddToStagingError:
            sys.exit(1)
    if check_staging_drift:
        try:
            staging_status_after = get_staging_status()
        except StagingStatusError:
            sys.exit(1)
        if staging_status_before != staging_status_after:
            logger.error(
                "Staging state changed during extract command. "
                "Review staged changes with 'git diff --cached', "
                "re-stage any updated files if needed, and then re-run the command.",
            )
            sys.exit(1)


@app.command()
def check(
    *,
    target_path: Annotated[str, typer.Option()] = ".",
    version: Annotated[  # noqa: ARG001
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """Check Office file version and detect Rubberduck Addin references."""
    try:
        branch_version = get_version_from_branch_name()
        exist_office_file: bool = False
        for office_file_path in Path(target_path).resolve().glob("*"):
            if office_file_path.name.startswith("~$"):
                continue
            if not is_office_file(office_file_path):
                continue
            if not has_vba_code(office_file_path):
                continue
            exist_office_file = True
            if has_rubberduck_addin_references(office_file_path):
                logger.error(
                    "Rubberduck Addin reference detected: %s",
                    office_file_path,
                )
                sys.exit(1)
            office_file_version = get_office_file_version(office_file_path)
            if office_file_version != "v" + branch_version:
                logger.error(
                    "Version mismatch: Office file version '%s' != Branch version '%s'",
                    office_file_version,
                    branch_version,
                )
                sys.exit(1)
        if not exist_office_file:
            logger.warning("No Office files found in the target path.")
            sys.exit(0)
    except NotReleaseBranchError:
        logger.info("Branch is not a release or hotfix branch")
        sys.exit(0)
    except InvalidSemVerError:
        logger.exception("Invalid semantic version in branch name")
        sys.exit(1)
    logger.info("Version check passed.")


extract_vba_code_from_workbooks = extract_vba_code_from_office_files


if __name__ == "__main__":
    app()
