Attribute VB_Name = "TestCustomerPersonInCharge"
'@TestModule
'@Folder "Tests.domain.model.customer"

Option Explicit
Option Private Module

Private testCon As TestController
Private sut As CustomerPersonInCharge
Private response As ValidationResult:

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
    'This method runs before every test in the module.
    Set sut = New CustomerPersonInCharge
End Sub

'@TestCleanup
Private Sub TestCleanup()
    'this method runs after every test in the module.
    Set sut = Nothing
    Set response = Nothing
End Sub

'@TestMethod("domain.model.CustomerPersonInCharge")
Private Sub TestParsonNameLengthTooShort()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = String(3, "A")
    'Act:
    Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Invalid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "Name must be at least") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("domain.model.CustomerPersonInCharge")
Private Sub TestParsonNameLengthTooLong()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = String(21, "A")
    'Act:
    Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Invalid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "Name must be at most") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("domain.model.CustomerPersonInCharge")
Private Sub TestParsonNameMustHaveValidHonorific()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = String(5, "A")
    'Act:
    Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Invalid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "Name must have valid honorific.") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("domain.model.CustomerPersonInCharge")
Private Sub TestParsonWrongCharacter()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = "Mx. TESTtest1!"
    'Act:
    Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Invalid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "Name must contain only letters, digits, spaces, and dots.") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub

'@TestMethod("domain.model.CustomerPersonInCharge")
Private Sub TestCodeOk()
    On Error GoTo TestFail
    'Arrange:
    Dim trialValue As String: trialValue = "Mr. TEST1234TEST1234"
    'Act:
     Set response = sut.IsValid(trialValue)
    'Assert:
    testCon.Assert.AreEqual Valid, response.result
    testCon.Assert.IsTrue InStr(response.Message, "OK") > 0
TestExit:
    '@Ignore UnhandledOnErrorResumeNext
    On Error Resume Next
    Exit Sub
TestFail:
    testCon.Assert.Fail "Test raised an error: #" & Err.Number & " - " & Err.Description
    Resume TestExit
End Sub
