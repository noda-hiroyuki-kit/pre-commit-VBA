VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "TestController"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder("Tests")
Option Explicit
' Reference page
' RubberDuckでテスト駆動開発したXLSMの配布時にコンパイラ動作を簡単切替
' by @ShortArrow(さぼったろう)
' https://qiita.com/ShortArrow/items/a16477a0926a68a88ead

'canRef = True : in developing
'canRef = False : in deploy
#Const canRef = True

#If canRef Then
Private Type TTestController
    Assert As Rubberduck.AssertClass
    Fakes As Rubberduck.FakesProvider
    Mocks As Rubberduck.MockProvider
End Type

#Else
Private Type TTestController
    Assert As Object
    Fakes As Object
    Mocks As Object
End Type

#End If

Private this As TTestController

Private Sub Class_Initialize()
    #If canRef Then
        Set this.Assert = New Rubberduck.AssertClass
        Set this.Fakes = New Rubberduck.FakesProvider
        Set this.Mocks = New Rubberduck.MockProvider
    #Else
        Set this.Assert = CreateObject("Rubberduck.AssertClass")
        Set this.Fakes = CreateObject("Rubberduck.FakesProvider")
        Set this.Mocks = CreateObject("Rubberduck.MockProvider")
    #End If
End Sub

Private Sub Class_Terminate()
    Set this.Assert = Nothing
    Set this.Fakes = Nothing
    Set this.Mocks = Nothing
End Sub

#If canRef Then
Public Property Get Assert() As Rubberduck.AssertClass
    Set Assert = this.Assert
End Property

Public Property Get Fakes() As Rubberduck.FakesProvider
    Set Fakes = this.Fakes
End Property

Public Property Get Mocks() As Rubberduck.MockProvider
    Set Mocks = this.Mocks
End Property

#Else
Public Property Get Assert() As Object
    Set Assert = this.Assert
End Property

Public Property Get Fakes() As Object
    Set Fakes = this.Fakes
End Property

Public Property Get Mocks() As Object
    Set Mocks = this.Mocks
End Property
#End If
