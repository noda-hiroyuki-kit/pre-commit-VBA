Attribute VB_Name = "SampleTab"
'@IgnoreModule ParameterNotUsed, ParameterCanBeByVal
'@Folder "customUI.sample_tab"
Option Explicit
'Keep the contents of the text box to module variable.
'テキストボックスの内容は自分で保持する

Private Type TRibbon
    SampleText As String
End Type

Private this As TRibbon

Private Sub SampleText_getText(ByRef control As IRibbonControl, ByRef Text As Variant)
    Text = this.SampleText
End Sub

Private Sub SampleText_onChange(ByRef control As IRibbonControl, ByRef Text As Variant)
    this.SampleText = Text
End Sub

Private Sub SampleButton_onAction(ByVal control As IRibbonControl)
    Excel.Application.EnableEvents = False
    MsgBox "Clicked Search Button!" & vbNewLine _
         & "Text Box value is " & this.SampleText, _
           vbSystemModal + vbInformation + vbOKOnly
    Excel.Application.EnableEvents = False
End Sub
