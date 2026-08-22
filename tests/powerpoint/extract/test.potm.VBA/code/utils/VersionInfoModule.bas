Attribute VB_Name = "VersionInfoModule"
'@Folder("utils")
Option Explicit
Option Private Module

'@EntryPoint
Public Sub SetVersion(Optional ByVal manager As VersionManager)
    Dim response As String
    response = InputBox("Input Version")
    If Len(response) = 0 Then Exit Sub
    Dim managerLocal As VersionManager: Set managerLocal = manager
    If managerLocal Is Nothing Then Set managerLocal = New VersionManager: managerLocal.Create ThisPresentation
    managerLocal.SetVersion response
End Sub

'@EntryPoint
Public Sub SetVersionFromBranchIfReleaseOrHotfix()
    On Error GoTo ErrorHandler

    Dim manager As VersionManager: Set manager = New VersionManager: manager.Create ThisPresentation
    Dim resolver As BranchVersionResolver: Set resolver = New BranchVersionResolver: resolver.Create manager
    resolver.SetVersionFromBranchIfReleaseOrHotfix
    Exit Sub
ErrorHandler:
    Err.Raise Err.Number, "VersionInfoModule.SetVersionFromBranchIfReleaseOrHotfix", _
              "Failed to set version from branch: " & Err.Description
End Sub
