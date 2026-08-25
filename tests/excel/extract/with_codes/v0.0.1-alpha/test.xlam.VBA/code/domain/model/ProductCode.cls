VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ProductCode"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("domain.model")
Option Explicit
' Product Code Class

Private Const MIN_LENGTH As Long = 4
Private Const MAX_LENGTH As Long = 20
Private Const REG_PATTERN As String = "[0-9A-Z]+"

Private Type TProductCode
    Value As String
    Created As Boolean
End Type

Private this As TProductCode

Private Sub Class_Initialize()
    this.Created = False
    this.Value = vbNullString
End Sub

Public Property Get Value() As String
    If Not this.Created Then Err.Raise AppError.NOT_CREATED, , "Product code has not created."
    Value = this.Value
End Property

Public Sub Create(ByVal ValueArg As String)
    If this.Created Then Err.Raise AppError.HAS_CREATED, , "Product code has Already created."
    Dim result As ValidationResult: Set result = IsValid(ValueArg)
    If Not result.result = Valid Then Err.Raise AppError.INVALID_VALUE, , result.Message
    this.Value = ValueArg
    this.Created = True
End Sub

Public Function IsValid(ByVal ValueArg As String) As ValidationResult
    Set IsValid = New ValidationResult
    Dim valueLength As Long: valueLength = LenB(StrConv(ValueArg, vbFromUnicode))
    If valueLength < MIN_LENGTH Then IsValid.SetInvalid: _
        IsValid.SetMessage "Code length is " & MIN_LENGTH & " Characters or more.": Exit Function
    If valueLength > MAX_LENGTH Then IsValid.SetInvalid: _
        IsValid.SetMessage "Code length is " & MAX_LENGTH & " Characters or less.": Exit Function
    If Not isOkInCharacterType(ValueArg) Then IsValid.SetInvalid: _
        IsValid.SetMessage "Code Characters MUST be Upper case letters or numbers.": Exit Function
    IsValid.SetValid
    IsValid.SetMessage "OK"
End Function

Private Function isOkInCharacterType(ByVal value_ As String) As Boolean
    Dim regEx As RegExp: Set regEx = New RegExp
    With regEx
        .Global = True
        .IgnoreCase = False
        .Pattern = REG_PATTERN
        If Not .test(value_) Then isOkInCharacterType = False: Exit Function
        Dim col As MatchCollection
        Set col = .Execute(value_)
        isOkInCharacterType = (value_ = col.Item(0).Value)
    End With
End Function
