VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} RegisterProductForm
   Caption         =   "RegisterProductForm"
   ClientHeight    =   2676
   ClientLeft      =   60
   ClientTop       =   264
   ClientWidth     =   4092
   OleObjectBlob   =   "RegisterProductForm.frx":0000
   StartUpPosition =   1  'オーナー フォームの中央
End
Attribute VB_Name = "RegisterProductForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'@Folder("registerForm")
Option Explicit

Implements IForm

Private Type TProductCodeResistorForm
    cancelled As Boolean
    Product As Product
    codeResult As ValidationResult
    nameResult As ValidationResult
End Type

Private GREEN As Long
Private RED As Long

Private this As TProductCodeResistorForm

Public Property Get IsCancelled() As Boolean
    IsCancelled = this.cancelled
End Property

Private Sub CancelCommandButton_Click()
    OnCancel
End Sub

Private Function IForm_ShowForm(ByVal viewModel As Object) As Boolean
    Set this.Product = viewModel
    Me.Show
    IForm_ShowForm = Not this.cancelled
End Function

Private Sub ProductCodeTextBox_Change()
    textBoxChange
End Sub

Private Sub ProductNameTextBox_Change()
    textBoxChange
End Sub

Private Sub textBoxChange()
    Set this.codeResult = this.Product.code.IsValid(ProductCodeTextBox.Text)
    Set this.nameResult = this.Product.Name.IsValid(ProductNameTextBox.Text)
    ValidateForm
End Sub
Private Sub ResisterCommandButton_Click()
    this.Product.code.Create ProductCodeTextBox.Text
    this.Product.Name.Create ProductNameTextBox.Text
    Me.Hide
End Sub

Private Sub UserForm_Initialize()
    GREEN = RGB(0, 255, 0)
    RED = RGB(255, 0, 0)
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
    Me.ResisterCommandButton.Enabled = _
        (this.codeResult.result = Valid) _
        And (this.nameResult.result = Valid)
    setLabelProperties Me.CodeValidationMessageLabel, this.codeResult
    setLabelProperties Me.NameValidationMessageLabel, this.nameResult
End Sub

Private Sub setLabelProperties(ByVal control As Object, ByVal result As ValidationResult)
    With control
        .Caption = result.Message
        .ForeColor = setCaptionColor(result)
    End With
End Sub

Private Function setCaptionColor(ByVal result As ValidationResult) As Long
    If result.result = Valid Then setCaptionColor = GREEN: Exit Function
    setCaptionColor = RED
End Function
