VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ValidationResult"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("domain")
Option Explicit

' Validation Result Class

Public Enum EValidationResult
    Undecided = 1
    Valid
    Invalid
End Enum

Private Type TThis
    result As EValidationResult
    Message As String
End Type

Private this As TThis

Private Sub Class_Initialize()
    this.result = Undecided
    this.Message = vbNullString
End Sub

Public Property Get result() As EValidationResult
    result = this.result
End Property

Public Property Get Message() As String
    Message = this.Message
End Property

Public Sub SetValid()
    this.result = Valid
End Sub

Public Sub SetInvalid()
    this.result = Invalid
End Sub

Public Sub SetMessage(ByVal messageArg As String)
    this.Message = messageArg
End Sub
