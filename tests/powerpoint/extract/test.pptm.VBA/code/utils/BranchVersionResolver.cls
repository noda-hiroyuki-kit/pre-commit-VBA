VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "BranchVersionResolver"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("utils")
Option Explicit

Private Type TClass
    manager As VersionManager
    isSystemUnderTest As Boolean
    branchName As String
    Created As Boolean
End Type

Private Type BranchCommandContext
    commandText As String
    OriginalCurrentDirectory As String
    HasOriginalCurrentDirectory As Boolean
    StdOutText As String
    StdErrText As String
    ExitCode As Long
    errorNumber As Long
    errorDescription As String
End Type

Private this As TClass

Private Sub Class_Initialize()
    this.Created = False
End Sub

Public Sub Create(ByVal manager As VersionManager)
    checkNotCreated
    Set this.manager = manager
    this.isSystemUnderTest = False
    this.Created = True
End Sub

'@Ignore ProcedureNotUsed
Public Sub CreateForTest(ByVal manager As VersionManager, ByVal branchName As String)
    checkNotCreated
    Set this.manager = manager
    this.isSystemUnderTest = True
    this.branchName = branchName
    this.Created = True
End Sub

Public Sub SetVersionFromBranchIfReleaseOrHotfix()
    checkCreated
    Dim branchName As String: branchName = getCurrentBranchName()
    Dim versionText As String: versionText = resolveVersionText(branchName)
    If Len(versionText) = 0 Then Exit Sub
    setVersionFromBranch branchName, versionText
End Sub

Private Function resolveVersionText(ByVal branchName As String) As String
    resolveVersionText = extractVersionFromBranchName(branchName)
End Function

Private Sub setVersionFromBranch(ByVal branchName As String, ByVal versionText As String)
    On Error GoTo SetVersionError
    this.manager.SetVersion versionText
    Exit Sub
SetVersionError:
    raiseSetVersionError branchName
End Sub

Private Sub raiseSetVersionError(ByVal branchName As String)
    Err.Raise Err.Number, "BranchVersionResolver.SetVersionFromBranchIfReleaseOrHotfix", _
              "Failed to set version from branch """ & branchName & """: " & Err.Description
End Sub

Private Sub logBranchNameResolutionError(ByVal commandText As String, ByVal errorNumber As Long, ByVal errorDescription As String)
    Debug.Print "BranchVersionResolver.getCurrentBranchName failed. Command=""" & commandText & """ Error " & CStr(errorNumber) & ": " & errorDescription
End Sub

Private Function getCurrentBranchName() As String
    Dim commandText As String: commandText = "git rev-parse --abbrev-ref HEAD"
    On Error GoTo ErrorHandler
    getCurrentBranchName = readStdOut(commandText)
    Exit Function
ErrorHandler:
    logBranchNameResolutionError commandText, Err.Number, Err.Description
    Err.Raise Err.Number, "BranchVersionResolver.getCurrentBranchName", _
              "Failed to determine current git branch using command """ & commandText & """: " & Err.Description
End Function

Private Function readStdOut(ByVal commandText As String) As String
    If this.isSystemUnderTest Then readStdOut = this.branchName: Exit Function

    Dim shell As WshShell: Set shell = New WshShell
    Dim commandContext As BranchCommandContext: commandContext = newBranchCommandContext(commandText)

    runBranchCommand shell, commandContext
    If commandContext.errorNumber <> 0 Then _
       Err.Raise commandContext.errorNumber, "BranchVersionResolver.readStdOut", commandContext.errorDescription

    readStdOut = commandContext.StdOutText
End Function

Private Function newBranchCommandContext(ByVal commandText As String) As BranchCommandContext
    Dim commandContext As BranchCommandContext
    commandContext.commandText = commandText
    newBranchCommandContext = commandContext
End Function

Private Sub runBranchCommand(ByVal shell As WshShell, ByRef commandContext As BranchCommandContext)
    prepareShellCurrentDirectory shell, commandContext
    executeCommand shell, commandContext
    mapCommandFailure commandContext
    restoreShellCurrentDirectory shell, commandContext
End Sub

Private Sub prepareShellCurrentDirectory(ByVal shell As WshShell, ByRef commandContext As BranchCommandContext)
    Dim presentationPath As String: presentationPath = ThisPresentation.Path
    If Len(Trim$(presentationPath)) = 0 Then _
       setContextError commandContext, AppError.BRANCH_VERSION_PRESENTATION_PATH_NOT_SET, "Workbook path is empty.": Exit Sub

    captureCurrentDirectory shell, commandContext
    If commandContext.errorNumber <> 0 Then Exit Sub

    assignCurrentDirectory shell, presentationPath, commandContext
End Sub

Private Sub captureCurrentDirectory(ByVal shell As WshShell, ByRef commandContext As BranchCommandContext)
    If commandContext.errorNumber <> 0 Then Exit Sub

    On Error GoTo Failed
    commandContext.OriginalCurrentDirectory = shell.CurrentDirectory
    commandContext.HasOriginalCurrentDirectory = True
    Exit Sub

Failed:
    setContextError commandContext, AppError.BRANCH_VERSION_CURRENT_DIRECTORY_SET_FAILED, _
                    "Failed to read shell current directory (" & Err.Description & ")"
End Sub

Private Sub assignCurrentDirectory(ByVal shell As WshShell, ByVal workbookPath As String, ByRef commandContext As BranchCommandContext)
    If commandContext.errorNumber <> 0 Then Exit Sub

    On Error GoTo Failed
    shell.CurrentDirectory = workbookPath
    Exit Sub

Failed:
    setContextError commandContext, AppError.BRANCH_VERSION_CURRENT_DIRECTORY_SET_FAILED, _
                    "Failed to set shell current directory: " & workbookPath & " (" & Err.Description & ")"
End Sub

Private Sub executeCommand(ByVal shell As WshShell, ByRef commandContext As BranchCommandContext)
    If commandContext.errorNumber <> 0 Then Exit Sub

    On Error GoTo Failed
    Dim execResult As WshExec: Set execResult = shell.Exec(commandContext.commandText)
    readExecStreams execResult, commandContext
    Exit Sub

Failed:
    mapExecException commandContext, Err.Description
End Sub

Private Sub readExecStreams(ByVal execResult As WshExec, ByRef commandContext As BranchCommandContext)
    commandContext.StdOutText = Trim$(execResult.StdOut.ReadAll)
    commandContext.StdErrText = Trim$(execResult.StdErr.ReadAll)
    commandContext.ExitCode = execResult.ExitCode
End Sub

Private Sub mapCommandFailure(ByRef commandContext As BranchCommandContext)
    If commandContext.errorNumber <> 0 Then Exit Sub
    If commandContext.ExitCode = 0 Then Exit Sub

    If IsGitNotAvailableError(commandContext.StdErrText) Then setGitNotInstalledError commandContext: Exit Sub

    Dim detail As String: detail = fallbackText(commandContext.StdErrText, "No stderr output.")
    setContextError commandContext, AppError.BRANCH_VERSION_COMMAND_FAILED, _
                    "Command failed with exit code " & CStr(commandContext.ExitCode) & ": " & commandContext.commandText & " (" & detail & ")"
End Sub

Private Sub mapExecException(ByRef commandContext As BranchCommandContext, ByVal errText As String)
    Dim detail As String: detail = fallbackText(commandContext.StdErrText, errText)
    If IsGitNotAvailableError(detail) Then setGitNotInstalledError commandContext: Exit Sub

    setContextError commandContext, AppError.BRANCH_VERSION_COMMAND_FAILED, _
                    "Failed to execute command: " & commandContext.commandText & " (" & detail & ")"
End Sub

Private Sub restoreShellCurrentDirectory(ByVal shell As WshShell, ByRef commandContext As BranchCommandContext)
    If Not commandContext.HasOriginalCurrentDirectory Then Exit Sub

    On Error Resume Next
    shell.CurrentDirectory = commandContext.OriginalCurrentDirectory
    On Error GoTo 0
End Sub

Private Sub setGitNotInstalledError(ByRef commandContext As BranchCommandContext)
    setContextError commandContext, AppError.GIT_NOT_INSTALLED_OR_CONFIGURED, _
                    "Git is not installed or configured. Please install git or check the system PATH configuration."
End Sub

Private Sub setContextError(ByRef commandContext As BranchCommandContext, ByVal errorNumber As Long, ByVal errorDescription As String)
    If commandContext.errorNumber <> 0 Then Exit Sub
    commandContext.errorNumber = errorNumber
    commandContext.errorDescription = errorDescription
End Sub

Private Function fallbackText(ByVal preferred As String, ByVal fallback As String) As String
    fallbackText = Trim$(preferred)
    If Len(fallbackText) = 0 Then fallbackText = fallback
End Function

Private Function IsGitNotAvailableError(ByVal errorDescription As String) As Boolean
    Dim errText As String: errText = LCase$(errorDescription)
    If InStr(errText, "not recognized") > 0 Then IsGitNotAvailableError = True: Exit Function
    If InStr(errText, "cannot find the file") > 0 Then IsGitNotAvailableError = True: Exit Function
    If InStr(errText, "system cannot find the file") > 0 Then IsGitNotAvailableError = True: Exit Function
    If InStr(errText, "'git'") > 0 And InStr(errText, "not found") > 0 Then IsGitNotAvailableError = True: Exit Function
End Function

Private Function extractVersionFromBranchName(ByVal branchName As String) As String
    Dim regEx As RegExp: Set regEx = createTargetBranchRegex()
    If Not regEx.Test(branchName) Then Exit Function
    extractVersionFromBranchName = regEx.Execute(branchName).Item(0).SubMatches.Item(1)
End Function

Private Function createTargetBranchRegex() As RegExp
    Dim regEx As RegExp: Set regEx = New RegExp
    regEx.Pattern = "^(release/|hotfix/)(.*)"
    regEx.IgnoreCase = False
    Set createTargetBranchRegex = regEx
End Function

Private Sub checkCreated()
    If this.Created Then Exit Sub
    Err.Raise AppError.NOT_CREATED, "BranchVersionResolver", "BranchVersionResolver has not been created."
End Sub

Private Sub checkNotCreated()
    If Not this.Created Then Exit Sub
    Err.Raise AppError.HAS_CREATED, "BranchVersionResolver", "BranchVersionResolver has been created."
End Sub
