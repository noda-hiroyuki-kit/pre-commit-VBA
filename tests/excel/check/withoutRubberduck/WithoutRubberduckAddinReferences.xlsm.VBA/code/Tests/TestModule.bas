Attribute VB_Name = "TestModule"
'@TestModule
'@Folder "Tests"


Option Explicit
Option Private Module

Private testCon As TestController

'@ModuleInitialize
Private Sub ModuleInitialize()
    'this method runs once per module.
    Set testCon = New TestController
End Sub

'@ModuleCleanup
Private Sub ModuleCleanup()
    'this method runs once per module.
    Set testCon = Nothing
End Sub

'@TestInitialize
Private Sub TestInitialize()
    'This method runs before every test in the module..
    testCon.Fakes.MsgBox.Returns vbOK
    ShowMsgBox
End Sub

'@TestCleanup
'@Ignore EmptyMethod
Private Sub TestCleanup()
    'this method runs after every test in the module.
End Sub

'@TestMethod("ShowMsgBox")
Public Sub PromptIsExpected()
    On Error GoTo TestFail
    testCon.Fakes.MsgBox.Verify.Parameter _
        testCon.Fakes.Params.MsgBox.Prompt, _
        "This Workbook is for check sub command test."
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next

    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("ShowMsgBox")
Public Sub MsgBoxStyleIsExpected()
    On Error GoTo TestFail
    testCon.Fakes.MsgBox.Verify.Parameter _
        testCon.Fakes.Params.MsgBox.Buttons, _
        vbSystemModal + vbInformation + vbOKOnly
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next

    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("ShowMsgBox")
Public Sub TitleIsExpected()
    On Error GoTo TestFail
    testCon.Fakes.MsgBox.Verify.Parameter _
        testCon.Fakes.Params.MsgBox.Title, _
        "This workbook information"
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next

    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub
