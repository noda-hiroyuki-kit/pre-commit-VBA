Attribute VB_Name = "ThisAppModule"
'@Folder "src"
Option Explicit
Option Private Module

Public Sub ShowAppIntroduction()
    MsgBox "This app is test-doc.", vbOKOnly + vbSystemModal + vbInformation
End Sub

Public Sub ShowVersion(Optional ByVal manager As VersionManager)
    Dim managerLocal As VersionManager: Set managerLocal = manager
    If managerLocal Is Nothing Then Set managerLocal = New VersionManager: managerLocal.Create ThisDocument
    MsgBox "test-doc" & vbNewLine & managerLocal.Version, vbOKOnly + vbSystemModal + vbInformation
End Sub

Public Sub CreateInvitationDocument(ByVal customerArg As Customer)
    ThisDocument.Content.Copy
    Dim newDoc As Word.Document: Set newDoc = Word.Documents.Add
    newDoc.Content.Paste
    replaceCustomer newDoc, customerArg
End Sub

Private Sub replaceCustomer(ByVal targetDoc As Word.Document, ByVal customerArg As Customer)
    Dim body As Range
    For Each body In targetDoc.StoryRanges
        With body.Find
            .Text = "[Client Name / Valued Partner]"
            .Replacement.Text = customerArg.Person.Value & " / " & customerArg.Company.Value
            .Forward = True
            .Wrap = wdFindContinue
            .Format = False
            .MatchCase = False
            .MatchWholeWord = False
            .MatchByte = False
            .MatchAllWordForms = False
            .MatchSoundsLike = False
            .MatchWildcards = False
            .Execute Replace:=wdReplaceAll
        End With
    Next body
End Sub
