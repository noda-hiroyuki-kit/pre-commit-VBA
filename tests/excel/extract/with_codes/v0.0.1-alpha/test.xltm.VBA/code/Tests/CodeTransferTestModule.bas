Attribute VB_Name = "CodeTransferTestModule"
'@Folder("Tests")
Option Explicit

' ① this comment crashes with an error.
'
Private Sub showMessageBox()
    MsgBox "This module crashes with an error.", vbCritical + vbSystemModal + vbOKOnly
End Sub
