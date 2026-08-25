Attribute VB_Name = "SampleTabModule"
'@Folder("customUI.sampleTab")
Option Explicit

'Keep the contents of the text box to module variable.
'テキストボックスの内容は自分で保持する

Private Type TRibbon
    SampleText As String
End Type

Private this As TRibbon

'@Ignore ParameterNotUsed, ParameterCanBeByVal, ProcedureNotUsed
Public Sub SampleText_getText(ByRef control As IRibbonControl, ByRef Text As Variant)
    Text = this.SampleText
End Sub

'@Ignore ParameterNotUsed, ParameterCanBeByVal, ProcedureNotUsed
Public Sub SampleText_onChange(ByRef control As IRibbonControl, ByRef Text As Variant)
    this.SampleText = Text
End Sub

'@Ignore ParameterNotUsed, ProcedureNotUsed
Public Sub SampleButton_onAction(ByVal control As IRibbonControl)
    On Error GoTo ErrorHandler
'    Word.Application.EnableEvents = False
    MsgBox "Clicked Search Button!" & vbNewLine _
         & "Text Box value is " & this.SampleText, _
           vbSystemModal + vbInformation + vbOKOnly
ErrorHandler:
'    Word.Application.EnableEvents = True
    On Error GoTo 0
    If Err.Number = 0 Then Exit Sub
    Err.Raise Err.Number, Err.Source, Err.Description, Err.HelpFile, Err.HelpContext
End Sub

'@Ignore ParameterNotUsed, ProcedureNotUsed
Public Sub AppIntroductionButton_onAction(ByVal control As IRibbonControl)
    On Error GoTo ErrorHandler
'    Word.Application.EnableEvents = False
    ThisAppModule.ShowAppIntroduction
ErrorHandler:
'    Word.Application.EnableEvents = True
    On Error GoTo 0
    If Err.Number = 0 Then Exit Sub
    Err.Raise Err.Number, Err.Source, Err.Description, Err.HelpFile, Err.HelpContext
End Sub

'@Ignore ParameterNotUsed, ProcedureNotUsed
Public Sub AppVersionsButton_onAction(ByVal control As IRibbonControl)
    On Error GoTo ErrorHandler
'    Word.Application.EnableEvents = False
    ThisAppModule.ShowVersion
ErrorHandler:
'    Word.Application.EnableEvents = True
    On Error GoTo 0
    If Err.Number = 0 Then Exit Sub
    Err.Raise Err.Number, Err.Source, Err.Description, Err.HelpFile, Err.HelpContext
End Sub

'@Ignore ParameterNotUsed, ProcedureNotUsed
Public Sub CreateInvitationButton_onAction(ByVal control As IRibbonControl)
    On Error GoTo ErrorHandler
'    Word.Application.EnableEvents = False
    ShowFormModule.CreateInvitation
ErrorHandler:
'    Word.Application.EnableEvents = True
    On Error GoTo 0
    If Err.Number = 0 Then Exit Sub
    Err.Raise Err.Number, Err.Source, Err.Description, Err.HelpFile, Err.HelpContext
End Sub
