VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} SetCompanyForm
   Caption         =   "Input Customer Company Name"
   ClientHeight    =   1956
   ClientLeft      =   108
   ClientTop       =   456
   ClientWidth     =   5784
   OleObjectBlob   =   "SetCompanyForm.frx":0000
   StartUpPosition =   1  'オーナー フォームの中央
End
Attribute VB_Name = "SetCompanyForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

'@Folder("createForm")
Option Explicit

Implements IForm

Private Type TSetCompanyForm
    cancelled As Boolean
    company_ As Company
    companyResult As ValidationResult
End Type

Private this As TSetCompanyForm

Private GREEN As Long
Private RED As Long

Private Sub CancelCommandButton_Click()
    OnCancel
End Sub

Private Sub CompanyTextBox_Change()
    textBoxChange
End Sub

Private Sub SetCommandButton_Click()
    On Error GoTo ErrorHandler
    this.company_.Create Me.CompanyTextBox.Text
    Me.Hide
ErrorHandler:
    On Error GoTo 0
    If Err.Number = 0 Then Exit Sub
    Err.Raise Err.Number, Err.Source, Err.Description, Err.HelpFile, Err.HelpContext
End Sub

Private Function IForm_ShowForm(ByVal viewModel As Object) As Boolean
    Set this.company_ = viewModel
    this.cancelled = False
    textBoxChange
    Me.Show
    IForm_ShowForm = Not this.cancelled
End Function

Private Sub UserForm_Initialize()
    GREEN = RGB(0, 127, 0)
    RED = RGB(255, 0, 0)
    Me.Width = 300
    Me.Height = 185
End Sub

Private Sub textBoxChange()
    Set this.companyResult = this.company_.IsValid(Me.CompanyTextBox.Text)
    ValidateForm
End Sub

Private Sub UserForm_QueryClose(ByRef Cancel As Integer, ByRef CloseMode As Integer)
    If Not CloseMode = VbQueryClose.vbFormControlMenu Then Exit Sub
    Cancel = True
    OnCancel
End Sub

Private Sub OnCancel()
    this.cancelled = True
    Me.Hide
End Sub

Private Sub ValidateForm()
    Me.SetCommandButton.Enabled = this.companyResult.result = Valid
    setLabelProperties Me.CompanyValidationMessageLabel, this.companyResult
End Sub

Private Sub setLabelProperties(ByVal labelControl As MSForms.Label, ByVal result As ValidationResult)
    With labelControl
        .Caption = result.Message
        .ForeColor = setCaptionColor(result)
    End With
End Sub

Private Function setCaptionColor(ByVal result As ValidationResult) As Long
    If result.result = Valid Then setCaptionColor = GREEN: Exit Function
    setCaptionColor = RED
End Function
