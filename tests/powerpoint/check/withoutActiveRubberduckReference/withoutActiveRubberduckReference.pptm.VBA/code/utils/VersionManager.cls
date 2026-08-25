VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "VersionManager"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("utils")
Option Explicit

Private Const INITIAL_VERSION As String = "v0.0.1"

Private Type TVersionManager
    versionForTest As String
    presentationVersion As Office.DocumentProperty
    semVer As SemanticVersioning
    Created As Boolean
    isSystemUnderTest As Boolean
End Type

Private this As TVersionManager

Private Sub Class_Initialize()
    this.versionForTest = vbNullString
    Set this.semVer = New SemanticVersioning
    this.Created = False
End Sub

'@Ignore ProcedureNotUsed
Public Sub CreateForTest(ByVal currentVersion As String)
    checkNotCreated
    this.isSystemUnderTest = True
    this.semVer.EnsureSemVer currentVersion, "current"
    this.versionForTest = currentVersion
    this.Created = True
End Sub

Public Sub Create(ByVal targetPresentation As Presentation)
    checkNotCreated
    this.isSystemUnderTest = False
    On Error GoTo MissingPropertyError
    Set this.presentationVersion = targetPresentation.BuiltInDocumentProperties.Item("Document Version")
    On Error GoTo 0
    Dim propertyVersion As String
    propertyVersion = CStr(this.presentationVersion.Value)
    If Len(propertyVersion) = 0 Then
        ApplyToPresentation INITIAL_VERSION
    Else
        this.semVer.EnsureSemVer propertyVersion, "current"
    End If
    this.Created = True
    Exit Sub
MissingPropertyError:
    Err.Raise AppError.MISSING_PROPERTY, "VersionManager.Create", _
              "Built-in document property ""Document Version"" is missing."
End Sub

Public Property Get Version() As String
    checkCreated
    Version = getVersion
End Property

Private Function getVersion() As String
    If this.isSystemUnderTest Then getVersion = this.versionForTest: Exit Function
    getVersion = CStr(this.presentationVersion.Value)
End Function

Public Sub SetVersion(ByVal nextVersion As String)
    checkCreated
    ApplyToPresentation nextVersion
End Sub

Private Sub ApplyToPresentation(ByVal nextVersion As String)
    this.semVer.EnsureSemVer nextVersion, "next"

    Dim normalizedNextVersion As String
    normalizedNextVersion = normalizedVersion(nextVersion)

    Dim currentVersion As String: currentVersion = getVersion
    If Len(Trim$(currentVersion)) > 0 Then
        this.semVer.EnsureNoRollback currentVersion, normalizedNextVersion
    End If
    setVersion_ normalizedNextVersion
End Sub

Private Function normalizedVersion(ByVal versionText As String) As String
    normalizedVersion = Trim$(versionText)
End Function

Private Sub setVersion_(ByVal nextVersion As String)
    If this.isSystemUnderTest Then this.versionForTest = nextVersion: Exit Sub
    this.presentationVersion.Value = nextVersion
End Sub

Private Sub checkCreated()
    If this.Created Then Exit Sub
    Err.Raise AppError.NOT_CREATED, "VersionManager", "VersionManager has not been created."
End Sub

Private Sub checkNotCreated()
    If Not this.Created Then Exit Sub
    Err.Raise AppError.HAS_CREATED, "VersionManager", "VersionManager has been created."
End Sub
