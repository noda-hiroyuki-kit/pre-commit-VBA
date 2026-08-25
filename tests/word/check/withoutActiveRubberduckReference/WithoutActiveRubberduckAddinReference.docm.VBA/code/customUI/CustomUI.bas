Attribute VB_Name = "CustomUI"
'@Folder "customUI"
Option Explicit

'@Ignore MoveFieldCloserToUsage, VariableNotUsed, EncapsulatePublicField
Public p_ribbon As IRibbonUI

'@Ignore ProcedureNotUsed
Public Sub OnLoad(ByVal ribbon As IRibbonUI)
    'This is the only time you can get an instance of the ribbon.
    'Make sure to keep a reference to the ribbon in a variable here.
    'リボンのインスタンスを取得できる唯一の機会です
    'ここで必ずリボンの参照を変数に保持しておきましょう。
    Set p_ribbon = ribbon
End Sub

'@Ignore ParameterNotUsed, ParameterCanBeByVal, ProcedureNotUsed
Public Sub SampleTab_getVisible(ByRef control As IRibbonControl, ByRef returnedVal As Variant)
    'Always show sample tab.
    '常にタブを表示する
    returnedVal = True
End Sub
