VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "SemanticVersioning"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("utils")
Option Explicit

Private Enum ComparisonResult
    LessThan = -1
    EqualTo = 0
    GreaterThan = 1
End Enum

Public Sub EnsureSemVer(ByVal versionText As String, ByVal role As String)
    If isSemVer(normalize(versionText)) Then Exit Sub
    Err.Raise AppError.INVALID_SEMVER, "SemanticVersioning", role & " version must follow SemVer: " & versionText
End Sub

Public Sub EnsureNoRollback(ByVal currentVersion As String, ByVal nextVersion As String)
    EnsureSemVer currentVersion, "Current"
    EnsureSemVer nextVersion, "Next"

    If Compare(nextVersion, currentVersion) >= ComparisonResult.EqualTo Then Exit Sub
    Err.Raise AppError.VERSION_ROLLBACK_NOT_ALLOWED, "SemanticVersioning", "Version rollback is not allowed: " & currentVersion & " -> " & nextVersion
End Sub

Private Function isSemVer(ByVal versionText As String) As Boolean
    Dim regEx As RegExp
    Set regEx = New RegExp
    regEx.Pattern = "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
    isSemVer = regEx.Test(Trim$(versionText))
End Function

Private Function Compare(ByVal leftVersion As String, ByVal rightVersion As String) As ComparisonResult
    Dim leftParts() As String
    Dim rightParts() As String
    Dim leftCore As String
    Dim rightCore As String
    Dim leftPre As String
    Dim rightPre As String

    leftParts = splitVersion(normalize(leftVersion))
    leftCore = leftParts(0)
    leftPre = leftParts(1)

    rightParts = splitVersion(normalize(rightVersion))
    rightCore = rightParts(0)
    rightPre = rightParts(1)

    Compare = compareCore(leftCore, rightCore)
    If Compare <> ComparisonResult.EqualTo Then Exit Function
    Compare = comparePreRelease(leftPre, rightPre)
End Function

Private Function normalize(ByVal versionText As String) As String
    normalize = Trim$(versionText)
    If LCase$(Left$(normalize, 1)) = "v" Then normalize = Mid$(normalize, 2)
End Function

Private Function splitVersion(ByVal versionText As String) As String()
    Dim versionTextLocal As String: versionTextLocal = versionText
    Dim plusPos As Long: plusPos = InStr(versionTextLocal, "+")
    If plusPos > 0 Then versionTextLocal = Left$(versionTextLocal, plusPos - 1)

    Dim dashPos As Long: dashPos = InStr(versionTextLocal, "-")
    Dim result(0 To 1) As String
    If dashPos = 0 Then
        result(0) = versionTextLocal
        result(1) = vbNullString
    Else
        result(0) = Left$(versionTextLocal, dashPos - 1)
        result(1) = Mid$(versionTextLocal, dashPos + 1)
    End If

    splitVersion = result
End Function

Private Function compareNumericIdentifier(ByVal leftText As String, ByVal rightText As String) As ComparisonResult
    If Len(leftText) < Len(rightText) Then
        compareNumericIdentifier = ComparisonResult.LessThan
        Exit Function
    End If
    If Len(leftText) > Len(rightText) Then
        compareNumericIdentifier = ComparisonResult.GreaterThan
        Exit Function
    End If
    If leftText < rightText Then
        compareNumericIdentifier = ComparisonResult.LessThan
        Exit Function
    End If
    If leftText > rightText Then
        compareNumericIdentifier = ComparisonResult.GreaterThan
        Exit Function
    End If
End Function

Private Function compareCore(ByVal leftText As String, ByVal rightText As String) As ComparisonResult
    Dim leftParts() As String:  leftParts = Split(leftText, ".")
    Dim rightParts() As String: rightParts = Split(rightText, ".")

    If UBound(leftParts) <> 2 Or UBound(rightParts) <> 2 Then
        Err.Raise AppError.INVALID_VALUE, "SemanticVersioning.compareCore", _
                  "Core version must contain exactly 3 parts: left=""" & leftText & """, right=""" & rightText & """"
    End If

    Dim index As Long
    For index = 0 To 2
        Dim result As ComparisonResult
        result = compareNumericIdentifier(leftParts(index), rightParts(index))
        If Not result = ComparisonResult.EqualTo Then compareCore = result: Exit Function
    Next index
End Function

Private Function comparePreRelease(ByVal leftText As String, ByVal rightText As String) As ComparisonResult
    If Len(leftText) = 0 And Len(rightText) = 0 Then Exit Function
    If Len(leftText) = 0 Then comparePreRelease = ComparisonResult.GreaterThan: Exit Function
    If Len(rightText) = 0 Then comparePreRelease = ComparisonResult.LessThan: Exit Function
    comparePreRelease = compareIdentifiers(leftText, rightText)
End Function

Private Function compareIdentifiers(ByVal leftText As String, ByVal rightText As String) As ComparisonResult
    Dim leftParts() As String:  leftParts = Split(leftText, ".")
    Dim rightParts() As String: rightParts = Split(rightText, ".")
    Dim maxIndex As Long:       maxIndex = UBound(leftParts)
    If UBound(rightParts) > maxIndex Then maxIndex = UBound(rightParts)
    Dim index As Long
    For index = 0 To maxIndex
        If index > UBound(leftParts) Then compareIdentifiers = ComparisonResult.LessThan:     Exit Function
        If index > UBound(rightParts) Then compareIdentifiers = ComparisonResult.GreaterThan: Exit Function
        Dim result As ComparisonResult
        result = compareIdentifier(leftParts(index), rightParts(index))
        If result <> ComparisonResult.EqualTo Then compareIdentifiers = result: Exit Function
    Next index
End Function

Private Function compareIdentifier(ByVal leftText As String, ByVal rightText As String) As ComparisonResult
    Dim leftNum As Boolean:  leftNum = isNumericIdentifier(leftText)
    Dim rightNum As Boolean: rightNum = isNumericIdentifier(rightText)
    If leftNum And rightNum Then compareIdentifier = compareNumericIdentifier(leftText, rightText): Exit Function
    If leftNum And Not rightNum Then compareIdentifier = ComparisonResult.LessThan: Exit Function
    If Not leftNum And rightNum Then compareIdentifier = ComparisonResult.GreaterThan: Exit Function
    compareIdentifier = Sgn(StrComp(leftText, rightText, vbBinaryCompare))
End Function

Private Function isNumericIdentifier(ByVal valueText As String) As Boolean
    Dim regEx As RegExp
    Set regEx = New RegExp
    regEx.Pattern = "^(0|[1-9]\d*)$"
    isNumericIdentifier = regEx.Test(valueText)
End Function
