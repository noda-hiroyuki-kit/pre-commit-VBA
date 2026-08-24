VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ErrorCode"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("domain")
Option Explicit

Public Enum AppError
    [_Base_Error] = 1024
    INVALID_VALUE
    HAS_CREATED
    NOT_CREATED
End Enum
