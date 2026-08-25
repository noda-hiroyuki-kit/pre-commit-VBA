Attribute VB_Name = "MainModule"
'@Folder("src")
Option Explicit

Public Sub ShowMsgBox()
    MsgBox "This Document is for check sub command test.", _
           vbSystemModal + vbInformation + vbOKOnly, _
           "This document information"
End Sub
