Attribute VB_Name = "Constants"
'@Folder("domain")
Option Explicit

'@Ignore EncapsulatePublicField
Public ThisPresentation As Presentation

Public Enum AppError
    [_Base_Error] = 1024
    BRANCH_VERSION_COMMAND_FAILED
    BRANCH_VERSION_CURRENT_DIRECTORY_SET_FAILED
    BRANCH_VERSION_PRESENTATION_PATH_NOT_SET
    GIT_NOT_INSTALLED_OR_CONFIGURED
    INVALID_VALUE
    INVALID_SEMVER
    HAS_CREATED
    MISSING_PROPERTY
    NOT_CREATED
    VERSION_ROLLBACK_NOT_ALLOWED
End Enum
