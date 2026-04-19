Attribute VB_Name = "MainModule"
'@Folder "src"
Option Explicit

Public Sub ShowMsgBox()
    MsgBox "This Workbook is for check sub command test.", _
           vbSystemModal + vbInformation + vbOKOnly, _
           "This workbook information"
End Sub
