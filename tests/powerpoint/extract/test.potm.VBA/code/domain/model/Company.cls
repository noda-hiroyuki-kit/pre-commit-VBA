VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Company"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("domain.model")
Option Explicit

Private Const MIN_LENGTH As Long = 4
Private Const MAX_LENGTH As Long = 50
Private Const REG_PATTERN As String = "^[0-9A-Za-z. ,]+$"

Private Type TCompany
    Value As String
    Created As Boolean
End Type

Private this As TCompany

Private Sub Class_Initialize()
    this.Created = False
    this.Value = vbNullString
End Sub

Public Property Get Value() As String
    If Not this.Created Then Err.Raise AppError.NOT_CREATED, , "Company has not been created."
    Value = this.Value
End Property

Public Sub Create(ByVal ValueArg As String)
    If this.Created Then Err.Raise AppError.HAS_CREATED, , "Company has already been created."
    Dim result As ValidationResult: Set result = IsValid(ValueArg)
    If Not result.result = Valid Then Err.Raise AppError.INVALID_VALUE, , result.Message
    this.Value = ValueArg
    this.Created = True
End Sub

Public Function IsValid(ByVal ValueArg As String) As ValidationResult
    Set IsValid = New ValidationResult
    Dim valueLength As Long: valueLength = Len(ValueArg)
    If valueLength < MIN_LENGTH Then
        IsValid.SetInvalid
        IsValid.SetMessage "Name must be at least " & MIN_LENGTH & " characters."
        Exit Function
    End If
    If valueLength > MAX_LENGTH Then
        IsValid.SetInvalid
        IsValid.SetMessage "Name must be at most " & MAX_LENGTH & " characters."
        Exit Function
    End If
    If Not hasValidCharacterType(ValueArg) Then
        IsValid.SetInvalid
        IsValid.SetMessage "Name must contain only letters, digits, spaces, and dots."
        Exit Function
    End If
    IsValid.SetValid
    IsValid.SetMessage "OK"
End Function

Private Function hasValidCharacterType(ByVal value_ As String) As Boolean
    hasValidCharacterType = testRegEx(value_, REG_PATTERN)
End Function

Private Function testRegEx(ByVal value_ As String, ByVal pattern_ As String) As Boolean
    Dim regEx As RegExp: Set regEx = New RegExp
    With regEx
        .Global = False
        .IgnoreCase = False
        .Pattern = pattern_
        testRegEx = .Test(value_)
    End With
End Function
