Attribute VB_Name = "SampleTabModule"
'@IgnoreModule ParameterNotUsed, ParameterCanBeByVal
'@Folder "customUI.sample_tab"
Option Explicit
Option Private Module
'Keep the contents of the text box to module variable.
'テキストボックスの内容は自分で保持する

Private Type TRibbon
    SampleText As String
End Type

Private this As TRibbon

'@EntryPoint
Public Sub SampleText_GetText(ByRef control As IRibbonControl, ByRef Text As Variant)
    Text = this.SampleText
End Sub

'@EntryPoint
Public Sub SampleText_OnChange(ByRef control As IRibbonControl, ByRef Text As Variant)
    this.SampleText = Text
End Sub

'@EntryPoint
Public Sub SampleButton_OnAction(ByVal control As IRibbonControl)
    MsgBox "Clicked Search Button!" & vbNewLine _
         & "Text Box value is " & this.SampleText, _
           vbSystemModal + vbInformation + vbOKOnly
End Sub

'@EntryPoint
Public Sub AppIntroductionButton_OnAction(ByVal control As IRibbonControl)
    Set ThisPresentation = ActivePresentation
    MsgBox "Clicked App Introduction Button!" & vbNewLine _
         & "This presentation is " & ThisPresentation.Name, _
           vbSystemModal + vbInformation + vbOKOnly
End Sub

'@EntryPoint
Public Sub AppVersionButton_OnAction(ByVal control As IRibbonControl)
    Set ThisPresentation = ActivePresentation
    Dim appVersion As VersionManager: Set appVersion = New VersionManager
    appVersion.Create ThisPresentation
    MsgBox "Clicked App Version Button!" & vbNewLine _
         & "This presentation is Ver. " & appVersion.Version, _
           vbSystemModal + vbInformation + vbOKOnly
End Sub

'@EntryPoint
Public Sub SetCompanyButton_OnAction(ByVal control As IRibbonControl)
    Set ThisPresentation = ActivePresentation
    ShowFormModule.ShowInputCompanyForm
End Sub
