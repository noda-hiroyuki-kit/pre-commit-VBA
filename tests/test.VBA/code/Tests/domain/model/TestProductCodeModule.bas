Attribute VB_Name = "TestProductCodeModule"
'@TestModule
'@Folder "Tests.domain.model"


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
End Sub

'@TestCleanup
Private Sub TestCleanup()
    'this method runs after every test in the module.
End Sub

'@TestMethod("domain.model.ProductCode")
Private Sub TestCodeLengthTooShort()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = String(3, "A")
    'Act:
    Dim sut As ProductCode: Set sut = New ProductCode
    Dim response As ValidationResult: Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Invalid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "Characters or more") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Set response = Nothing
    Set sut = Nothing
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("domain.model.ProductCode")
Private Sub TestCodeLengthTooLong()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = String(21, "A")
    'Act:
    Dim sut As ProductCode: Set sut = New ProductCode
    Dim response As ValidationResult: Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Invalid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "Characters or less") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Set sut = Nothing
    Set response = Nothing
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("domain.model.ProductCode")
Private Sub TestCodeWrongCharacter()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = "TESTtest1"
    'Act:
    Dim sut As ProductCode: Set sut = New ProductCode
    Dim response As ValidationResult: Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Invalid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "MUST be Upper case letters or numbers.") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Set response = Nothing
    Set sut = Nothing
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("domain.model.ProductCode")
Private Sub TestCodeOk()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = "TEST1234TEST1234"
    'Act:
    Dim sut As ProductCode: Set sut = New ProductCode
    Dim response As ValidationResult: Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Valid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "OK") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Set response = Nothing
    Set sut = Nothing
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub
